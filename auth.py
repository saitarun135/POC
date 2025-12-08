import jwt
from fastapi import Request,HTTPException

class Auth:
    __SECRET__ = "This is a POC of FAST_API"
    __ALGORITHM__ = 'HS256'
    
    def encode_data(self, data:dict) -> str:
        encoded_str = jwt.encode(payload=data, key=Auth.__SECRET__, algorithm=Auth.__ALGORITHM__)
        return encoded_str
    
    async def id(self, request:Request) ->int | HTTPException:
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise HTTPException(status_code=401, detail="Authorization header missed.")
        elif auth_header.split(" ")[0] != "Bearer":
            raise HTTPException(status_code= 401, detail="Invalid formation of Bearer token")
        
        token:str = auth_header.split(" ")[1]
        decoded_data:dict = jwt.decode(jwt=token, algorithms=Auth.__ALGORITHM__, key=Auth.__SECRET__)
        
        return decoded_data['id']
