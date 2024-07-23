from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

# List of allowed origins (domains) that will be allowed to make CORS requests
origins = [
    'http://localhost',
    'http://localhost:80',
    'http://localhost:3000',
    'http://rea.development',
    'http://rea.pro',
]

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)


handler = Mangum(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
