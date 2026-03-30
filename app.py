import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制：实现一屏式锁定 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底遮蔽原网站品牌 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 全局样式 */
    .stApp { background: #F8F9FA; text-align: left !important; color: #455A64; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
    
    /* 首页一屏式遮盖容器：锁定在屏幕中心，消除滑动感 */
    .home-mask {
        position: fixed;
        top: 45%;         /* 视觉重心稍微偏上，更显专业 */
        left: 50%;
        transform: translate(-50%, -50%); 
        width: 90%;
        max-width: 500px;
        padding: 40px 25px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 28px;
        box-shadow: 0 20px 50px rgba(26, 35, 126, 0.15);
        border: 1px solid rgba(255,255,255,0.7);
        backdrop-filter: blur(15px);
        z-index: 10000;
        display: flex;
        flex-direction: column;
    }
    
    /* 三行标题规范 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }
    
    /* 老友感引导语 */
    .intro-text {
        font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 30px;
        border-left: 5px solid #FF7043; padding-left: 20px;
    }
    
    /* 题目与选项按钮 */
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.2);
    }
    div.stButton > button:hover { background-color: #0D47A1; transform: translateY(-2px); }
    div.stButton > button:active { transform: scale(0.97); }
    
    /* 结果页警报 Banner */
    .warn-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; text-align: left; }
    .bg-red { background: #C62828; }
    .bg-orange { background: #E65100; }
    .bg-blue { background: #0D47A1; }
    
    /* 维度解析卡片 */
    .res-card { padding: 20px; border-radius: 15px; background: white; border: 1px solid #E0E0E0; border-left: 8px solid #1A237E; margin-bottom: 15px; }
    
    /* 微信转化卡片 */
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

# --- 4. 维度话术数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固，依恋关系安全。", "【预警】地基有裂缝。", "【危险】地基动摇。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛。", "【内耗】内耗严重。", "【力竭】心理力竭。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通畅通。", "【防御】防御增强。", "【断联】情感断联。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】生机勃勃。", "【下行】动力下行。", "【枯竭】动力枯竭。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】认知高效。", "【疲劳】生理疲劳。", "【宕机】大脑宕机。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】规则意识强。", "【退缩】社交回避。", "【受损】功能受损。"]}
}
# --- 5. 页面流程 ---

# A. 首页 (一屏式体验：容器包裹所有元素实现锁定)
if st.session_state.step == 'home':
    # 利用 markdown 开启一个固定位置的 div 容器
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
    """, unsafe_allow_html=True)
    
    # 按钮必须在 div 闭合前渲染，以保证其在白色卡片内部，且随卡片整体居中
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    
    # 闭合 div 容器
    st.markdown("</div>", unsafe_allow_html=True)

# B. 答题页 (标准流布局)
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.write(f"当前进度：{cur + 1} / 85")
    
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    # 选项逻辑
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

# C. 结果页 (可视化与多维分析)
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    # --- 雷达图 ---
    scores = []
    labels = list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # --- 三大维度报警 ---
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】孩子目前存在明显的生存危机。请立刻停止施压，确保生命安全！</div>", unsafe_allow_html=True)
    
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】非态度问题，而是前额叶执行功能发育滞后。</div>", unsafe_allow_html=True)

    if (sum(st.session_state.ans.get(i, 0) for i in range(72, 78))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【生理地基预警】检测到肠脑轴失调。大脑已切至“生存模式”。</div>", unsafe_allow_html=True)

    # --- 维度详情展示 ---
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    # --- 微信转化 ---
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <p style='text-align:left; font-weight:bold; margin-top:20px; color:#1A237E;'>添加微信您可以获得：</p>
            <div class='benefit'>1. 十个维度个性化改善方案</div>
            <div class='benefit'>2. 30 分钟 1V1 深度解析</div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='color:#546E7A; font-size:15px; margin-bottom:20px;'>添加时请备注生成的数字</p>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold;">👉 点击添加老师</a>
        </div>
    """, unsafe_allow_html=True)
