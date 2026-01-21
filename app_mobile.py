import streamlit as st
import asyncio
import edge_tts
import tempfile
import os

# 設定網頁標題
st.set_page_config(page_title="魔法故事屋", page_icon="🌙")

# 手機版美化介面
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        border-radius: 30px;
        background-color: #FFB6C1;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌟 魔法故事屋")
st.write("適合 3-5 歲的甜美大姐姐朗讀")

# 故事輸入區域
default_text = "小乖抱著枕頭，電視突然發出魔法光芒，出現了一個可愛的小妖怪！"
story_text = st.text_area("在這裡輸入或貼上故事：", value=default_text, height=200)

# 語音設定
with st.expander("🛠️ 調整聲音設定"):
    # 設定語速與音高
    speed = st.select_slider("朗讀速度 (越右邊越輕快)", options=["-10%", "0%", "+10%", "+20%", "+30%"], value="+10%")
    pitch = st.select_slider("甜美度 (越右邊越高音)", options=["-10%", "0%", "+10%", "+20%", "+30%"], value="+15%")

async def speak_story(text, speed, pitch):
    # 使用 Xiaoxiao 曉曉這款最甜美的聲音
    voice = "zh-CN-XiaoxiaoNeural"
    
    # 建立暫存檔
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
    
    # 直接使用參數，不使用 SSML 標籤，避免唸出程式碼
    communicate = edge_tts.Communicate(text, voice, rate=speed, pitch=pitch)
    await communicate.save(temp_path)
    return temp_path

if st.button("🪄 變出故事聲音"):
    if story_text.strip():
        with st.spinner("魔法施展中..."):
            try:
                # 執行語音合成
                audio_file = asyncio.run(speak_story(story_text, speed, pitch))
                # 播放音訊
                st.audio(audio_file)
                st.balloons()
            except Exception as e:
                st.error(f"抱歉，魔法失效了：{e}")
    else:
        st.error("請輸入故事內容喔！")

st.info("💡 提示：現在只會唸出你輸入的故事內容囉！")


