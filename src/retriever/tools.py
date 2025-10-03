from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

def setup_retriever():
    """Set up and return a retriever tool for web documents."""
    # Load documents from a web page
    urls = [
        "https://scoras.com.br/academy/",
        "https://scoras.com.br/"
    ]

    # Load the documents from each URL

    docs = [WebBaseLoader(url).load() for url in urls]

    print(docs[0][0].metadata)

    return docs


setup_retriever()