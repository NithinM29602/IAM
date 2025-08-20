from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles validation errors and returns a structured JSON response.
    """
    missing_fields = []
    invalid_fields = []
    invalid_fields_value = []
    for error in exc.errors():
        if error["type"] == "missing":
            loc = error["loc"]
            if len(loc) > 1:
                missing_fields.append(loc[1])
        elif error["type"] == "extra_forbidden":
            loc = error["loc"]
            if len(loc) > 1:
                invalid_fields.append(loc[1])
        elif error["type"] == "value_error":
            loc = error["loc"]
            if len(loc) > 1:
                invalid_fields_value.append(loc[1])

    # Create a custom message
    if missing_fields:
        message = f"The following fields are missing: [{', '.join(missing_fields)}]"
    elif invalid_fields:
        message = f"The following fields are invalid: [{', '.join(invalid_fields)}]"
    elif invalid_fields_value:
        message = f"The following fields have invalid type: [{', '.join(invalid_fields_value)}]"
    else:
        message = "Invalid input."

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"error": message}),
    )