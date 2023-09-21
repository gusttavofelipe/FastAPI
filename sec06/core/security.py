from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, hash_password: str) -> bool:
    '''
    funcao para verificar se a password esta correto, comparando
    o password em texto puro informado pelo usuario, e pelo hash
    da password que foi salvo no banco de dados durante a criacao da conta
    '''
    return CRYPTO.verify(password, hash_password)

def generate_password_hash(password: str) -> str:
    '''
    funcao que gera e retorna o hash da password
    '''
    return CRYPTO.verify(password)
