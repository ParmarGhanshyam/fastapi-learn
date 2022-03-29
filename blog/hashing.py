from passlib.context import CryptContext

# from blog.hashing import

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(hashed_password, plan_password):
        return pwd_context.verify(plan_password,hashed_password)
