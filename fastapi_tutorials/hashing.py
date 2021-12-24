from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    # plain_password is the request body password and hashed_password means db password which is hashed already.
    return pwd_context.verify(plain_password, hashed_password)

