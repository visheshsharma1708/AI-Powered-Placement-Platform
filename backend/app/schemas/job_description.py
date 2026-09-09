from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class JobDescriptionCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    company_name: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    description: str = Field(
        ...,
        min_length=20,
    )

    source: Optional[str] = Field(
        default="manual",
        max_length=50,
    )


class JobDescriptionResponse(BaseModel):
    id: int
    title: str
    company_name: Optional[str]
    description: str
    source: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    company_name: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    description: Optional[str] = Field(
        default=None,
        min_length=20,
    )

    source: Optional[str] = Field(
        default=None,
        max_length=50,
    )