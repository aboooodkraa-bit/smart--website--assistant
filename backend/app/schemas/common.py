from pydantic import BaseModel, ConfigDict

class HealthResponse(BaseModel):
    status: str
    app: str
    env: str
    version: str

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
