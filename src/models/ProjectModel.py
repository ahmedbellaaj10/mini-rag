import math

from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DatabaseEnums import DatabaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object) -> None:
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project) -> Project:
        result = await self.collection.insert_one(
            project.model_dump(by_alias=True, exclude={"id"})
        )
        project.id = result.inserted_id

        return project

    async def get_project_or_create_one(self, project_id: str) -> Project:
        project = await self.collection.find_one({"project_id": project_id})
        if project:
            return Project(**project)
        else:
            new_project = Project(project_id=project_id)
            return await self.create_project(new_project)

    async def get_all_projects(
        self, page: int = 1, page_size: int = 10
    ) -> tuple[list[Project], int]:
        total_documents = await self.collection.count_documents({})
        total_pages = math.ceil(total_documents // page_size)
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects: list[Project] = [Project(**doc) async for doc in cursor]
        return projects, total_pages
