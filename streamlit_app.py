import streamlit as st
from openai import OpenAI
import os

def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <a href="https://cdbp.edu.vn" target="_blank">Website</a> |
                <a href="https://zalo.me/caodangbinhphuoc" target="_blank">Zalo</a> |
                <a href="https://facebook.com/truongcaodangbp" target="_blank">Fanpage</a> |
                <a href="https://tiktok.com/@ilovebpc1111?lang=vi-VN" target="_blank">Tiktok</a>
            </div>
            """,
            unsafe_allow_html=True
        )
except:
    pass

title_content = rfile("00.xinchao.txt")
st.markdown(
    f"""<h1 style="text-align: center; font-size: 24px;">{title_content}</h1>""",
    unsafe_allow_html=True
)

openai_api_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

st.markdown(
    """
    <style>
        .assistant {
            padding: 10px;
            border-radius: 10px;
            max-width: 75%;
            background: none;
            text-align: left;
        }
        .user {
            padding: 10px;
            border-radius: 10px;
            max-width: 75%;
            background-color: #f0f2f5;
            text-align: right;
            margin-left: auto;
        }
        .assistant::before { content: "🤖 "; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="assistant">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "user":
        st.markdown(f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

    response = ""
    stream = client.chat.completions.create(
        model=rfile("module_chatgpt.txt").strip(),
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices:
            response += chunk.choices[0].delta.content or ""

    st.markdown(f'<div class="assistant">{response}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": response})
