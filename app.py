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

# --- 4. 维度话术数据库 (严格匹配文档文案) ---
DIM_DATA = {
    "家庭系统": {
        "range": range(0, 8), 
        "levels": [
            "【稳固】您的家庭地基非常扎实，孩子早期依恋关系很好。这意味着孩子内心的安全感底色是亮的，只要解决表层的功能问题，他好起来会比别人快得多。",
            "【内耗】您的家庭基础整体是稳定的，但内部存在一些“微损耗”（如教育标准不一）。孩子现在像是在顺风和逆风交替的环境下航行，虽然没翻船，但走得很累。",
            "【动荡】家里的“气压”太不稳定了。孩子现在就像在地震带上盖房子，他把所有的能量都用来“维稳”了，根本没有余力去搞学习。"
        ]
    },
    "家长状态": {
        "range": range(8, 18), 
        "levels": [
            "【高能】您的心理建设做得很好。您是孩子最稳的后盾。现在的困局不是您无能，而是您手里缺一把精准的“手术刀”。",
            "【疲劳】您正处于“育儿倦怠”的边缘。您依然在坚持，但这种坚持带有一种强迫性的自我牺牲感。现在的您就像亮起黄灯的仪表盘，提醒您该停下来修整认知模式了。",
            "【力竭】您现在的油箱已经干了。您在用透支自己的方式陪跑，这种焦灼感会通过镜像神经元直接传染给孩子，咱们得先帮您把油加满。"
        ]
    },
    "亲子关系": {
        "range": range(18, 28), 
        "levels": [
            "【顺畅】最宝贵的是，孩子还愿意跟您说真心话。只要情感管道通着，任何技术手段都能 100% 发挥作用。",
            "【疏离】你们之间没有大冲突，但缺乏“深链接”。沟通仅维持在琐事的“事务性交流”上。孩子正在慢慢关上心门，如果您不主动更换频率，他会习惯性心理隔离。",
            "【淤塞】你们之间现在是“信号屏蔽”状态。您说的每一句“为他好”，在他听来都是攻击。不先疏通情感，所有的教育都是无效功。"
        ]
    },
    "动力状态": {
        "range": range(28, 37), 
        "levels": [
            "【自驱】孩子骨子里是有胜负欲和生命力的。他现在的颓废只是“暂时的死机”，只要重装系统，他自己就能跑起来。",
            "【摇摆】孩子的生命力处于“待机状态”。他有想好的愿望，但缺乏持续的推力。这种“推一下动一下”的状态，最容易在压力剧增时彻底熄火。",
            "【空心】孩子已经进入了“节能模式”，对外界失去了探索欲。这是典型的生命力萎缩，我们要通过底层激活，让他重新“活”过来。"
        ]
    },
    "学业管理": {
        "range": range(37, 48), 
        "levels": [
            "【高效】孩子的大脑硬件配置其实很高，执行功能没问题。现在的成绩波动，纯粹是情绪或态度的小感冒，很好修补。",
            "【补偿】孩子目前的学业表现是一种“高代偿”的维持。他在用双倍意志力弥补脑启动效率不足。一旦难度超过极限，会迅速厌学崩盘。",
            "【损耗】这不是态度问题，是“大脑CPU过载”。他写一个字消耗的能量是别人的三倍。咱们得用脑科学的方法帮他降载。"
        ]
    },
    "社会化适应": {
        "range": range(48, 58), 
        "levels": [
            "【合群】孩子的社会化属性很好。这种对集体的归属感，是我们后期把他从手机世界拉回现实的最强抓手。",
            "【依赖】电子世界对他吸引力正在盖过现实。如果现在不干预，他会越来越倾向于在虚拟世界寻找安全感，现实社交能力将持续退化。",
            "【退缩】他在现实世界里找不到成就感，只能去虚拟世界吸氧。学校对他来说不是学习的地方，而是“刑场”，我们要重建他的现实自信。"
        ]
    }
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

# C. 结果报告页逻辑
elif st.session_state.step == 'report':
    # --- 标题部分 ---
    st.markdown("<h2 style='text-align:center; color:#1A237E; margin-bottom:15px;'>报告解析</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:12px; border-radius:10px; text-align:center; margin-bottom:20px; font-size:14px;'>📸 请【截屏保存】本页结果，作为咨询凭证。</div>", unsafe_allow_html=True)
    
    # 1. 风险预警模块（暖橙色卡片提示）
    st.markdown("<p style='color:#E65100; font-weight:bold; margin-bottom:10px;'>核心风险筛查：</p>", unsafe_allow_html=True)
    
    # 7. 情绪状态预警 (59-66题)
    emo_scores = [st.session_state.ans.get(i, 0) for i in range(58, 66)]
    if any(s == 3 for s in emo_scores) or (sum(emo_scores) >= 24 * 0.6) or any(st.session_state.ans.get(i, 0) >= 2 for i in [64, 65]): # 假设65/66为消极倾向题
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【情绪状态预警】当前孩子情绪安全水位极低，沉默是他在呼救。首要任务不是抓学习，而是“稳情绪”，必须立刻切入心理安全干预。</div>", unsafe_allow_html=True)
    
    # 8. 注意状态预警 (67-72题)
    adhd_scores = [st.session_state.ans.get(i, 0) for i in range(66, 72)]
    if any(s == 3 for s in adhd_scores) or (sum(adhd_scores) >= 18 * 0.6):
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【注意状态预警】疑似 ADHD 特质。孩子大脑天生自带“降噪功能缺陷”，不要再骂他粗心了，他需要专业的脑功能整合训练。</div>", unsafe_allow_html=True)

    # 9. 身体状态预警 (73-78题)
    body_avg = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if body_avg > 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【身体状态预警】当前表现受生理代谢（如营养、过敏）影响。生理基础不稳，心智无法成长，建议从营养与节律层面修复。</div>", unsafe_allow_html=True)

    # 2. 雷达图绘制
    scores, labels = [], list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1)) # 转化为100分制展示
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(t=20, b=20, l=40, r=40))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<p style='font-size:12px; color:#90A4AE; text-align:center;'>注：分值越高，代表该维度的“负荷”或“风险”越大。</p>", unsafe_allow_html=True)

    # 3. 六大维度深度解析卡片 (匹配 0.8/1.8/3.0 分层逻辑)
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        # 匹配分值：0-0.8 优秀(绿/蓝), 0.9-1.8 预警(黄), 1.9-3.0 危险(红)
        if avg <= 0.8:
            color, idx = "#2E7D32", 0 # 稳固
        elif avg <= 1.8:
            color, idx = "#F9A825", 1 # 中位
        else:
            color, idx = "#C62828", 2 # 高分危险
            
        st.markdown(f"""
            <div style='padding:18px; border-radius:12px; background:white; border-left:6px solid {color}; margin-bottom:12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                <b style='color:{color};'>{dim}</b><br>
                <span style='color:#455A64; font-size:15px;'>{info['levels'][idx]}</span>
            </div>
        """, unsafe_allow_html=True)

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
