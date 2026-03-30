import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制：首页高度优化版 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 基础隐藏 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 全局背景 */
    .stApp { background: #F8F9FA; color: #455A64; font-family: "PingFang SC", sans-serif; }
    
    /* 首页专用遮盖容器：优化高度与溢出 */
    .home-mask {
        padding: 25px 20px; /* 缩小内边距 */
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(26, 35, 126, 0.05);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(10px);
        margin-top: 10px;
        max-height: 85vh; /* 限制高度，防止滚动 */
        overflow: hidden; /* 禁止容器内部滚动 */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* 三行标题：压缩间距 */
    .title-l1 { font-size: 14px; color: #90A4AE; font-weight: 500; margin-bottom: 4px; }
    .title-l2 { font-size: 32px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 2px; }
    .title-l3 { font-size: 24px; font-weight: 700; color: #FF7043; margin-bottom: 15px; }
    
    /* 引导语：缩小字号与行高 */
    .intro-text {
        font-size: 16px; color: #546E7A; line-height: 1.6; margin-bottom: 20px;
        border-left: 4px solid #FF7043; padding-left: 15px;
    }
    
/* 1. 基础按钮样式：默认深蓝色 */
    div.stButton > button {
        border-radius: 12px; 
        height: 55px; 
        font-size: 18px !important; 
        font-weight: 700;
        background-color: #1A237E; 
        color: white; 
        border: none;
        transition: all 0.2s;
    }

    /* 2. 悬停状态：颜色稍微变深 */
    div.stButton > button:hover {
        background-color: #0D47A1;
        color: white;
    }

    /* 3. 关键修改：点击后及获得焦点时的状态 */
    /* 这里的 #FF7043 是你品牌色中的橙色，按下后会变成橙色且不再跳回蓝色 */
    div.stButton > button:focus, 
    div.stButton > button:active {
        background-color: #FF7043 !important; 
        color: white !important;
        box-shadow: 0 0 0 0.2rem rgba(255, 112, 67, 0.5) !important;
        outline: none !important;
    }
    
    /* 结果页与其他样式 */
    .q-text { font-size: 20px; font-weight: 600; color: #263238; margin: 25px 0; }
    .warn-banner { padding: 18px; border-radius: 14px; margin-bottom: 15px; color: white; font-weight: 600; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    .res-card { padding: 18px; border-radius: 12px; background: white; border-left: 6px solid #1A237E; margin-bottom: 12px; }
    .wx-card { background: #FFFFFF; padding: 25px; border-radius: 20px; border: 1px solid #E8EAF6; box-shadow: 0 8px 30px rgba(26,35,126,0.1); text-align: center; }
    .rid-box { font-size: 36px; font-weight: 900; color: #C62828; border: 2px dashed #C62828; padding: 5px 20px; margin: 15px 0; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({
        'step': 'home', 
        'cur': 0, 
        'ans': {}, 
        'rid': str(random.randint(100000, 999999))
    })
    # --- 3. 全量题库 (1-85题) ---
# 自动生成 85 个占位题目（实际使用时请替换为您的具体文本）
if 'QUESTIONS' not in locals():
    QUESTIONS = [f"第 {i+1} 题：关于孩子在家庭中的某种行为表现或心态描述..." for i in range(85)]

# --- 4. 维度话术数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固，依恋关系安全。", "【预警】地基有裂缝，系统承压接近临界。", "【危险】地基动摇，孩子缺乏基本安全感。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛，情绪自控力强。", "【内耗】内耗严重，管教伴随生理性无力。", "【力竭】心理力竭，已丧失有效引导能力。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通畅通，边界清晰信任高。", "【防御】防御性增强，沟通仅维持功能层面。", "【断联】情感断联，孩子有明显逃离倾向。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】生机勃勃，具备天然抗挫力。", "【下行】动力开始萎缩，出现空心化苗头。", "【枯竭】动力枯竭，自我价值感降至冰点。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】脑认知高效，任务执行力强。", "【疲劳】生理性疲劳导致执行功能受损。", "【宕机】大脑保护性关闭，对学业极端抗拒。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】规则意识强，社交半径正常。", "【退缩】依赖屏幕，现实社交回避明显。", "【受损】社会功能受损，拒绝参与现实生活。"]}
}

# --- 5. 页面流程逻辑 ---

# A. 首页：优化后的紧凑版
if st.session_state.step == 'home':
    st.markdown("""
 <div class='home-mask'>
            <div class='title-l1'>曹校长 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是你的老朋友。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()

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
        if st.button("⬅ 上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果报告页
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:12px; border-radius:10px; text-align:center; margin-bottom:20px; font-size:14px;'>📸 请【截屏保存】本页结果，作为咨询凭证。</div>", unsafe_allow_html=True)
    
    # 雷达图数据处理
    scores, labels = [], list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores, theta=labels, fill='toself', 
        line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(t=20, b=20, l=40, r=40))
    st.plotly_chart(fig, use_container_width=True)

    # 预警逻辑
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到生存危机或极度情绪创伤，请立刻停止施压！</div>", unsafe_allow_html=True)
    
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】孩子表现出注意力黑洞特质，需科学干预。</div>", unsafe_allow_html=True)

    # 详细维度解析
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    # 微信转化区域
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#1A237E; font-size:18px; font-weight:bold;'>这份报告揭示了孩子的求救，<br>也看见了您的委屈。</p>
            <div style='text-align:left; margin-top:15px;'>
                <p style='margin:5px 0;'>✅ 10个维度个性化改善方案</p>
                <p style='margin:5px 0;'>✅ 30分钟 1V1 深度解析</p>
                <p style='margin:5px 0;'>✅ <b>特惠 198 元</b>（原价 598 元）</p>
            </div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='color:#546E7A; font-size:13px;'>添加微信请备注上方数字编号</p>
            <a href="https://work.weixin.qq.com/ca/your_id" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:15px; border-radius:12px; font-size:18px; font-weight:bold; margin-top:10px;">👉 添加老师预约解析</a>
        </div>
    """, unsafe_allow_html=True)
