import time

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # FastAPI instance to call in uvicorn in order to start a server


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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post)#.all()
    print(posts)

#   return {"data": posts}
    return {"data": "successful"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(**post.dict())  # Unpacking the dictionary with **
    new_post = models.Post(**post.dict())  # Does the same exact thing as below, it's just a shortcut
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # RETURNING *

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):  # Issue: Internal Server Error 500 if nonexistent post id > 9
    post = db.query(models.Post).filter(models.Post.id == id).first()  # filter() is WHERE
    # Using .all() on it is a waste of resources bc it'll keep looking for more after finding the matching post.

    if not post:  # If post is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} was not found.")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} does not exist.")
    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the ID {id} does not exist.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    # post_query.update({'title': 'check out new title awesome :gorilla:', 'content': 'bbbbbbbbbbbbbbbbb'},
    #                   synchronize_session=False)

    db.commit()

    return {'data': post_query.first()}
