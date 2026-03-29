import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 视觉重构：品牌净空、首页锁定 ---
st.set_page_config(page_title="曹校长 脑科学专业版", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    .stApp { background: #F8F9FA; text-align: left !important; color: #455A64; }
    
    /* 首页锁定：禁止滑动 */
    .home-lock { height: 100vh; overflow: hidden; display: flex; flex-direction: column; justify-content: center; padding: 25px; background: white; }
    
    /* 曹校长三行标题 */
    .t1 { font-size: 16px; color: #90A4AE; font-weight: 500; }
    .t2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; }
    .t3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-top: 5px; }
    
    /* 引导语 */
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin: 30px 0; border-left: 5px solid #FF7043; padding-left: 20px; }
    
    /* 按钮与卡片 */
    div.stButton > button { border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700; background-color: #1A237E; color: white; border: none; width: 100%; }
    .warn-banner { padding: 25px; border-radius: 18px; margin-bottom: 25px; color: white; font-weight: 600; line-height: 1.8; text-align: left; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    
    .res-card { padding: 25px; border-radius: 18px; background: white; border: 1px solid #E0E0E0; border-left: 8px solid #1A237E; margin-bottom: 20px; line-height: 1.8; }
    .wx-card { background: #FFFFFF; padding: 30px; border-radius: 24px; border: 2px solid #E8EAF6; box-shadow: 0 12px 40px rgba(26,35,126,0.15); text-align: left; margin-top: 40px; }
    .benefit-row { font-size: 17px; font-weight: 700; color: #1A237E; margin: 15px 0; border-bottom: 1px dashed #E8EAF6; padding-bottom: 10px; }
    .rid-box { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 10px 30px; border-radius: 12px; border: 3px dashed #C62828; display: block; margin: 20px auto; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态与数据管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 结果页话术：7-9 维度特殊激活话术 (全量录入) ---
WARN_7 = """⚠️ 【最高级别红色警报】<br>
监测到孩子目前存在明显的生存危机或极度情绪创伤（如厌世念头、自伤、极度冷漠）。<br>
此时任何关于学习的督促都是在“火上浇油”。请务必立刻停止施压，寻求专业心理干预，确保生命安全是当前家庭的第一要务！"""

WARN_8 = """⚠️ 【脑特性深度预警】<br>
孩子表现出典型的高多动、冲动或注意力黑洞特质。这并非“态度不端正”，而是前额叶皮质执行功能发育的暂时性滞后。<br>
单纯的说教和惩罚只会破坏自尊，建议采用脑科学感统律动结合的行为管理方案进行“弯道超车”。"""

WARN_9 = """⚠️ 【底层生理地基预警】<br>
监测到孩子伴有明显的肠脑轴失调或慢性生理压力迹象（如长期过敏、睡眠呼吸障碍、眼圈发青、情绪易炸）。<br>
当身体处于慢性炎症或缺氧状态时，大脑会自动切换到“生存模式”而非“学习模式”。建议先进行生理节律的系统调理。"""

# --- 4. 页面流程 ---

# A. 首页 (锁定)
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

# B. 答题页 (略，请参照前文 1-85 题逻辑)

# C. 结果页 (滑动长图流)
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px;'>📸 提示：编号是唯一凭证，请【截屏保存】本页诊断。</div>", unsafe_allow_html=True)

    # --- 7-9 特殊警报逻辑 ---
    
    # 维度七：情绪红灯 (59-66题) -> 有任何一题选3分(总是)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown(f"<div class='warn-banner bg-red'>{WARN_7}</div>", unsafe_allow_html=True)
    
    # 维度八：ADHD 脑特性 (67-72题) -> 均分 >= 1.5
    adhd_score = sum(st.session_state.ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_score >= 1.5:
        st.markdown(f"<div class='warn-banner bg-orange'>{WARN_8}</div>", unsafe_allow_html=True)

    # 维度九：底层生理基础 (73-78题) -> 均分 >= 1.5
    bio_score = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_score >= 1.5:
        st.markdown(f"<div class='warn-banner bg-blue'>{WARN_9}</div>", unsafe_allow_html=True)

    # --- 1-6 维度长话术 (逻辑同前文) ---
    
    # --- 微信转化卡片 (100% 还原图片) ---
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
