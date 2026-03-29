import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 样式与视觉定制 (极致排版 & 品牌标题) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

# CSS 注入：隐藏 Streamlit 官方信息 & 美化排版
st.markdown("""
    <style>
    /* 彻底隐藏右上角菜单、右下角 GitHub 链接和 Streamlit 官方页脚 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .reportview-container .main footer {visibility: hidden;}
    [data-testid="stSidebar"] {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* 首页标题美化 (三行排版) */
    .title-row1 { text-align: center; font-size: 36px; font-weight: 800; color: #1B5E20; margin-bottom: -15px; }
    .title-row2 { text-align: center; font-size: 30px; font-weight: 700; color: #1B5E20; margin-top: -10px; margin-bottom: -15px;}
    .title-sub { text-align: center; font-size: 16px; color: #666; font-style: italic; border-top: 1px solid #E8F5E9; display: inline-block; padding-top: 5px; }
    
    /* 题目单行显示 */
    .question-box { font-size: 21px; font-weight: 600; margin-bottom: 25px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: center; color: #333; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-size: 16px; }
    .report-card { padding: 18px; border-radius: 12px; background-color: #F0F4F0; border-left: 5px solid #2E7D32; margin-bottom: 15px; }
    
    /* 微信引导强化 */
    .highlight-id { font-size: 30px; font-weight: 900; color: #D32F2F; background-color: #FFF3F3; padding: 5px 15px; border-radius: 8px; border: 2px dashed #D32F2F; display: inline-block; }
    .权益-title { font-size: 24px; font-weight: 800; color: #1B5E20; text-align: center; margin-bottom: 15px;}
    .权益-item { font-size: 18px; margin-bottom: 10px; font-weight: 600; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# 渲染首页双行标题和缩小版的 sub [cite: 149, 150]
st.markdown("""
    <div class='title-row1'>家庭教育</div>
    <div class='title-row2'>十维深度探查表</div>
    <div style='text-align: center;'><div class='title-sub'>( 脑科学专业版 )</div></div>
    """, unsafe_allow_html=True)

# --- 2. 题库数据 (1-78计分 + 7道背景) ---
# [cite: 5-82] (1-78计分题文字请沿用上一版本，此处省略以节省空间)

QS_BG = [
    ("79. 是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
    ("80. 为了解决问题，您之前尝试过哪些方式？", ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"], "multi"),
    ("81. 之前尝试的方法没有彻底生效的原因是？", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"], "multi"),
    ("82. 目前最迫切想解决的前三个痛点是？", ["关系/叛逆", "厌学/手机", "专注力差/成绩差", "情绪较大", "其它"], "multi"),
    ("83. 如诊断根源在于“家庭系统及认知”，您是否有勇气参与改变？", ["非常愿意", "愿意，但需指导", "比较纠结", "只想改孩子"], "single"),
    ("84. 填完后，是否愿预约一次资深专家“全面分析解读”？", ["是", "否"], "single"),
    ("85. 如果需投入时间及精力扭转局面，您是否有兴趣了解我们的系统方案？", ["是", "否"], "single")
]

# --- 3. 状态管理 ---
if 'idx' not in st.session_state:
    st.session_state.update({'step':'home', 'idx':0, 'ans':{}, 'rid':str(random.randint(100000, 999999))})

# --- 4. 测评界面逻辑 ---
if st.session_state.step == 'home':
    st.info("💡 **这是一场跨越心与脑的对话，请放空杂念，给孩子和自己一次被“看见”的机会。**")
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'testing'; st.rerun()

elif st.session_state.step == 'testing':
    cur = st.session_state.idx
    st.progress((cur + 1) / 85)
    
    if cur < 78:
        st.write(f"第 {cur+1} 题 / 共 85 题")
        # 强制单行排版
        st.markdown(f"<div class='question-box'>{QS_SCORE[cur]}</div>", unsafe_allow_html=True)
        cols = st.columns(2)
        if cols[0].button("0 (从不)", use_container_width=True, key=f"q{cur}_{0}"): move(0)
        if cols[1].button("1 (偶尔)", use_container_width=True, key=f"q{cur}_{1}"): move(1)
        if cols[0].button("2 (经常)", use_container_width=True, key=f"q{cur}_{2}"): move(2)
        if cols[1].button("3 (总是)", use_container_width=True, key=f"q{cur}_{3}"): move(3)
    elif cur < 85:
        q_txt, opts, mode = QS_BG[cur-78]
        st.markdown(f"### {q_txt}")
        u_val = st.multiselect("可多选:", opts) if mode == "multi" else st.radio("请选择:", opts, index=None)
        if st.button("生成最终报告" if cur==84 else "下一步", use_container_width=True, disabled=not u_val):
            st.session_state.ans[cur] = u_val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.idx += 1
            st.rerun()
    
    if cur > 0:
        if st.button("⬅️ 返回上一题"): st.session_state.idx -= 1; st.rerun()

# --- 5. 报告逻辑 (核心逻辑和话术坚决不动) ---
elif st.session_state.step == 'report':
    st.header("📊 深度探查诊断报告")
    st.warning("⚠️ 重要提醒：分数越高，代表该维度的“负荷”或“风险”越大。")
    
    # 维度计算与话术库 [cite: 106-135] (沿用上一版话术库内容)
    DIM_6_DATA = { "家庭系统": (range(0,8), { "low": "您的家庭地基非常扎实...", "mid": "您的家庭基础整体是稳定的...", "high": "家里的‘气压’太不稳定了..." }), # (省略文字内容)
        # (其他维度请沿用上一版本)...
    }

    scores = {}
    st.subheader("🔍 核心六维度分析")
    for name, (indices, txts) in DIM_6_DATA.items():
        avg = sum(st.session_state.ans.get(i,0) for i in indices) / len(indices)
        scores[name] = avg
        if avg >= 1.9: color, level, desc = "#D32F2F", "高分危险", txts["high"]
        elif avg >= 0.9: color, level, desc = "#F57C00", "预警", txts["mid"]
        else: color, level, desc = "#388E3C", "优秀优秀优秀", txts["low"]
        
        with st.container():
            st.markdown(f"#### **{name}：{avg:.2f}分 ({level})**")
            st.markdown(f"<div class='report-card' style='border-left: 5px solid {color};'>{desc}</div>", unsafe_allow_html=True)

    # 专项报警 [cite: 136-147] (逻辑不动)
    if any(st.session_state.ans.get(i) == 3 for i in range(58, 66)):
        st.error("🚨 红灯警报：当前孩子情绪安全水位极低，建议暂停学业施压，优先进行情感固着。")
    # (其他报警提示省略)...

    # 雷达图 (视觉辅助)
    fig = go.Figure(data=go.Scatterpolar(r=list(scores.values()), theta=list(scores.keys()), fill='toself', line_color='#1B5E20'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- 6. 转化闭环 (强化强调板块) [cite: 151-159] ---
    st.markdown("---")
    
    # 引导话术
    st.markdown("""<div style='text-align: center; color: #666;'>这一份报告揭示了孩子的求救，也看见了您的委屈。其实，您不需要独自扛着。</div>""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 使用 st.info 强调特惠权益 [cite: 155-158]
    st.info("""
    <div class='权益-title'>💝 专属特惠权益</div>
    <div class='权益-item'>🎁 获得 10 维度个性化改善PDF方案 (含生理归因分析)</div>
    <div class='权益-item'>🗣️ 资深专家 30分钟 1V1 深度解析课 (解决当下最迫切问题)</div>
    <div class='权益-item'>🔥 <b>限时特惠：198元</b> (原价 598元)</div>
    """, icon="🎁")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # **核心编号强调：醒目、加粗、红色 dashed 框** [cite: 159]
    st.markdown("<div style='text-align: center;'>添加专家老师微信，备注专属报告编号：</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'><span class='highlight-id'>{st.session_state.rid}</span></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 链接按钮
    st.link_button("👉 点击添加老师，预约深度诊断", "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f", use_container_width=True)
    st.caption(f"报告编号: {st.session_state.rid} (请保存截屏)")
