from fastapi import FastAPI
from web import book, author

app = FastAPI()
app.include_router(book.router)
app.include_router(author.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=9000, reload=True)