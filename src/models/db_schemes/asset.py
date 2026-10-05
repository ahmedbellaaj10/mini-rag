from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from bson.objectid import ObjectId
from datetime import datetime, timezone


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id: ObjectId = Field(...)
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: Optional[int] = Field(ge=0, default=None)
    asset_pushed_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    asset_config: Optional[dict] = Field(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    @classmethod
    def get_indexes(cls) -> list[dict]:
        return [
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_index",
                "unique": False,
            },
            {
                "key": [("asset_project_id", 1), ("asset_name", 1)],
                "name": "asset_project_id_name_index",
                "unique": True,
            },
        ]
