import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制：实现物理级一屏整体上移 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底隐藏系统残留 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 1. 首页一屏绝对锁定：禁止一切滑动 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
        background: #F4F7F9;
    }

    /* 2. 整体布局上移容器 */
    .viewport-fix {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* 改为靠顶对齐 */
        height: 100vh;
        padding-top: 8vh; /* 通过这个值控制上移的高度，值越小越靠顶 */
    }

    /* 3. 首页一体化大卡片 */
    .home-card {
        background: white;
        padding: 35px 25px;
        border-radius: 28px;
        box-shadow: 0 15px 45px rgba(26, 35, 126, 0.1);
        border: 1px solid rgba(255,255,255,1);
        width: 100%;
        max-width: 400px;
    }

    /* 4. 标题与文案排版 */
    .t-l1 { font-size: 14px; color: #90A4AE; font-weight: 500; margin-bottom: 6px; }
    .t-l2 { font-size: 34px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 4px; }
    .t-l3 { font-size: 24px; font-weight: 700; color: #FF7043; margin-bottom: 20px; }
    .intro-box { 
        font-size: 17px; color: #546E7A; line-height: 1.7; margin-bottom: 30px;
        border-left: 4px solid #FF7043; padding-left: 15px;
    }

    /* 5. 原生按钮：深度定制 */
    div.stButton > button {
        width: 100% !important;
        background-color: #1A237E !important;
        color: white !important;
        border-radius: 14px !important;
        height: 58px !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(26, 35, 126, 0.15) !important;
    }

    /* 6. 答题与结果页：动态覆盖锁定，允许滑动 */
    .scroll-allow { overflow-y: auto !important; height: auto !important; }
    
    /* 其他通用样式 */
    .q-text { font-size: 21px; font-weight: 600; color: #263238; margin: 25px 0; }
    .res-card { padding: 18px; border-radius: 15px; background: white; border-left: 8px solid #1A237E; margin-bottom: 12px; }
    .warn-banner { padding: 20px; border-radius: 16px; margin-bottom: 18px; color: white; font-weight: 600; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    .wx-card { background: white; padding: 25px; border-radius: 22px; border: 2px solid #E8EAF6; text-align: center; margin-top: 30px; }
    .rid-box { font-size: 38px; font-weight: 900; color: #C62828; border: 3px dashed #C62828; display: inline-block; padding: 5px 20px; margin: 15px 0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 题库预设 ---
if 'QUESTIONS' not in locals():
    QUESTIONS = [f"这里是第 {i+1} 题的具体描述内容..." for i in range(85)]

# --- 4. 维度数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": ["【稳固】地基牢固。", "【预警】地基有裂缝。", "【危险】地基动摇。"]},
    "家长维度": {"range": range(8,18), "levels": ["【优秀】能量充沛。", "【内耗】内耗严重。", "【力竭】心理力竭。"]},
    "关系维度": {"range": range(18,28), "levels": ["【信任】沟通顺畅。", "【防御】防御增强。", "【断联】情感断联。"]},
    "动力维度": {"range": range(28,37), "levels": ["【旺盛】抗挫力强。", "【下行】出现下行。", "【枯竭】动力枯竭。"]},
    "学业维度": {"range": range(37,48), "levels": ["【高效】执行功能强。", "【疲劳】生理疲劳。", "【宕机】大脑保护性关闭。"]},
    "社会化": {"range": range(48,58), "levels": ["【自如】社交正常。", "【退缩】回避明显。", "【受损】功能受损。"]}
}
# --- 5. 页面流程控制 ---

# A. 首页：实现“整体上移”且“禁止滑动”
if st.session_state.step == 'home':
    # 强制当前页面禁止滑动
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { overflow: hidden !important; }</style>", unsafe_allow_html=True)
    
    # 开启“上移”容器
    st.markdown('<div class="viewport-fix">', unsafe_allow_html=True)
    
    # 嵌套白色卡片
    st.markdown('<div class="home-card">', unsafe_allow_html=True)
    
    # 内容文案
    st.markdown("""
        <div class='t-l1'>曹校长 脑科学专业版</div>
        <div class='t-l2'>家庭教育</div>
        <div class='t-l3'>十维深度探查表</div>
        <div class='intro-box'>
            这是一场跨越心与脑的对话。<br>
            你好，我是你的老朋友。<br><br>
            接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
            这不仅是一份测评，更是给孩子一次被“看见”的机会。
        </div>
    """, unsafe_allow_html=True)
    
    # 原生按钮：物理嵌套在 home-card 内
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
        
    st.markdown('</div></div>', unsafe_allow_html=True) # 闭合 home-card 和 viewport-fix

# B. 答题页：恢复滑动功能
elif st.session_state.step == 'quiz':
    # 动态覆盖之前的锁定，允许滑动
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { overflow-y: auto !important; height: auto !important; }</style>", unsafe_allow_html=True)
    
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.caption(f"当前进度：{cur + 1} / 85 题")
    
    # 题目显示
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    # 选项布局：2x2 矩阵
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
        st.write("---")
        if st.button("⬅ 返回上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页：分析报告
elif st.session_state.step == 'report':
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { overflow-y: auto !important; height: auto !important; }</style>", unsafe_allow_html=True)
    
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    # 雷达图
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

    # 预警逻辑
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到生存危机。请立刻停止施压，确保生命安全！</div>", unsafe_allow_html=True)
    
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】非态度问题，而是前额叶执行功能发育滞后。</div>", unsafe_allow_html=True)

    if (sum(st.session_state.ans.get(i, 0) for i in range(72, 78))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【生理地基预警】检测到肠脑轴失调。大脑已切至“生存模式”。</div>", unsafe_allow_html=True)

    # 维度分析
    st.write("### 🔍 维度详细分析")
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    # 转化区域
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:17px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。<br>此刻，您不需要独自扛着。</p>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='text-align:left; font-weight:bold; color:#1A237E; margin-top:10px;'>添加老师备注编号：</p>
            <div style='text-align:left; color:#1A237E; font-size:15px; margin:5px 0;'>• 获得十个维度个性化改善方案</div>
            <div style='text-align:left; color:#1A237E; font-size:15px; margin:5px 0;'>• 30 分钟 1V1 深度报告解析</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:18px; border-radius:12px; font-size:18px; font-weight:bold; margin-top:15px;">👉 点击添加老师，预约解析</a>
        </div>
    """, unsafe_allow_html=True)
    st.write("###") # 底部留空
