import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 物理级一屏视觉重构 ---
st.set_page_config(page_title="曹校长-脑科学十维探查", layout="centered")

st.markdown("""
    <style>
    /* 1. 彻底移除所有系统 UI 干扰 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 2. 首页一屏锁定逻辑：禁止滚动 + 强制居中 */
    .stApp {
        background-color: #F4F7F9;
        overflow: hidden !important; 
    }

    /* 首页专用容器：占据视口高度，Flex 居中 */
    .home-viewport {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        display: flex; align-items: center; justify-content: center;
        background: #F4F7F9;
        z-index: 100;
    }

    /* 首页一体化白色大卡片 */
    .main-card {
        background: white;
        width: 88%;
        max-width: 420px;
        padding: 40px 28px;
        border-radius: 32px;
        box-shadow: 0 20px 60px rgba(26, 35, 126, 0.1);
        border: 1px solid rgba(255,255,255,0.8);
        text-align: left;
    }

    /* 文本排版 */
    .t1 { font-size: 15px; color: #90A4AE; font-weight: 500; margin-bottom: 6px; }
    .t2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 4px; }
    .t3 { font-size: 26px; font-weight: 700; color: #FF7043; margin-bottom: 28px; }
    .intro-body { 
        font-size: 17px; color: #546E7A; line-height: 1.8; margin-bottom: 35px;
        border-left: 4px solid #FF7043; padding-left: 18px;
    }

    /* 原生按钮视觉注入：让它看起来就是卡片的一部分 */
    div.stButton > button {
        width: 100%;
        height: 64px;
        background: #1A237E !important;
        color: white !important;
        border-radius: 18px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(26,35,126,0.2) !important;
    }

    /* 答题页与结果页：解除锁定，允许滚动 */
    .scroll-mode { overflow-y: auto !important; height: auto !important; display: block !important; }
    
    /* 其他通用样式 */
    .q-text { font-size: 22px; font-weight: 600; color: #263238; margin: 30px 0; line-height: 1.5; }
    .res-card { padding: 20px; border-radius: 18px; background: white; border-left: 8px solid #1A237E; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .warn-banner { padding: 20px; border-radius: 16px; margin-bottom: 15px; color: white; font-weight: 600; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    .wx-card { background: white; padding: 30px; border-radius: 24px; border: 2px solid #E8EAF6; text-align: center; margin-top: 30px; }
    .rid-box { font-size: 42px; font-weight: 900; color: #C62828; border: 3px dashed #C62828; display: inline-block; padding: 5px 25px; margin: 20px 0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 基础题库 (测试用) ---
if 'QUESTIONS' not in locals():
    QUESTIONS = [f"在近一个月的家庭生活中，第 {i+1} 项表现是..." for i in range(85)]

# --- 4. 维度定义 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固。", "【预警】地基有裂缝。", "【危险】地基动摇。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛。", "【内耗】内耗严重。", "【力竭】心理力竭。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通顺畅。", "【防御】防御增强。", "【断联】情感断联。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】抗挫力强。", "【下行】出现下行。", "【枯竭】动力枯竭。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】脑认知高效。", "【疲劳】生理疲劳。", "【宕机】大脑保护性关闭。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】社交正常。", "【退缩】回避明显。", "【受损】功能受损。"]}
}# --- 5. 页面流程控制 ---

# A. 首页：绝对居中 + 一体化大卡片
if st.session_state.step == 'home':
    # 首页核心：利用第一部分定义的 home-viewport 和 main-card
    # 这里的逻辑是将 HTML 结构拆分，把 st.button 嵌在中间
    st.markdown('<div class="home-viewport"><div class="main-card">', unsafe_allow_html=True)
    
    # 渲染卡片内的文案
    st.markdown("""
        <div class='t1'>曹校长 脑科学专业版</div>
        <div class='t2'>家庭教育</div>
        <div class='t3'>十维深度探查表</div>
        <div class='intro-body'>
            这是一场跨越心与脑的对话。<br>
            你好，我是你的老朋友。<br><br>
            接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
            这不是一份考卷，而是给孩子一次被“看见”的机会。
        </div>
    """, unsafe_allow_html=True)
    
    # 渲染卡片内的按钮 (原生按钮会根据 CSS 自动填满卡片宽度)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    
    # 闭合所有容器标签
    st.markdown('</div></div>', unsafe_allow_html=True)

# B. 答题页：解除锁定，进入测评流程
elif st.session_state.step == 'quiz':
    # 关键：注入 CSS 恢复滚动条，让 stApp 回复正常显示
    st.markdown("<style>.stApp { overflow-y: auto !important; display: block !important; }</style>", unsafe_allow_html=True)
    
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.caption(f"当前进度：{cur + 1} / 85 题")
    
    # 题目内容
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    # 选项布局：两列长条按钮
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
    
    # 辅助功能
    if cur > 0:
        st.write("---")
        if st.button("⬅ 返回上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页：深度多维分析报告
elif st.session_state.step == 'report':
    st.markdown("<style>.stApp { overflow-y: auto !important; display: block !important; }</style>", unsafe_allow_html=True)
    
    # 1. 顶部提示
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    # 2. 雷达图可视化
    scores = []
    labels = list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores, theta=labels, fill='toself', 
        line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # 3. 三大红灯预警
    # 情绪危机 (59-66)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到孩子目前存在明显的生存危机或极度情绪创伤。请立刻停止施压，确保生命安全！</div>", unsafe_allow_html=True)
    
    # ADHD/脑特性 (67-72)
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】孩子表现出注意力黑洞特质。这非态度问题，而是前额叶执行功能发育滞后。</div>", unsafe_allow_html=True)

    # 生理地基 (73-78)
    if (sum(st.session_state.ans.get(i, 0) for i in range(72, 78))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【生理地基预警】检测到肠脑轴失调迹象。大脑已切至“生存模式”，建议先调理生理节律。</div>", unsafe_allow_html=True)

    # 4. 详细卡片展示
    st.write("### 🔍 深度维度解析")
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    # 5. 微信转化区
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。<br>其实，您不需要独自扛着。</p>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='text-align:left; font-weight:bold; margin-top:10px; color:#1A237E;'>添加老师获得：</p>
            <div style='text-align:left; color:#1A237E; font-weight:700; margin:5px 0;'>1. 十个维度个性化改善方案</div>
            <div style='text-align:left; color:#1A237E; font-weight:700; margin:5px 0;'>2. 30 分钟 1V1 深度报告解析</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:18px; border-radius:15px; font-size:19px; font-weight:bold; margin-top:20px;">👉 点击添加老师，预约解析</a>
        </div>
    """, unsafe_allow_html=True)
    st.write("") # 底部占位
