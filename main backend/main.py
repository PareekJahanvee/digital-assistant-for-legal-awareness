from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory storage
users_db = []

# Models
class RegisterUser(BaseModel):
    name: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str


# Register API
@app.post("/auth/register")
def register(user: RegisterUser):
    # Check if email already exists
    for u in users_db:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    users_db.append({
        "name": user.name,
        "email": user.email,
        "password": user.password
    })

    return {"message": "User registered successfully"}


# Login API
@app.post("/auth/login")
def login(user: LoginUser):
    for u in users_db:
        if u["email"] == user.email and u["password"] == user.password:
            return {
                "token": "dummy-token",
                "user": {
                    "name": u["name"],
                    "email": u["email"]
                }
            }

    raise HTTPException(status_code=401, detail="Invalid email or password")
