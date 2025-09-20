from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr
from typing import List

# Initialize FastAPI
app = FastAPI(title="User Registration API", description="API to register users with validation", version="1.0")

# In-memory storage for registered users
registered_users = []

# Pydantic model for user registration
class UserRegistration(BaseModel):
    username: str
    email: EmailStr               # Ensures proper email format
    password: constr(min_length=8)  # Ensures password is at least 8 characters long

# Response model (for returning user info without password)
class UserResponse(BaseModel):
    username: str
    email: EmailStr

# POST endpoint to register a new user
@app.post("/register", response_model=UserResponse)
async def register_user(user: UserRegistration):
    # Check if email is already registered
    for existing_user in registered_users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    # Store user in memory
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": user.password  # In real-world apps, never store passwords as plain text
    }
    registered_users.append(user_data)

    return {"username": user.username, "email": user.email}

# GET endpoint to fetch all registered users (without passwords)
@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return [{"username": u["username"], "email": u["email"]} for u in registered_users]
