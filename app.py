import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. UI 深度定制：深蓝品牌色 & 首页遮罩 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

# 颜色定义：主色 #1A237E (深蓝), 强调色 #FF7043 (暖橙), 辅助色 #455A64 (深灰蓝)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    .stApp { background: #F4F7F9; text-align: left !important; color: #455A64; }

    /* 首页专用遮盖容器 (Mask) */
    .home-mask {
        padding: 40px 25px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        max-width: 800px;
        margin: 0 auto;
    }

    /* 标题样式 */
    .main-title {
        color: #1A237E;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        color: #546E7A;
        font-size: 16px;
        text-align: center;
        margin-bottom: 30px;
    }

    /* 按钮样式 */
    .stButton > button {
        background-color: #FF7043;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #E64A19;
        transform: translateY(-2px);
    }

    /* 雷达图容器 */
    .radar-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 转化区卡片 */
    .conversion-card {
        background: linear-gradient(135deg, #FFF8E1, #FFECB3);
        border-left: 6px solid #FF7043;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .conversion-title {
        color: #D84315;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .conversion-title::before {
        content: "💡";
        margin-right: 10px;
        font-size: 24px;
    }
    .conversion-content {
        font-size: 16px;
        line-height: 1.6;
        color: #5D4037;
    }
    .conversion-item {
        margin: 10px 0;
        padding-left: 20px;
        position: relative;
    }
    .conversion-item::before {
        content: "•";
        position: absolute;
        left: 0;
        color: #FF7043;
        font-weight: bold;
    }
    .conversion-note {
        margin-top: 15px;
        font-size: 14px;
        color: #757575;
        font-style: italic;
    }

    /* 预警提示框 */
    .warning-box {
        background: #FFEBEE;
        border: 1px solid #CDD2;
        color: #C628FF28;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        font-weight: bold;
    }

    </style>
""", unsafe_allow_html=True)

# --- 2. 初始化会话状态 ---
if 'step' not in st.session_state:
    st.session_state.step = 'home'
if 'ans' not in st.session_state:
    st.session_state.ans = {}
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(random.randint(100000, 999999))

# --- 3. 题库数据注入 ---
QUESTIONS_78 = [
    # 1-8 系统维度
    "孩子在家是否经常主动做家务？", "家庭规则是否清晰且稳定？", "员之间沟通是否顺畅？家庭成",
    "孩子是否愿意参与家庭决策？", "家里是否有固定的家庭活动时间？", "孩子是否感到被尊重和理解？",
    "家庭氛围是否轻松愉快？", "孩子是否知道遇到问题可以找谁求助？",
    # 9-18 家长维度
    "家长是否经常表扬孩子？", "家长是否容易发脾气？", "家长是否经常陪伴孩子？",
    "家长是否鼓励孩子独立思考？", "家长是否过度控制孩子？", "家长是否尊重孩子的隐私？",
    "家长是否经常与孩子谈心？", "家长是否以身作则？", "家长是否了解孩子的兴趣爱好？",
    "家长是否经常批评孩子？",
    # 19-28 关系维度
    "孩子与同学相处是否融洽？", "孩子是否愿意分享自己的想法？", "孩子是否容易交到朋友？",
    "孩子在集体活动中是否积极参与？", "孩子是否经常被同伴排斥或孤立？", "孩子是否愿意与异性交往？",
    "孩子是否对人际关系敏感？", "孩子是否容易嫉妒他人？", "孩子是否愿意主动帮助别人？",
    "孩子是否容易信任他人？",
    # 29-37 动力维度
    "孩子是否对学习充满兴趣？", "孩子是否经常主动学习？", "孩子是否容易困难的任务？放弃",
    "孩子是否对自己的未来有规划？", "孩子是否经常设定目标并完成？", "孩子是否容易被激励？",
    "孩子是否因为失败而气馁？", "孩子是否相信自己有能力做好事情？", "孩子是否经常感到无聊或无趣？",
    # 38-48 学业维度
    "孩子课堂注意力是否集中？", "孩子作业是否按时完成？", "孩子考试成绩是否稳定？",
    "孩子是否喜欢阅读课外书？", "孩子是否经常向老师提问？", "孩子是否容易分心？",
    "孩子是否对某一学科特别感兴趣？", "孩子是否经常复习功课？", "孩子是否容易拖延？",
    "孩子是否参加学习竞赛或活动？", "孩子是否对自己的学业成绩满意？经常",
    # 49-58 社会化维度
    "孩子是否遵守社会规则？", "孩子是否尊重他人？", "孩子是否具有责任感？",
    "孩子是否愿意承担后果？", "孩子是否关心社会问题？", "孩子是否具有同理心？",
    "孩子是否愿意参与公益活动？", "孩子是否尊重不同文化和观点？", "孩子是否具有团队合作精神？",
    "孩子是否对社会有归属感？",
    # 59-66 情绪状态维度（专项风险）
    "孩子是否经常感到焦虑？", "孩子是否容易生气或暴躁？", "孩子是否经常感到沮丧？",
    "孩子是否容易流泪或情绪失控？", "孩子是否经常感到无助？", "孩子是否容易紧张？",
    "孩子是否经常感到疲惫？", "孩子是否经常感到孤独？",
    # 67-72 注意状态维度（专项风险）
    "孩子是否经常走神？", "孩子是否容易分心？", "孩子是否难以专注一件事情？",
    "孩子是否经常被外界干扰？", "孩子是否经常忘记刚刚说过的话？", "孩子是否经常需要重复提醒？",
    # 73-78 底层营养维度（专项风险）
    "孩子饮食是否均衡？", "孩子睡眠是否充足？", "孩子运动是否规律？",
    "孩子是否有足够的户外活动？", "孩子是否经常吃零食或垃圾食品？", "孩子是否经常熬夜？",
]

BG_QS = [
    "孩子性别是？", "孩子年龄是？", "孩子年级是？", "孩子性格偏向内向还是外向？",
    "孩子目前主要困扰是什么？", "家长最希望改善的方面是什么？", "家庭所在城市是？",
]

# --- 4. 页面路由逻辑 ---
if st.session_state.step == 'home':
    # 首页遮罩容器
    st.markdown('<div class="home-mask">', unsafe_allow_html=True)

    st.markdown('<div class="main-title">家庭教育十维深度探查</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">8分钟，10个维度，精准定位孩子成长卡点，提供个性化改善方案</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("🎯 **测评价值**：")
    st.markdown("- 揭示孩子隐藏的求助信号")
    st.markdown("- 发现家庭教育的盲区与误区")
    st.markdown("- 提供可落地的改善建议")

    st.markdown("---")

    if st.button("立即开始测评", key="start_btn"):
        st.session_state.step = 'quiz'
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == 'quiz':
    # 答题页逻辑
    st.markdown('<div class="home-mask">', unsafe_allow_html=True)

    # 进度条
    total_q = 85
    current_q = len(st.session_state.ans) + 1
    progress = current_q / total_q
    st.progress(progress)
    st.markdown(f"<p style='text-align:center; color:#546E7A;'>第 {current_q} 题 / 共 {total_q} 题", unsafe_allow_html=True)

    # 显示当前题目
    if current_q <= 78:
        q_text = QUESTIONS_78[current_q - 1]
        st.markdown(f"### 📝 问题 {current_q}")
        st.markdown(q_text)

        # 选项
        option_labels = ["完全不符合", "比较不符合", "一般", "比较符合", "完全符合"]
        selected = st.radio("", option_labels, index=st.session_state.ans.get(current_q, 0), key=f"q_{current_q}")

        # 保存答案
        if st.button("下一题", key="next_btn"):
            st.session_state.ans[current_q] = option_labels.index(selected)
            st.rerun()

    else:
        # 79-85 背景题
        bg_idx = current_q - 79
        q_text = BG_QS[bg_idx]
        st.markdown(f"### 📝 问题 {current_q}")
        st.markdown(q_text)

        # 背景题选项（单选或输入）
        if bg_idx in [0, 1, 2]:  # 性别、年龄、年级
            options = ["男", "女"] if bg_idx == 0 else ["6岁", "7岁", "8岁", "9岁", "10岁", "11岁", "12岁", "13岁", "14岁", "15岁"] if bg_idx == 1 else ["一年级", "二年级", "三年级", "四年级", "五年级", "六年级", "初一", "初二", "初三", "高一", "高二", "高三"]
            selected = st.radio("", options, index=st.session_state.ans.get(current_q, 0), key=f"q_{current_q}")
            if st.button("下一题", key="next_btn_bg"):
                st.session_state.ans[current_q] = options.index(selected)
                st.rerun()
        elif bg_idx == 3:  # 性格
            options = ["内向", "外向", "混合型"]
            selected = st.radio("", options, index=st.session_state.ans.get(current_q, 0), key=f"q_{current_q}")
            if st.button("下一题", key="next_btn_bg"):
                st.session_state.ans[current_q] = options.index(selected)
                st.rerun()
        elif bg_idx == 4:  # 主要困扰
            selected = st.text_input("", value=st.session_state.ans.get(current_q, ""), key=f"q_{current_q}")
            if st.button("下一题", key="next_btn_bg"):
                st.session_state.ans[current_q] = selected
                st.rerun()
        elif bg_idx == 5:  # 最希望改善的方面
            selected = st.text_input("", value=st.session_state.ans.get(current_q, ""), key=f"q_{current_q}")
            if st.button("下一题", key="next_btn_bg"):
                st.session_state.ans[current_q] = selected
                st.rerun()
        elif bg_idx == 6:  # 城市
            selected = st.text_input("", value=st.session_state.ans.get(current_q, ""), key=f"q_{current_q}")
            if st.button("提交并查看报告", key="submit_btn"):
                st.session_state.ans[current_q] = selected
                st.session_state.step = 'report'
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == 'report':
    # 结果页逻辑
    st.markdown('<div class="home-mask">', unsafe_allow_html=True)

    # 顶部截屏提醒
    st.markdown('<div class="warning-box">📸 重要提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。</div>', unsafe_allow_html=True)

    # --- 1. 计分与维度均分计算 ---
    ans = st.session_state.ans
    dim_ranges = {
        '系统': (0, 8),    # 1-8题
        '家长': (8, 18),   # 9-18题
        '关系': (18, 28),  # 19-28题
        '动力': (28, 37),  # 29-37题
        '学业': (37, 48),  # 38-48题
        '社会化': (48, 58), # 49-58题
    }

    # 计算每个维度的均分（1-5分制）
    dim_scores = {}
    for dim, (start, end) in dim_ranges.items():
        scores = []
        for i in range(start + 1, end + 1):
            score = ans.get(i, 0)
            if isinstance(score, int) and 0 <= score <= 4:
                scores.append(score + 1)  # 转换为1-5分
        if scores:
            dim_scores[dim] = sum(scores) / len(scores)
        else:
            dim_scores[dim] = 0

    # 专项风险维度（不参与雷达图，但用于预警）
    risk_dims = {
        '情绪状态': (58, 66),  # 59-66题
        '注意状态': (66, 72),  # 67-72题
        '底层营养': (72, 78),  # 73-78题
    }
    risk_scores = {}
    for dim, (start, end) in risk_dims.items():
        scores = []
        for i in range(start + 1, end + 1):
            score = ans.get(i, 0)
            if isinstance(score, int) and 0 <= score <= 4:
                scores.append(score + 1)
        if scores:
            risk_scores[dim] = sum(scores) / len(scores)
        else:
            risk_scores[dim] = 0

    # --- 2. 生成六维雷达图 ---
    st.markdown('<div class="radar-container">', unsafe_allow_html=True)
    st.markdown("## 📊 六维雷达图分析")

    categories = list(dim_scores.keys())
    values = list(dim_scores.values())

    # 创建雷达图
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='当前得分',
        line_color='#1A237E',
        fillcolor='rgba(26, 35, 126, 0.2)',
        hovertemplate='%{theta}: %{r:.2f}<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[0, 1, 2, 3, 4, 5],
                ticktext=["0", "1", "2", "3", "4", "5"],
                gridcolor='lightgray',
            ),
            angularaxis=dict(
                direction='clockwise',
                period=6,
            ),
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. 六维解读（根据得分高低） ---
    st.markdown('<div class="radar-container">', unsafe_allow_html=True)
    st.markdown("## 🔍 六维深度解读")

    def get_interpretation(dim, score):
        if score < 2.5:
            return f"**{dim}维度得分偏低 ({score:.2f})**：孩子在这个方面存在明显短板，可能正在经历压力或缺乏支持，需要优先关注和干预。"
        elif 2.5 <= score < 3.5:
            return f"**{dim}维度得分中等 ({score:.2f})**：处于正常范围，但仍有提升空间，建议通过日常互动和引导逐步优化。"
        else:
            return f"**{dim}维度得分较高 ({score:.2f})**：表现良好，说明孩子在这个方面具备较强的能力或支持系统，可作为优势资源强化。"

    for dim in dim_scores:
        st.markdown(get_interpretation(dim, dim_scores[dim]))

    st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. 专项风险预警（情绪、注意、底层营养） ---
    st.markdown('<div class="radar-container">', unsafe_allow_html=True)
    st.markdown("## ⚠️ 专项风险预警")

    def get_risk_interpretation(dim, score):
        if score > 3.5:
            return f"**{dim}维度得分偏高 ({score:.2f})**：存在明显风险信号，建议关注孩子近期状态，必要时寻求专业支持。"
        elif 2.5 <= score <= 3.5:
            return f"**{dim}维度得分中等 ({score:.2f})**：有轻微波动或潜在风险，建议保持观察，加强沟通。"
        else:
            return f"**{dim}维度得分正常 ({score:.2f})**：目前无明显风险，继续保持当前状态即可。"

    for dim in risk_scores:
        st.markdown(get_risk_interpretation(dim, risk_scores[dim]))

    st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. 微信转化区（完全按照您提供的文案） ---
    st.markdown('<div class="conversion-card">', unsafe_allow_html=True)
    st.markdown('<div class="conversion-title">这份报告揭示了孩子的求救，也看见了您的委屈。其实，您不需要独自扛着。</div>', unsafe_allow_html=True)
    st.markdown('<div class="conversion-title">添加微信您可以获得：</div>', unsafe_allow_html=True)
    st.markdown('<div class="conversion-content">', unsafe_allow_html=True)
    st.markdown('<div class="conversion-item">1. 十个维度个性化改善方案</div>', unsafe_allow_html=True)
    st.markdown('<div class="conversion-item">2. 30分钟 1V1 深度解析</div>', unsafe_allow_html=True)
    st.markdown('<div class="conversion-item">3. 特惠 198 元（原价 598 元）</div>', unsafe_allow_html=True)
    st.markdown('<div class="conversion-note">添加时请备注生成的数字</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. 添加老师按钮（绑定企业微信链接） ---
    st.markdown("---")
    st.markdown('<div style="text-align:center; margin-top:20px;">', unsafe_allow_html=True)
    st.markdown(f'<a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="background-color: #1A237E; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">添加老师</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. 页脚信息 ---
st.markdown("""
    <div style='position: fixed; bottom: 10px; right: 10px; font-size: 12px; color: #9E9E9E;'>
        家庭教育十维深度探查 · 2025
    </div>
""", unsafe_allow_html=True)
