import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

# --- 1. UI 深度定制：还原遮罩感与左对齐规范 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* 核心背景遮罩效果 */
    .stApp {
        background: linear-gradient(135deg, #F8F9FA 0%, #ECEFF1 100%);
        text-align: left !important;
        color: #455A64;
    }
    
    /* 首页专用遮盖容器 */
    .home-mask {
        padding: 40px 20px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
        margin-top: 20px;
    }
    
    /* 三行标题规范 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #37474F; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #2E7D32; margin-bottom: 25px; }
    
    /* 老友感引导语：左对齐，带呼吸感 */
    .intro-text {
        font-size: 18px;
        color: #546E7A;
        line-height: 1.8;
        margin-bottom: 35px;
        border-left: 5px solid #A5D6A7;
        padding-left: 20px;
    }
    
    /* 结果页报警 Banner */
    .warning-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; line-height: 1.6; }
    .bg-red { background: #D32F2F; box-shadow: 0 4px 12px rgba(211,47,47,0.3); }
    .bg-orange { background: #EF6C00; box-shadow: 0 4px 12px rgba(239,108,0,0.3); }
    .bg-blue { background: #1565C0; box-shadow: 0 4px 12px rgba(21,101,192,0.3); }

    /* 按钮：保持大圆角与点击反馈 */
    div.stButton > button {
        border-radius: 12px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #2E7D32; color: white; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #1B5E20; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 逻辑管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 页面渲染 ---

# A. 首页：还原遮盖与老友话术
if st.session_state.step == 'home':
    st.markdown("""
        <div class='home-mask'>
            <div class='title-l1'>HelloADHDer 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是你的老朋友。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不仅是一份考卷，更是给孩子和你自己一次被“看见”的机会。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("") # 留白
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'; st.rerun()

# B. 结果页：还原三大核心预警话术
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#D32F2F; font-weight:bold; background:#FFEBEE; padding:12px; border-radius:10px; text-align:center; margin-bottom:20px; border:1px solid #FFCDD2;'>📸 提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。</div>", unsafe_allow_html=True)
    
    # [此处插入雷达图 Plotly 代码]

    # --- 三大维度原版话术还原 ---
    
    # 维度一：情绪红灯 (59-66题)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("""<div class='warning-banner bg-red'>
            ⚠️ 【最高级别红色警报】<br>
            监测到孩子目前存在明显的生存危机或极度情绪创伤（如厌世念头、自伤、极度冷漠）。<br>
            此时任何关于学习的督促都是在“火上饺油”。请务必立刻停止施压，寻求专业心理干预，确保生命安全是当前家庭的第一要务！
        </div>""", unsafe_allow_html=True)

    # 维度二：ADHD 脑特性 (67-72题)
    adhd_score = sum(st.session_state.ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_score >= 1.5:
        st.markdown("""<div class='warning-banner bg-orange'>
            ⚠️ 【脑特性深度预警】<br>
            孩子表现出典型的高多动、冲动或注意力黑洞特质。这并非“态度不端正”，而是前额叶皮质执行功能发育的暂时性滞后。<br>
            单纯的说教和惩罚只会破坏自尊，建议采用脑科学感统律动结合的行为管理方案进行“弯道超车”。
        </div>""", unsafe_allow_html=True)

    # 维度三：底层生理基础 (73-78题)
    bio_score = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_score >= 1.5:
        st.markdown("""<div class='warning-banner bg-blue'>
            ⚠️ 【底层生理地基预警】<br>
            监测到孩子伴有明显的肠脑轴失调或慢性生理压力迹象（如长期过敏、睡眠呼吸障碍、眼圈发青、情绪易炸）。<br>
            当身体处于慢性炎症或缺氧状态时，大脑会自动切换到“生存模式”而非“学习模式”。建议先进行生理节律的系统调理。
        </div>""", unsafe_allow_html=True)

    # --- 底部转化区 ---
    st.markdown(f"""
        <div style='background:#E8F5E9; padding:30px; border-radius:24px; text-align:center; border:1px solid #C8E6C9; margin-top:30px;'>
            <p style='color:#1B5E20; font-size:18px; font-weight:600;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div style='font-size:42px; font-weight:900; color:#D32F2F; background:#FFF; padding:15px; border-radius:15px; border:3px dashed #D32F2F; display:inline-block; margin:20px 0;'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#2E7D32; color:white; padding:20px; border-radius:15px; font-size:22px; font-weight:bold;">👉 点击添加老师，领取方案
