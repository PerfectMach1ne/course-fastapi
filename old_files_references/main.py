from fastapi import FastAPI, Body, Response, status, HTTPException
# from fastapi.params import Body      above is shorter and works just fine
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI() # FastAPI instance to call in uvicorn in order to start a server
# command to type to start the server:
# uvicorn main:app --reload
# --reload for not having to restart the server to see any new changes to the code


class Post(BaseModel):  # from Pydantic
    title: str
    content: str
    published: bool = True  # default value if user doesn't provide a value
    rating: Optional[int] = None  # optional field


my_posts = [{"id": 1, "title": "post title", "content": "example post content"},
            {"id": 2, "title": "favourite foods", "content": "piza..."}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")  # Decorator that turns root() into an API path operation
def root():  # could be async def root(), but asynchronous call is not necessary there
    return {"message": "HEELOOOOO WOOOORLD!!!!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: dict = Body(...)):  # JSON as payload is converted to a regular Python dictionary
def create_posts(post: Post):  # JSON as payload is converted to a regular Python dictionary
    print(post)
    # print(posts.rating)
    # If you ever need to convert a Pydantic model to a Python dictionary, use this:
    print(post.dict())
    # return {"data": f"Post title: {post.title}; post content: {post.content}"}
    # return {"new_post": f"Post title: {payload['title']}; post content: {payload['content']}"}
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 575757)  # bruh
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:  # If post is not found
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND # Better than hardcoding things ("no magic numbers" "pattern")
        # return {'message': f"Post with the ID {id} was not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} was not found.")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} does not exist.")
    my_posts.pop(index)
    # This below won't work due to how FastAPI interprets 204 (no data sent back)
    # return {'message': "Post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} does not exist.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data': post_dict}
