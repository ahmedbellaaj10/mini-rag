from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from bson.objectid import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric.")
        return value

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    @classmethod
    def get_indexes(cls) -> list[dict]:
        return [
            {
                "key": [("project_id", 1)],
                "name": "project_id_index",
                "unique": True,
            }
        ]
