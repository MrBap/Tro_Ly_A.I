import streamlit as st
from openai import OpenAI
import os

def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# Thanh menu
st.markdown(
    """
    <style>
        .menu {
            background-color: #007bff; /* Màu xanh dương */
            padding: 10px 0;
            text-align: center;
            position: fixed; /* Cố định ở đầu trang */
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000; /* Đảm bảo menu nằm trên cùng */
        }
        .menu a {
            color: white;
            text-decoration: none;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            margin: 0 20px; /* Khoảng cách giữa các mục */
            padding: 10px 15px;
            border-radius: 5px;
            transition: background-color 0.3s; /* Hiệu ứng chuyển màu */
        }
        .menu a:hover {
            background-color: #0056b3; /* Màu khi hover */
        }
    </style>
    <div class="menu">
        <a href="https://cdbp.edu.vn" target="_blank">Trang chủ</a>
        <a href="https://zalo.me/caodangbinhphuoc" target="_blank">Zalo</a>
        <a href="https://facebook.com/truongcaodangbp" target="_blank">Fanpage</a>
        <a href="https://tiktok.com/@ilovebpc1111?lang=vi-VN" target="_blank">Tiktok</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Thêm khoảng cách để nội dung không bị che bởi menu cố định
st.markdown("<div style='padding-top: 60px;'></div>", unsafe_allow_html=True)

# Hiển thị logo
try:
    col1, col2, col3 = st.columns([1, 3, 4])
    with col1:
        st.image("logo.png", width=100)
except:
    pass

# Tiêu đề
title_content = rfile("00.xinchao.txt")
st.markdown(
    f"""<h1 style="text-align: center; font-size: 36px; color: #007bff;">{title_content}</h1>""",
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
        body {
            background-color: #f8f9fa;
        }
        .assistant {
            padding: 12px;
            border-radius: 10px;
            max-width: 75%;
            background-color: #e6f3ff;
            text-align: left;
            font-family: 'Arial', sans-serif;
            border: 1px solid #007bff;
            margin-bottom: 10px;
        }
        .user {
            padding: 12px;
            border-radius: 10px;
            max-width: 75%;
            background-color: #d1e7dd;
            text-align: right;
            margin-left: auto;
            font-family: 'Arial', sans-serif;
            border: 1px solid #28a745;
            margin-bottom: 10px;
        }
        .assistant::before { content: "🤖 "; font-weight: bold; }
        .user::before { content: "👤 "; font-weight: bold; }
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
