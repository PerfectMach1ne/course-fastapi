from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

import time

app = FastAPI()  # FastAPI instance to call in uvicorn in order to start a server
# command to type to start the server:
# uvicorn app.main:app --reload


class Post(BaseModel):  # from Pydantic
    title: str
    content: str
    published: bool = True  # default value


while True:
    try:
        # Connect to an existing database
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='chronium333',
                                cursor_factory=RealDictCursor)
        # cursor_factory thing in order to get access to column names

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as err:
        print("Database connection failed.")
        print("Error: ", err)
        time.sleep(5)

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
def root():
    return {"message": "HEELOOOOO WOOOORLD!!!!!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts; """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published)
                      VALUES (%s, %s, %s) RETURNING *; """,  # %s for data sanitization
                   (post.title, post.content, post.published))
    # Doing the same thing as with above but with f-strings makes you vulnerable to SQL injection attacks
    # ...which is why passing data in there directly SUCKS and you should NEVER do that, since all our cool and awesome
    # SQL-Python integration libraries can do SQL sanitization for our lazy, tired and confused asses.
    new_post = cursor.fetchone()

    conn.commit()  # Because we're making a change to the database.

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):  # Issue: Internal Server Error 500 if nonexistent post id > 9
    cursor.execute("""SELECT * FROM posts WHERE id = %s; """,
                   (str(id),))
    # YT guy just said this weird comma fixes the aforementioned issue.
    # ...and well, it actually does. And they say that mathematics and quantum mechanics are
    # the "dark magic" of STEM. Naw.
    post = cursor.fetchone()
    # print(post)

    if not post:  # If post is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} was not found.")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *; """,
                   (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()  # Because we're making a change to the database.

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} does not exist.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
                      WHERE id = %s  RETURNING *; """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()  # Because we're making a change to the database.

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} does not exist.")

    return {'data': updated_post}
