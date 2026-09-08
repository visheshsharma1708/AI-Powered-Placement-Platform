from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class StudentProfileBase(BaseModel):
    university: str | None = Field(
        default=None,
        max_length=255,
    )

    degree: str | None = Field(
        default=None,
        max_length=255,
    )

    branch: str | None = Field(
        default=None,
        max_length=255,
    )

    graduation_year: int | None = Field(
        default=None,
        ge=2000,
        le=2100,
    )

    target_role: str | None = Field(
        default=None,
        max_length=255,
    )

    github_url: HttpUrl | None = None

    linkedin_url: HttpUrl | None = None

    portfolio_url: HttpUrl | None = None

    bio: str | None = Field(
        default=None,
        max_length=2000,
    )


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(StudentProfileBase):
    pass


class StudentProfileResponse(StudentProfileBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    user_id: int