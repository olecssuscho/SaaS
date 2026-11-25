from datetime import datetime
from pydantic import BaseModel,ConfigDict

class TenantsRESPONCES(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str
    plane_id : int
    subscription_status : int
    current_period_end : datetime | None
    created_at : datetime