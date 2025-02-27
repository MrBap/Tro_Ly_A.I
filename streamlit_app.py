import streamlit as st
from openai import OpenAI
import os

# Hàm đọc nội dung từ file văn bản
def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# Hiển thị logo (nếu có)
try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
except:
    pass

# Hiển thị tiêu đề
title_content = rfile("00.xinchao.txt")
st.markdown(
    f"""<h1 style="text-align: center; font-size: 24px;">{title_content}</h1>""",
    unsafe_allow_html=True
)

# Lấy OpenAI API key từ st.secrets
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# Khởi tạo OpenAI client
client = OpenAI(api_key=openai_api_key)

# Khởi tạo tin nhắn "system" và "assistant"
INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

# Kiểm tra nếu chưa có session lưu trữ thì khởi tạo tin nhắn ban đầu
if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# CSS để căn chỉnh trợ lý bên trái, người hỏi bên phải, và thêm icon trợ lý
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

# Hiển thị lịch sử tin nhắn
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="assistant">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "user":
        st.markdown(f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True)

# Tạo nút ghi âm và JavaScript để nhận diện giọng nói
st.markdown(
    """
    <script>
    function startDictation() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = "vi-VN";
        recognition.onresult = function(event) {
            document.getElementById("chat_input").value = event.results[0][0].transcript;
        };
        recognition.start();
    }
    </script>
    <button onclick="startDictation()">🎙️ Ghi âm</button>
    """,
    unsafe_allow_html=True
)

# Ô nhập liệu cho người dùng
if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

    # Tạo phản hồi từ API OpenAI
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
