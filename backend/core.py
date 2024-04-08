import os

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import Pinecone

print("hello world")


def run_llm(myQuery: str, chatHistory: list[(str, any)] = []) -> any:

    # from_existing_index ALSO takes index_name as an argument, but I'm pretty sure it'll automatically load that from my environmental variables
    docsearch = Pinecone.from_existing_index(
        embedding=OpenAIEmbeddings(), index_name=os.environ["PINECONE_INDEX_NAME"]
    )

    llm = ChatOpenAI(verbose=True, temperature=0)

    # EXPLANATION OF THE THIRD ARGUMENT BELOW:
    # a retriever is simply a wrapper around our vectorstore object which allows us to go retrieve relevant info through similarity search.
    # all vectorstore objects (even non-Pinecone ones) can become retriever objects. just use .as_retriever(), which wraps the vectorstore upon which it was called and wraps it in the retriever class
    # qa = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=docsearch.as_retriever(),
    #     return_source_documents=True,
    # )

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=docsearch.as_retriever(), return_source_documents=True
    )

    return qa(
        {"question": myQuery, "chat_history": chatHistory}
    )  # plug myQuery into our question/answer chain


# myQuery = "What is a Langchain chain?"
# print(run_llm(myQuery)["result"])
