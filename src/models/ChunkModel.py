from typing import Optional
from bson import ObjectId

from pymongo import InsertOne

from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DatabaseEnums import DatabaseEnum


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object) -> None:
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk) -> DataChunk:
        result = await self.collection.insert_one(
            chunk.model_dump(by_alias=True, exclude={"id"})
        )
        chunk.id = result.inserted_id

        return chunk

    async def get_chunk(self, chunk_id: str) -> Optional[DataChunk]:
        chunk = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if chunk:
            return DataChunk(**chunk)
        else:
            return None

    async def insert_many_chunks(
        self, chunks: list[DataChunk], batch_size: int = 100
    ) -> int:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude={"id"}))
                for chunk in batch
            ]
        result = await self.collection.bulk_write(operations)
        return result.inserted_count

    async def delete_chunks_by_project_id(self, project_id: ObjectId) -> int:
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count
