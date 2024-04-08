from backend.core import run_llm
import streamlit as st
from streamlit_chat import message


st.header("Conure 🦜 a squawking good Langchain documentation assistant")

user_prompt = st.text_input(
    label="Provide a Prompt",
    placeholder="Enter your question here...",
)

if "user_prompt_history" not in st.session_state:  # initializing
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:  # initializing
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:  # initializing
    st.session_state["chat_history"] = []


# there is certainly a more succinct way to do this with Python but i'd rather just do it manually
def truncate_https(link: str) -> str:
    output = ""
    counter = 0
    char_index = 0
    while char_index < len(link) and counter < 2:
        if link[char_index] == "/":
            counter += 1
        char_index += 1

    while char_index < len(link):
        output += link[char_index]
        char_index += 1

    return output


def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {truncate_https(source)}\n"
    return sources_string


if user_prompt:
    with st.spinner("Generating Response..."):
        generated_response = run_llm(user_prompt, st.session_state["chat_history"])

        # we make the sources variable a set so that duplicate sources are not included
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        # print(generated_response)

        parsed_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(user_prompt)
        st.session_state["chat_answers_history"].append(parsed_response)
        st.session_state["chat_history"].append(
            (user_prompt, generated_response["answer"])
        )  # append a tuple

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)
