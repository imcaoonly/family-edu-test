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
    
    /* 首页卡片居中锁定逻辑 */
    .home-mask {
        position: fixed; /* 锁定在屏幕视口 */
        top: 45%;        /* 竖直方向居中（45%比50%视觉感更好） */
        left: 50%;
        transform: translate(-50%, -50%); /* 完美的绝对居中 */
        width: 90%;
        max-width: 550px;
        padding: 40px 25px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        box-shadow: 0 15px 45px rgba(26, 35, 126, 0.12);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(12px);
        z-index: 9999;
    }
    
    /* 首页按钮间距优化：让按钮贴合卡片内容 */
    .home-btn-fix {
        margin-top: -15px !important;
    }
    
    /* 标题规范 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 30px; border-left: 5px solid #FF7043; padding-left: 20px; }
    
    /* 通用按钮样式 */
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #0D47A1; }
    
    /* 结果页警报、卡片等样式保持不变 */
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

# --- 3. 全量题库 (1-85题) ---
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
# --- 5. 页面流程 ---

# A. 首页 (卡片与按钮整体绝对居中)
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
    """, unsafe_allow_html=True)
    
    # 将按钮放入 mask 内部 div，确保它们作为一个整体在屏幕中心
    st.markdown("<div class='home-btn-fix'>", unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
    cols = st.columns(2)
    for i, (txt, val) in enumerate(opts):
        with (cols[0] if i % 2 == 0 else cols[1]):
            if st.button(txt, key=f"q_{cur}_{i}", use_container_width=True):
                st.session_state.ans[cur] = val
                if cur == 84: 
                    st.session_state.step = 'report'
                else: 
                    st.session_state.cur += 1
                st.rerun()
    
    if cur > 0:
        st.write("")
        if st.button("⬅ 回到上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    scores = []
    labels = list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # 预警警报
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到生存危机。请立刻停止施压！</div>", unsafe_allow_html=True)
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】孩子表现出注意力黑洞特质。</div>", unsafe_allow_html=True)

    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div class='benefit'>1. 十个维度个性化改善方案</div>
            <div class='benefit'>2. 30 分钟 1V1 深度解析</div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold;">👉 点击添加老师，预约 1V1 解析</a>
        </div>
    """, unsafe_allow_html=True)
