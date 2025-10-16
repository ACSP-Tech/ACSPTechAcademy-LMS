from pydantic import BaseModel, ConfigDict

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def normalize(value):
    return value if value not in ("", None) else None