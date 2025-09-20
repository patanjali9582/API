from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

# Create FastAPI instance
app = FastAPI(title="Simple Calculator API", description="A simple calculator using FastAPI", version="1.0")

# Define Pydantic model for request body
class CalculatorRequest(BaseModel):
    a: float
    b: float
    operation: str

    @validator("operation")
    def validate_operation(cls, value):
        allowed_operations = {"add", "subtract", "multiply", "divide"}
        if value.lower() not in allowed_operations:
            raise ValueError(f"Invalid operation. Must be one of {allowed_operations}")
        return value.lower()

# POST endpoint
@app.post("/calculator")
async def calculator(request: CalculatorRequest):
    a, b, operation = request.a, request.b, request.operation

    # Perform the calculation
    try:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
            result = a / b
        else:
            raise HTTPException(status_code=400, detail="Invalid operation.")

        return {
            "a": a,
            "b": b,
            "operation": operation,
            "result": result
        }

    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
