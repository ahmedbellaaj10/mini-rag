import os
from typing import Optional

from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


from controllers.BaseController import BaseController
from controllers.ProjectController import ProjectController
from models import LoadingEnums


class ProcessFileController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)

    def get_file_extension(self, file_id: str) -> str:
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str) -> BaseLoader:
        file_extension = self.get_file_extension(file_id)
        if file_extension == LoadingEnums.TXT.value:
            return TextLoader(self.project_path / f"{file_id}", encoding="utf-8")
        elif file_extension == LoadingEnums.PDF.value:
            return PyMuPDFLoader(self.project_path / f"{file_id}")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def get_file_content(self, file_id: str) -> list[Document]:
        loader = self.get_file_loader(file_id)
        content = loader.load()
        return content

    def process_file_content(
        self,
        file_content: list[Document],
        chunk_size: Optional[int] = 100,
        overlap_size: Optional[int] = 20,
    ) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,  # customize using a lambda function if needed
        )
        file_content_texts = [page.page_content for page in file_content]
        file_content_metadata = [page.metadata for page in file_content]
        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata,
        )
        return chunks
