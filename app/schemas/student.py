from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Full name of the student", examples=["sujith"])
    email: EmailStr = Field(
        description="unique email address of the student", examples=["sujith@gmail.com"])
    age: int = Field(..., gt=0, le=120,
                     description="age of the student", examples=[22])
    course: str = Field(..., min_length=1, max_length=100,
                        description="course enrolled by the student", examples=["MCA"])

    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "name": "sujith",
                "email": "sujith@gmail.com",
                "age": 23,
                "course": "MCA"
            }
        ]
    })


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

    model_config = ConfigDict(json_schema_extra={"examples": [
                              {"id": 1, "name": "sujith", "email": "sujith@gmail.com", "age": 23, "course": "MCA"}]})


class ErrorResponse(BaseModel):
    detail: str


class StudentDeleteResponse(BaseModel):
    message: str

    model_config = ConfigDict(json_schema_extra={"examples": [
                              {"message": "Student delete successfully"}]})
