from typing import Optional
from bson import ObjectId

from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DatabaseEnums import DatabaseEnum


class AssetModel(BaseDataModel):
    def __init__(self, db_client: object) -> None:
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object) -> "AssetModel":
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self) -> None:
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DatabaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_asset(self, asset: Asset) -> Asset:
        result = await self.collection.insert_one(
            asset.model_dump(by_alias=True, exclude={"id"})
        )
        asset.id = result.inserted_id

        return asset

    async def get_all_project_assets(
        self, asset_project_id: str, asset_type: str = "file"
    ) -> list[Asset]:
        assets = await self.collection.find(
            {
                "asset_project_id": ObjectId(asset_project_id)
                if isinstance(asset_project_id, str)
                else asset_project_id,
                "asset_type": asset_type,
            }
        ).to_list(length=None)
        return [Asset(**asset) for asset in assets]

    async def get_asset_record(
        self, asset_project_id: str, asset_name: str
    ) -> Optional[Asset]:
        asset = await self.collection.find_one(
            {
                "asset_project_id": ObjectId(asset_project_id)
                if isinstance(asset_project_id, str)
                else asset_project_id,
                "asset_name": asset_name,
            }
        )
        if asset:
            return Asset(**asset)
        return None
