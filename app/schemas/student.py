from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., gt=0, le=120)
    course: str = Field(..., min_length=1, max_length=100)


class StudentPatchRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, gt=0, le=120)
    course: str | None = Field(default=None, min_length=1, max_length=100)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    course: str
