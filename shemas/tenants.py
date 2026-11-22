from pydantic import BaseModel, Field
from typing import Literal

class TenantShema(BaseModel):
    name: str = Field(max_length=50)
    plane_name: Literal["Free","Pro"] 
