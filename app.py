import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底遮蔽原网站品牌 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 全局样式 */
    .stApp { background: #F8F9FA; text-align: left !important; color: #455A64; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
    
    /* 首页整体容器：实现整体竖直居中 */
    .home-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 80vh; /* 占据视口高度，实现居中感 */
        padding-bottom: 5vh; /* 整体稍微向上提一点 */
    }

    /* 首页卡片 */
    .home-mask {
        width: 100%;
        max-width: 550px;
        padding: 40px 25px 30px 25px; /* 底部留出一点内边距给按钮 */
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        box-shadow: 0 15px 45px rgba(26, 35, 126, 0.12);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(12px);
    }
    
    /* 三行标题规范 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }
    
    /* 引导语 */
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 30px; border-left: 5px solid #FF7043; padding-left: 20px; }
    
    /* 按钮基础样式 */
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #0D47A1; transform: translateY(-2px); }

    /* 结果页及其他样式保持不变 */
    .warn-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; text-align: left; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    .res-card { padding: 20px; border-radius: 15px; background: white; border: 1px solid #E0E0E0; border-left: 8px solid #1A237E; margin-bottom: 15px; }
    .wx-card { background: #FFFFFF; padding: 30px; border-radius: 24px; border: 2px solid #E8EAF6; box-shadow: 0 12px 40px rgba(26,35,126,0.15); text-align: center; margin-top: 40px; }
    .benefit { font-size: 17px; font-weight: 700; color: #1A237E; margin: 12px 0; text-align: left; padding-left: 15px; }
    .rid-box { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 10px 30px; border-radius: 12px; border: 3px dashed #C62828; display: inline-block; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 全量题库 ---
if 'QUESTIONS' not in locals():
    QUESTIONS = [f"这里是第 {i+1} 题的具体描述内容..." for i in range(85)]

# --- 4. 维度数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固。", "【预警】地基有裂缝。", "【危险】地基动摇。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛。", "【内耗】内耗严重。", "【力竭】心理力竭。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通畅通。", "【防御】防御增强。", "【断联】情感断联。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】生机勃勃。", "【下行】动力萎缩。", "【枯竭】动力枯竭。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】执行力强。", "【疲劳】功能受损。", "【宕机】极端抗拒。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】社交正常。", "【退缩】回避明显。", "【受损】功能受损。"]}
}
import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底遮蔽原网站品牌 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 全局样式 */
    .stApp { background: #F8F9FA; text-align: left !important; color: #455A64; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
    
    /* 首页整体容器：实现整体竖直居中 */
    .home-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 80vh; /* 占据视口高度，实现居中感 */
        padding-bottom: 5vh; /* 整体稍微向上提一点 */
    }

    /* 首页卡片 */
    .home-mask {
        width: 100%;
        max-width: 550px;
        padding: 40px 25px 30px 25px; /* 底部留出一点内边距给按钮 */
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        box-shadow: 0 15px 45px rgba(26, 35, 126, 0.12);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(12px);
    }
    
    /* 三行标题规范 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }
    
    /* 引导语 */
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 30px; border-left: 5px solid #FF7043; padding-left: 20px; }
    
    /* 按钮基础样式 */
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #0D47A1; transform: translateY(-2px); }

    /* 结果页及其他样式保持不变 */
    .warn-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; text-align: left; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    .res-card { padding: 20px; border-radius: 15px; background: white; border: 1px solid #E0E0E0; border-left: 8px solid #1A237E; margin-bottom: 15px; }
    .wx-card { background: #FFFFFF; padding: 30px; border-radius: 24px; border: 2px solid #E8EAF6; box-shadow: 0 12px 40px rgba(26,35,126,0.15); text-align: center; margin-top: 40px; }
    .benefit { font-size: 17px; font-weight: 700; color: #1A237E; margin: 12px 0; text-align: left; padding-left: 15px; }
    .rid-box { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 10px 30px; border-radius: 12px; border: 3px dashed #C62828; display: inline-block; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 全量题库 ---
if 'QUESTIONS' not in locals():
    QUESTIONS = [f"这里是第 {i+1} 题的具体描述内容..." for i in range(85)]

# --- 4. 维度数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固。", "【预警】地基有裂缝。", "【危险】地基动摇。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛。", "【内耗】内耗严重。", "【力竭】心理力竭。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通畅通。", "【防御】防御增强。", "【断联】情感断联。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】生机勃勃。", "【下行】动力萎缩。", "【枯竭】动力枯竭。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】执行力强。", "【疲劳】功能受损。", "【宕机】极端抗拒。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】社交正常。", "【退缩】回避明显。", "【受损】功能受损。"]}
}
