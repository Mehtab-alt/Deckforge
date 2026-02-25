import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

class CorporateMemory:
    def __init__(self):
        self.vector_db = None

    def initialize(self, path="knowledge_base"):
        if not os.path.exists(path): os.makedirs(path)
        loaders = [
            DirectoryLoader(path, glob="**/*.md", loader_cls=TextLoader),
            DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        ]
        docs = []
        for l in loaders: docs.extend(l.load())
        if docs:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            self.vector_db = Chroma.from_documents(
                documents=splitter.split_documents(docs),
                embedding=OpenAIEmbeddings()
            )

    def retrieve(self, query: str) -> str:
        if not self.vector_db: return "No specific policies found."
        docs = self.vector_db.similarity_search(query, k=2)
        return "\n".join([d.page_content for d in docs])

memory = CorporateMemory()