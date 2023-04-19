from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, vote, auth

# Tell SQLAlchemy to run the CREATE statements to generate all the tables when it first starts up
# Mostly redundant with Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # FastAPI instance to call in uvicorn in order to start a server

# origins = [
#     "https://www.google.com"
# ]
# For public API:
# origins = ["*"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while True:
#     try:
#         # Connect to an existing database
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='chronium333',
#                                 cursor_factory=RealDictCursor)
#         # cursor_factory thing in order to get access to column names
#
#         # Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as err:
#         print("Database connection failed.")
#         print("Error: ", err)
#         time.sleep(5)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)


@app.get("/")  # Decorator that turns root() into an API path operation
def root():
    return {"message": "HEELOOOOO WOOOORLD!!!!!!"}
