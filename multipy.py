from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

# Create FastAPI instance
app = FastAPI(title="Multiply API", description="API to multiply two integers")

# Pydantic model for request validation
class MultiplyRequest(BaseModel):
    a: int
    b: int

    @validator("a", "b")
    def check_integer(cls, value):
        if not isinstance(value, int):
            raise ValueError("Both 'a' and 'b' must be integers.")
        return value

# POST endpoint to multiply two numbers
@app.post("/multiply")
async def multiply_numbers(request: MultiplyRequest):
    try:
        result = request.a * request.b
        return {"a": request.a, "b": request.b, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
