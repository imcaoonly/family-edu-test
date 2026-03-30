import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制：实现物理级一屏锁定 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底隐藏系统残留 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 核心：强制一屏锁定，禁止滚动 */
    .stApp { 
        background: #F8F9FA; 
        height: 100vh; 
        overflow: hidden !important; 
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 限制主容器宽度并居中 */
    [data-testid="stMainView"] > div {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    /* 首页卡片容器：确保高度自适应但不溢出 */
    .home-card-body {
        background: white;
        padding: 35px 25px;
        border-radius: 28px;
        box-shadow: 0 15px 45px rgba(26, 35, 126, 0.12);
        border: 1px solid rgba(255,255,255,0.7);
        max-width: 420px;
        width: 100%;
        margin: auto;
    }

    /* 标题与文案规范 */
    .title-l1 { font-size: 14px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 4px; }
    .title-l2 { font-size: 34px; font-weight: 800; color: #1A237E; line-height: 1.1; }
    .title-l3 { font-size: 24px; font-weight: 700; color: #FF7043; margin-bottom: 20px; }
    .intro-text { 
        font-size: 17px; color: #546E7A; line-height: 1.6; margin-bottom: 25px;
        border-left: 4px solid #FF7043; padding-left: 15px;
    }

    /* 按钮深度美化：确保在任何设备都醒目 */
    div.stButton > button {
        width: 100% !important;
        background-color: #1A237E !important;
        color: white !important;
        border-radius: 16px !important;
        height: 58px !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(26, 35, 126, 0.25) !important;
        margin-top: 10px;
    }
    div.stButton > button:active { transform: scale(0.97); }

    /* 答题页专用（进入答题后会动态恢复滚动） */
    .scrollable-app { overflow-y: auto !important; height: auto !important; }
    .q-text { font-size: 21px; font-weight: 600; color: #263238; margin-bottom: 25px; }
    .res-card { padding: 20px; border-radius: 15px; background: white; border-left: 8px solid #1A237E; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .warn-banner { padding: 20px; border-radius: 16px; margin-bottom: 15px; color: white; font-weight: 600; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 题库与维度 (保持不变) ---
if 'QUESTIONS' not in locals():
    QUESTIONS = [f"在日常生活中，{i+1}. 对应维度的具体表现行为描述..." for i in range(85)]

DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】依恋关系安全。", "【预警】地基有裂缝。", "【危险】地基动摇。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛。", "【内耗】内耗严重。", "【力竭】心理力竭。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通顺畅。", "【防御】防御增强。", "【断联】情感断联。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】抗挫力强。", "【下行】出现空心化。", "【枯竭】自我价值感极低。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】执行功能强。", "【疲劳】生理性疲劳。", "【宕机】大脑保护性关闭。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】社交正常。", "【退缩】回避明显。", "【受损】拒绝参与现实。"]}
}
# --- 5. 页面流程控制 ---

# A. 首页：强制居中 + 按钮内嵌逻辑
if st.session_state.step == 'home':
    # 再次确保首页状态下全局不可滚动
    st.markdown("<style>.stApp { overflow: hidden !important; }</style>", unsafe_allow_html=True)
    
    # 1. 开启卡片容器
    st.markdown('<div class="home-card-body">', unsafe_allow_html=True)
    
    # 2. 渲染文案内容
    st.markdown("""
        <div class='title-l1'>曹校长 脑科学专业版</div>
        <div class='title-l2'>家庭教育</div>
        <div class='title-l3'>十维深度探查表</div>
        <div class='intro-text'>
            这是一场跨越心与脑的对话。<br>
            你好，我是你的老朋友。<br><br>
            接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
            这不是一份考卷，而是给孩子一次被“看见”的机会。
        </div>
    """, unsafe_allow_html=True)
    
    # 3. 渲染原生按钮 (它会根据 CSS 自动适配到卡片宽度)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    
    # 4. 闭合卡片容器
    st.markdown('</div>', unsafe_allow_html=True)

# B. 答题页：恢复滚动条，进入流程
elif st.session_state.step == 'quiz':
    # 动态切换 CSS，允许答题页滚动
    st.markdown("<style>.stApp { overflow-y: auto !important; display: block !important; }</style>", unsafe_allow_html=True)
    
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.caption(f"当前进度：{cur + 1} / 85 题")
    
    # 题目显示
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    # 选项布局：双列长条
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

# C. 结果页：深度报告展示
elif st.session_state.step == 'report':
    st.markdown("<style>.stApp { overflow-y: auto !important; display: block !important; }</style>", unsafe_allow_html=True)
    
    # 顶部风险提示
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    # --- 1. 雷达图可视化 ---
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

    # --- 2. 三大红灯预警逻辑 ---
    # 情绪/生存危机 (59-66题)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到孩子目前存在明显的生存危机或极度情绪创伤。此时任何关于学习的督促都是“火上浇油”。请立刻停止施压，确保生命安全！</div>", unsafe_allow_html=True)
    
    # ADHD/脑特性 (67-72题)
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】孩子表现出注意力黑洞特质。这非态度问题，而是前额叶执行功能发育滞后，需科学干预。</div>", unsafe_allow_html=True)

    # 生理地基 (73-78题)
    if (sum(st.session_state.ans.get(i, 0) for i in range(72, 78))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【生理地基预警】检测到肠脑轴失调或慢性炎症迹象。建议先调理生理节律。</div>", unsafe_allow_html=True)

    # --- 3. 维度详细卡片 ---
    st.write("### 🔍 深度维度解析")
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}：分析结果</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    # --- 4. 转化引导卡片 ---
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。<br>其实，您不需要独自扛着。</p>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='text-align:left; font-weight:bold; margin-top:10px; color:#1A237E;'>添加老师您可以获得：</p>
            <div style='text-align:left; color:#1A237E; font-weight:700; margin:5px 0;'>1. 十个维度个性化改善方案</div>
            <div style='text-align:left; color:#1A237E; font-weight:700; margin:5px 0;'>2. 30 分钟 1V1 深度解析报告</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:18px; border-radius:15px; font-size:19px; font-weight:bold; margin-top:20px;">👉 点击添加老师，预约解析</a>
        </div>
    """, unsafe_allow_html=True)
    st.write("") # 底部留空
