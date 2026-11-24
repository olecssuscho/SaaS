from pydantic import BaseModel, Field

class TenantShema(BaseModel):
    model_config = {"extra":"forbid"}
    name: str = Field(max_length=50)
