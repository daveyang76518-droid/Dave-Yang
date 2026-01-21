import streamlit as st
import asyncio
import edge_tts
import tempfile

# 設定網頁標題與手機版布局
st.set_page_config(page_title="魔法故事屋", page_icon="🌙", layout="centered")

# 使用 CSS 讓手機版介面更美觀
st.markdown("""
    <style>
    .main { text-align: center; }
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

# 簡易設定（收納在摺疊選單中）
with st.expander("🛠️ 調整聲音設定"):
    speed = st.select_slider("語速 (越右邊越輕快)", options=["-20%", "-10%", "0%", "+10%", "+20%", "+30%"], value="+10%")
    pitch = st.select_slider("甜美度 (越右邊越高音)", options=["-10%", "0%", "+10%", "+20%", "+30%"], value="+15%")

# 核心朗讀邏輯
async def speak_story(text, speed, pitch):
    # 自動加強關鍵詞語氣
    keywords = ["枕頭", "電視", "魔法", "妖怪"]
    for word in keywords:
        text = text.replace(word, f"<emphasis level='strong'>{word}</emphasis>")
    
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='zh-CN'>
        <voice name='zh-CN-XiaoxiaoNeural'>
            <mstts:express-as style='cheerful' styledegree='1.8'>
                <prosody rate='{speed}' pitch='{pitch}'>{text}</prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
    
    communicate = edge_tts.Communicate(ssml, "zh-CN-XiaoxiaoNeural")
    await communicate.save(temp_path)
    return temp_path

if st.button("🪄 變出故事聲音"):
    if story_text:
        with st.spinner("魔法施展中..."):
            audio_file = asyncio.run(speak_story(story_text, speed, pitch))
            st.audio(audio_file)
            st.balloons() # 播放成功後的彩帶動畫，增加趣味性
    else:
        st.error("請輸入故事內容喔！")
