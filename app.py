import streamlit as st
import plotly.graph_objects as go
import random

# --- 1. 视觉配置 (复刻图片要求) ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .home-lock { height: 100vh; overflow: hidden; display: flex; flex-direction: column; justify-content: center; }
    .l1 { color: #90A4AE; font-size: 16px; }
    .l2 { color: #1A237E; font-size: 38px; font-weight: 900; margin: 5px 0; }
    .l3 { color: #FF7043; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .glass-box { background: rgba(255,255,255,0.6); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; color: #37474F; line-height: 1.8; }
    .rid-box { border: 2px dashed #FF5252; padding: 15px; text-align: center; margin: 20px 0; border-radius: 8px; background-color: #FFF5F5; }
    .stButton > button { width: 100%; text-align: left !important; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心数据库 [cite: 107, 113-148] ---
if 'rid' not in st.session_state: st.session_state.rid = random.randint(100000, 999999)
if 'step' not in st.session_state: st.session_state.step = "HOME"
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'current_q' not in st.session_state: st.session_state.current_q = 1

# 维度文案库
TEXTS = {
    "系统": {
        "low": "地基稳固。孩子安全感足，解决表层问题见效极快 [cite: 114]。",
        "mid": "存在内耗。教育标准不一，孩子像在逆风航行，走得很累 [cite: 115]。",
        "high": "结构动荡。孩子像在地震带盖房子，能量全用来维稳了 [cite: 116]。"
    },
    "家长": {
        "low": "心态高能。您是稳固后盾，目前只需一把精准的手术刀 [cite: 118]。",
        "mid": "身心疲劳。处于育儿倦怠边缘，这种坚持带有自我牺牲感 [cite: 119]。",
        "high": "能量力竭。油箱已干，您的焦灼正通过神经元传染给孩子 [cite: 120]。"
    },
    "关系": {
        "low": "沟通顺畅。孩子还愿说真心话，任何技术手段都能100%见效 [cite: 122]。",
        "mid": "情感疏离。缺乏深链接，孩子正慢慢关上心门 [cite: 123]。",
        "high": "信号屏蔽。您说的每句‘为他好’，在他听来都是攻击 [cite: 124]。"
    },
    "动力": {
        "low": "核心自驱。骨子里有胜负欲，只需重装系统即可跑起来 [cite: 126]。",
        "mid": "生命摇摆。推一下动一下，初高中阶段极易彻底熄火 [cite: 127]。",
        "high": "生命空心。已进入节能模式，对外界失去探索欲 [cite: 128]。"
    },
    "学业": {
        "low": "硬件优秀。执行功能没问题，成绩波动只是小感冒 [cite: 130]。",
        "mid": "高代偿维持。用双倍意志力弥补脑效率不足，极易崩盘 [cite: 131]。",
        "high": "CPU过载。写字消耗能量是别人三倍，必须科学降载 [cite: 132]。"
    },
    "社会化": {
        "low": "合群自信。渴望链接，这是拉回现实的最强抓手 [cite: 134]。",
        "mid": "社交依赖。电子世界吸引力正盖过现实，能力持续退化 [cite: 135]。",
        "high": "现实退缩。在学校找不到成就感，只能去虚拟世界吸氧 [cite: 136]。"
    }
}

# --- 3. 页面渲染 ---
if st.session_state.step == "HOME":
    st.markdown('<div class="home-lock"><div class="l1">曹校长 脑科学专业版</div><div class="l2">家庭教育</div><div class="l3">十维深度探查表</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-box">这是一场跨越心与脑的对话。<br>你好，我是曹校长。<br><br>请放下焦虑，这不是一份考卷，而是给孩子和你自己一次被“看见”的机会 [cite: 151-154]。</div>', unsafe_allow_html=True)
    if st.button("👉 开始测评"): st.session_state.step = "QUIZ"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "QUIZ":
    # 题目逻辑 (参考前一版，确保引号已修复)
    idx = st.session_state.current_q
    if idx <= 78:
        st.write(f"进度：{idx} / 85")
        # 简化题目显示（实际请填入QUESTIONS列表）
        st.subheader(f"第 {idx} 题内容...") 
        for i, lbl in enumerate(["从不", "偶尔", "经常", "总是"]):
            if st.button(lbl, key=f"q{idx}_{i}"):
                st.session_state.answers[idx] = i
                st.session_state.current_q += 1
                st.rerun()
    else:
        if st.button("生成深度报告"): st.session_state.step = "RESULT"; st.rerun()

elif st.session_state.step == "RESULT":
    st.markdown("### 📸 您的深度诊断报告")
    ans = st.session_state.answers
    
    # 维度计分与话术匹配
    def get_level(s, e):
        score = sum(ans.get(i, 0) for i in range(s, e+1)) / (e - s + 1)
        if score <= 0.8: return "low", score
        if score <= 1.8: return "mid", score
        return "high", score

    # 绘制雷达图 (省略细节，逻辑同前)
    
    # 1-6维度话术展示 
    st.divider()
    res_summary = []
    for name, (s, e) in {"系统":(1,8), "家长":(9,18), "关系":(19,28), "动力":(29,37), "学业":(38,48), "社会化":(49,58)}.items():
        lv, sc = get_level(s, e)
        st.markdown(f"**【{name}】**: {TEXTS[name][lv]}")
        if lv == "high": res_summary.append(name)

    # 7-9专项预警 [cite: 140-148]
    st.divider()
    st.subheader("⚠️ 风险专项预警")
    if any(ans.get(i,0) == 3 for i in range(59,67)):
        st.error("🔴 红灯：孩子情绪安全水位极低，建议暂停学业施压 ！")
    if sum(ans.get(i,0) for i in range(67,73))/6 > 1.5:
        st.warning("🟠 预警：高度疑似ADHD特质，孩子需要脑功能整合训练而非指责 [cite: 145]。")
    if sum(ans.get(i,0) for i in range(73,78))/6 > 1.5:
        st.info("🔵 提醒：表现出的易激惹受生理代谢影响，建议从营养与律动修复 [cite: 147]。")

    # 动态微信转化区 (根据最严重维度生成)
    focus_topic = res_summary[0] if res_summary else "家庭系统"
    st.markdown(f"""
        <div style="border: 2px solid #1A237E; padding: 20px; border-radius: 15px; background: #F8F9FA;">
            <p style='font-size: 18px; color: #D32F2F;'><b>曹校长特别建议：</b></p>
            <p>基于数据，您孩子的<b> {focus_topic} </b>维度风险最高。这不是靠讲道理能解决的，必须切入底层脑科学方案。</p>
            <div class="rid-box">
                <span style="font-size: 28px; font-weight: 900; color: #D32F2F; letter-spacing: 5px;">{st.session_state.rid}</span><br>
                <small>请截屏保存，添加微信时备注此编号</small>
            </div>
            <div style="background-color: #1A237E; color: white; text-align: center; padding: 15px; border-radius: 10px; font-weight: bold;">
                👉 添加曹校长，获取【{focus_topic}】专项改善方案
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。")
