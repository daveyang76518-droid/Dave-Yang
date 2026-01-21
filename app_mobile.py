import streamlit as st
import asyncio
import edge_tts
import tempfile
import os

# 1. 網頁基本設定
st.set_page_config(page_title="魔法故事屋", page_icon="🌙")

# 2. 手機版介面優化
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

# 3. 故事輸入區域
default_text = "小乖抱著枕頭，電視突然發出魔法光芒，出現了一個可愛的小妖怪！"
story_text = st.text_area("在這裡輸入或貼上故事：", value=default_text, height=200)

# 4. 聲音設定 (已修正選項不匹配的問題)
with st.expander("🛠️ 調整聲音設定"):
    # 這裡的 value 必須要在 options 清單裡面
    speed = st.select_slider("朗讀速度 (越右邊越輕快)", options=["-10%", "0%", "+10%", "+20%", "+30%"], value="+10%")
    pitch = st.select_slider("甜美度 (越右邊越高音)", options=["-10%", "0%", "+10%", "+20%", "+30%"], value="+20%")

async def speak_story(text, speed, pitch):
    # 使用 Xiaoxiao 曉曉這款最甜美的聲音
    voice = "zh-CN-XiaoxiaoNeural"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
    
    # 這裡直接傳入純文字，保證不唸出 <speak> 等標籤
    communicate = edge_tts.Communicate(text, voice, rate=speed, pitch=pitch)
    await communicate.save(temp_path)
    return temp_path

# 5. 執行按鈕
if st.button("🪄 變出故事聲音"):
    if story_text.strip():
        with st.spinner("魔法施展中..."):
            try:
                # 執行異步語音合成
                audio_file = asyncio.run(speak_story(story_text, speed, pitch))
                # 播放音軌
                st.audio(audio_file)
                st.balloons()
            except Exception as e:
                st.error(f"抱歉，魔法失效了：{e}")
    else:
        st.error("請輸入故事內容喔！")

st.info("💡 提示：更新後請點擊右下角 Manage app -> Reboot app 確保設定生效。")


