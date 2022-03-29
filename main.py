from fastapi import FastAPI
from blog.database import engine, Base
from blog.routers import blog, user, authentication

app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=9000, log_level="debug")
