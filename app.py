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
    .stApp { background: #F8F9FA; color: #455A64; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
    
    /* 首页卡片整体垂直居中逻辑 (修正：内容和按钮视为一体) */
    .home-mask {
        position: fixed;
        top: 48%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90%;
        max-width: 550px;
        padding: 45px 30px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 28px;
        box-shadow: 0 25px 60px rgba(26, 35, 126, 0.18);
        border: 1px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(20px);
        z-index: 9999;
        text-align: left !important;
    }
    
    /* 标题与文本 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1.5px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 35px; border-left: 5px solid #FF7043; padding-left: 20px; }
    
    /* 按钮全局样式 */
    div.stButton > button {
        border-radius: 16px; height: 62px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.2s all;
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.2);
    }
    div.stButton > button:hover { background-color: #0D47A1; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(26, 35, 126, 0.3); }
    div.stButton > button:active { transform: scale(0.96); } /* 点击缩放动效 */
    
    /* 答题页专用 */
    .q-text { font-size: 22px; font-weight: 600; color: #1A237E; line-height: 1.6; margin: 40px 0 20px 0; min-height: 80px; }
    
    /* 结果页元素 */
    .res-card { padding: 22px; border-radius: 18px; background: white; border-left: 10px solid #1A237E; margin-bottom: 18px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .warn-banner { padding: 22px; border-radius: 18px; margin-bottom: 25px; color: white; font-weight: 600; line-height: 1.6; }
    .bg-red { background: linear-gradient(135deg, #D32F2F, #C62828); }
    .bg-orange { background: linear-gradient(135deg, #F57C00, #E65100); }
    .bg-blue { background: linear-gradient(135deg, #1976D2, #0D47A1); }
    
    /* 转化卡片 */
    .wx-card { background: #FFFFFF; padding: 35px; border-radius: 30px; border: 2px solid #E8EAF6; text-align: center; margin-top: 50px; box-shadow: 0 15px 40px rgba(26,35,126,0.1); }
    .rid-box { font-size: 45px; font-weight: 900; color: #C62828; background: #F8F9FA; padding: 12px 35px; border-radius: 15px; border: 3px dashed #C62828; display: inline-block; margin: 25px 0; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 题库预设 ---
if 'QUESTIONS' not in locals():
    # 示例题库，实际应用时请替换为您的85题
    QUESTIONS = [
        "孩子最近是否经常表现出情绪突然爆发？",
        "您是否感到在管教孩子时力不从心？",
        "孩子与您的沟通是否仅限于询问生活琐事？",
        "孩子对以前感兴趣的活动是否失去了热情？",
        "在完成作业时，孩子是否需要不停地催促？",
        "孩子是否更倾向于躲在房间里玩电子产品？"
    ] + [f"这是第 {i+7} 题的具体内容..." for i in range(79)]

# --- 4. 十维解析数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固，依恋关系安全。", "【预警】地基有裂缝，系统承压接近临界。", "【危险】地基动摇，孩子缺乏基本安全感。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛，情绪自控力强。", "【内耗】内耗严重，管教伴随生理性无力。", "【力竭】心理力竭，已丧失有效引导能力。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通畅通，边界清晰信任高。", "【防御】防御性增强，沟通仅维持功能层面。", "【断联】情感断联，孩子有明显逃离倾向。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】生机勃勃，具备天然抗挫力。", "【下行】动力开始萎缩，出现空心化苗头。", "【枯竭】动力枯竭，自我价值感降至冰点。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】脑认知高效，任务执行力强。", "【疲劳】生理性疲劳导致执行功能受损。", "【宕机】大脑保护性关闭，对学业极端抗拒。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】社交正常，规则意识强。", "【退缩】依赖屏幕，现实社交回避明显。", "【受损】社会功能受损，拒绝参与现实生活。"]}
}
# --- 5. 页面流程 ---

# A. 首页 (整体居中且按钮内置)
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
    
    # 按钮直接在 div 内部渲染，保持整体感
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    # 顶部进度
    st.progress((cur + 1) / 85)
    st.write(f"进度: {cur+1} / 85")
    
    # 题目显示
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    # 选项平铺
    opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
    cols = st.columns(2)
    for i, (txt, val) in enumerate(opts):
        with (cols[i % 2]):
            if st.button(txt, key=f"q_{cur}_{i}", use_container_width=True):
                st.session_state.ans[cur] = val
                if cur == 84: 
                    st.session_state.step = 'report'
                else: 
                    st.session_state.cur += 1
                st.rerun()
    
    # 返回按钮
    if cur > 0:
        st.write("---")
        if st.button("⬅ 回到上一题", key="back", use_container_width=False):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页
elif st.session_state.step == 'report':
    st.markdown("<h2 style='text-align:center; color:#1A237E;'>探查结果报告</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    # --- 雷达图绘制 ---
    scores = []
    labels = list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        # 计算平均分并转换为100分制
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=450)
    st.plotly_chart(fig, use_container_width=True)

    # --- 三大核心预警系统 ---
    # 1. 情绪红灯 (59-66)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到孩子目前存在明显的生存危机或极度情绪创伤。请立刻停止施压，确保生命安全！</div>", unsafe_allow_html=True)
    
    # 2. ADHD脑特性 (67-72)
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】孩子表现出注意力黑洞特质。这非态度问题，而是前额叶执行功能发育滞后。</div>", unsafe_allow_html=True)

    # 3. 生理地基 (73-78)
    if (sum(st.session_state.ans.get(i, 0) for i in range(72, 78))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【生理地基预警】检测到肠脑轴失调迹象。大脑已切至“生存模式”，建议先调理生理节律。</div>", unsafe_allow_html=True)

    # --- 维度详细卡片 ---
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}：</b> {info['levels'][lv]}</div>", unsafe_allow_html=True)

    # --- 转化区 ---
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。其实，您不需要独自扛着。</p>
            <p style='text-align:left; font-weight:bold; margin-top:20px; color:#1A237E;'>添加微信您可以获得：</p>
            <ul style='text-align:left; color:#1A237E; font-weight:600;'>
                <li>十个维度个性化改善方案</li>
                <li>30 分钟 1V1 深度解析</li>
            </ul>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='color:#546E7A; font-size:15px; margin-bottom:20px;'>添加时请备注上方 6 位数字</p>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold;">👉 点击添加老师，预约 1V1 解析</a>
        </div>
    """, unsafe_allow_html=True)
