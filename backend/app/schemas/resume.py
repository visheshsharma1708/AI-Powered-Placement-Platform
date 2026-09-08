from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_size: int
    version: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)