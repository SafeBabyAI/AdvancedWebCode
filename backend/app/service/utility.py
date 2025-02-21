from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#hash_password() → 비밀번호를 bcrypt 해싱해서 저장
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
#verify_password() → 입력한 비밀번호가 해시된 값과 일치하는지 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)