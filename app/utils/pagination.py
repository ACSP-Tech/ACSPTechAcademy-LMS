from fastapi_pagination import Params
from typing import Annotated
from pydantic import Field


class UserParams(Params):
    """Default pagination parameters with a custom page size for all users"""
    size: Annotated[int, Field(gt=1, le=50)] = 10  # Default page size set to 10, max 50, min 1