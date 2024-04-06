# below: a tool that helps with building documentation for GitHub repos (LangChain docs are written with this)
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# from PineconeVectorStore import Pinecone as PineconeLangChain
from langchain_pinecone import Pinecone

# pc = Pinecone() <-- i don't think we're supposed to instantiate Pinecone this early (and with no arguments)


def ingest_docs() -> None:
    print("WARNING!!!!!!! EXPENSIVE OPENAI API CALL IMPENDING.")
    loader = ReadTheDocsLoader(
        path="langchain-docs/langchain-docs/api.python.langchain.com/en/latest"
    )

    raw_documents = loader.load()

    print(f"loaded {len(raw_documents)} documents!")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )

    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Raw Documents split into {len(documents)} chunks!")

    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents, embeddings, index_name="langchain-doc-index")

    print("Added to Pinecone vectorstore vectors!")
