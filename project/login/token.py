import jwt
import sys
sys.path.append('/home/roopesh/Desktop/project/programs-fellowship/project')
from project.settings import SECRET_KEY

def generate_token(data):
    
    token = jwt.encode(data,SECRET_KEY, algorithm='HS256')
    return str(token)[2:-1]

def decode_token(token):
    
    data = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
    return data 
#decode_token(generate_token('a','bccd'))