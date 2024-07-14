from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain):
    return pwd_context.hash(plain)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def split_equal(amount,num_friends):
      if num_friends <= 0:
        raise ValueError("Number of friends must be greater than zero.")
      return amount/num_friends
       
    
 