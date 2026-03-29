import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 视觉重构：品牌净空、首页锁定、左对齐 ---
st.set_page_config(page_title="曹校长 脑科学专业版", layout="centered")

st.markdown("""
    <style>
    /* 彻底遮蔽原网站品牌露出 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 全局样式：左对齐、深灰蓝 */
    .stApp { background: #F8F9FA; text-align: left !important; color: #455A64; font-family: "PingFang SC", sans-serif; }
    
    /* 首页锁定逻辑：禁止滑动 */
    .home-lock { 
        height: 100vh; overflow: hidden; position: fixed; width: 100%; top: 0; left: 0;
        display: flex; flex-direction: column; justify-content: center; padding: 40px 25px;
        background: white; z-index: 9999;
    }
    
    /* 曹校长三行标题规范 */
    .t1 { font-size: 16px; color: #90A4AE; font-weight: 500; margin-bottom: 5px; }
    .t2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; }
    .t3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-top: 5px; }
    
    /* 曹校长版引导语 */
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin: 30px 0; border-left: 5px solid #FF7043; padding-left: 20px; }
    
    /* 题目与选项布局 */
    .q-text { font-size: 22px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0 20px 0; }
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.2s; width: 100%;
    }
    div.stButton > button:active { transform: scale(0.97); background-color: #0D47A1; }
    
    /* 结果页报警 Banner */
    .warn-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; line-height: 1.6; text-align: left; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    
    /* 1-6维度解析卡片：深蓝左侧强调 */
    .res-card { padding: 25px; border-radius: 18px; background: white; border: 1px solid #E0E0E0; border-left: 8px solid #1A237E; margin-bottom: 20px; line-height: 1.8; }
    
    /* 微信转化卡片：还原图片要求 */
    .wx-card { background: #FFFFFF; padding: 30px; border-radius: 24px; border: 2px solid #E8EAF6; box-shadow: 0 12px 40px rgba(26,35,126,0.15); text-align: left; margin-top: 40px; }
    .benefit-row { font-size: 17px; font-weight: 700; color: #1A237E; margin: 15px 0; border-bottom: 1px dashed #E8EAF6; padding-bottom: 10px; }
    .rid-box { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 10px 30px; border-radius: 12px; border: 3px dashed #C62828; display: block; margin: 20px auto; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 维度话术数据库 (100% 原版长文案) ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "levels": [
        "【稳固】家庭系统运行稳健，夫妻关系与亲子关系各司其职。孩子拥有安全感底色，能感受到规则的保护而非束缚。即使面对外界压力，家庭内部也能提供有效的缓冲。",
        "【预警】系统平衡正在打破，家庭成员间开始出现隐形的控制或过度卷入。地基出现细微裂缝，孩子开始通过“问题行为”来分担家庭系统的焦虑，承压已接近临界点。",
        "【危险】地基严重动摇。系统内部功能紊乱，可能存在长期的冷暴力、过度指责或依恋断裂。孩子缺乏基本的安全感，大脑常年处于“战或逃”生存模式，无法调动能量用于学习。"
    ]},
    "家长维度": {"range": range(8,18), "levels": [
        "【优秀】家长具备极高的情绪自控力与能量带宽。能够识别孩子的行为动机，而非仅仅反应于表面症状。管教温和而坚定，能作为孩子的“情绪容器”。",
        "【内耗】家长长期处于高压状态，教育理念在“放任”与“高压”间反复横跳。存在严重的内耗，管教时常伴随生理性的无力感，孩子的情绪容易引发家长的二次崩溃。",
        "【力竭】家长已处于心理力竭（Burnout）状态。对孩子的管教已丧失信心，引导功能基本瘫痪。长期的挫败感导致家长在潜意识里开始回避与孩子的深度链接，教育动作已变形。"
    ]},
    "关系维度": {"range": range(18,28), "levels": [
        "【信任】亲子间存在良性的情感双向流动。沟通顺畅，边界清晰，孩子愿意主动分享困难。信任感是家庭教育最坚硬的护城河，孩子具备极强的复原力。",
        "【防御】孩子开始关闭心门，沟通仅维持在功能层面。防御性增强，家长的建议常被误读为攻击。关系中充满了隐形的拉锯感。",
        "【断联】情感连接已名存实亡。孩子表现出明显的逃离倾向或极端的对立违抗。任何教育动作在此时都会引发剧烈的排斥，孩子在心理上已将家长视为“敌人”。"
    ]},
    "动力维度": {"range": range(28,37), "levels": [
        "【旺盛】孩子具备天然的生命力与探索欲。对世界保持好奇，具备一定的抗挫力。学习对于孩子而言是自我实现的途径，而非外在的苦役。",
        "【下行】动力开始萎缩，出现“空心化”苗头。学习变成为了应付家长，成就感来源单一。面对困难时极易放弃，需要大量的外在推力才能维持运转。",
        "【枯竭】动力彻底熄火。自我价值感降至冰点，对未来丧失想象力。表现为极度的习得性无助，对任何激励手段都产生免疫，甚至出现厌世或摆烂心态。"
    ]},
    "学业维度": {"range": range(37,48), "levels": [
        "【高效】脑认知功能开发良好，执行功能能够支撑当下的学业强度。学习过程伴随正向反馈，具备良好的时间管理能力。",
        "【疲劳】生理性疲劳导致执行功能受损。大脑像一台发热的电脑，运行缓慢。努力程度很高但产出低下，注意力分散明显，学业压力已开始侵蚀心理健康。",
        "【宕机】大脑由于过度过载已启动保护性关闭。对书本、学校产生强烈的生理性厌恶（如头痛、恶心）。执行功能崩盘，已无法完成基本的学业任务。"
    ]},
    "社会化": {"range": range(48,58), "levels": [
        "【自如】具备正常的规则意识与社交弹性。能够处理同伴冲突，理解社会规范。在集体中能找到归属感，具备同理心。",
        "【退缩】社交半径显著萎缩，现实社交回避明显。过度依赖屏幕或二次元世界来获取社交补偿。在群体中表现敏感、自卑或过度防御。",
        "【受损】社会功能严重受损。拒绝参与现实社交，可能存在严重的社交恐惧或由于长期的挫败感导致的攻击性社交模式。无法在集体环境中正常生存。"
    ]}
}

# --- 4. 流程引擎 ---

# A. 首页 (锁定不滚动)
if st.session_state.step == 'home':
    st.markdown(f"""
        <div class='home-lock'>
            <div class='t1'>曹校长 脑科学专业版</div>
            <div class='t2'>家庭教育</div>
            <div class='t3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是曹校长。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# B. 答题页 (线性答题 + 回溯)
elif st.session_state.step == 'quiz':
    # 请务必在此处将 1-85 题完整列表填入
    QS = [f"这里是第 {i+1} 题的具体内容..." for i in range(85)]
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.markdown(f"<div class='q-text'>{cur+1}. {QS[cur]}</div>", unsafe_allow_html=True)
    
    opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
    for i, (txt, val) in enumerate(opts):
        if st.button(txt, key=f"q_{cur}_{i}"):
            st.session_state.ans[cur] = val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.cur += 1
            st.rerun()
    
    if cur > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ 回到上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页 (滑动长图流)
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px;'>📸 提示：编号是唯一凭证，请【截屏保存】本页诊断。</div>", unsafe_allow_html=True)
    
    # [此处绘制雷达图，代码省略以保持简洁，逻辑参考前文]

    # 7-9 维度原版报警话术 (59-78题判断)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【最高级别红色警报】检测到生存危机或极度情绪创伤（如厌世、自伤）。此时任何学业督促都是“火上浇油”。请立刻停止施压，寻求干预，生命安全是第一要务！</div>", unsafe_allow_html=True)
    
    # 1-6 维度长话术分层展示
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    # 微信转化卡片 (还原图片)
    st.markdown(f"""
        <div class='wx-card'>
            <p style='font-size:18px;'>这份报告揭示了孩子的求救，也看见了您的委屈。<br>其实，您不需要独自扛着。</p>
            <p style='font-weight:bold; margin-top:20px; color:#1A237E;'>添加微信您可以获得：</p>
            <div class='benefit-row'>1. 十个维度个性化改善方案</div>
            <div class='benefit-row'>2. 30 分钟 1V1 深度解析</div>
            <div class='benefit-row'>3. 特惠 198 元（原价 598 元）</div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='color:#546E7A; font-size:15px; text-align:center;'>添加时请备注生成的数字</p>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold; text-align:center; margin-top:15px;">👉 点击添加曹校长，领取以上福利</a>
        </div>
    """, unsafe_allow_html=True)
