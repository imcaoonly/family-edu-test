import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 核心视觉与 UI 重塑 (深度参考链接风格) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

# 强力注入 CSS，打造移动端高级感
st.markdown("""
    <style>
    /* 彻底清除官方元素 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* 页面基础背景 */
    .stApp { background-color: #FFFFFF; }
    
    /* 标题系统 (三行化) */
    .brand-box { text-align: center; margin-bottom: 40px; }
    .t1 { font-size: 42px; font-weight: 900; color: #1B5E20; letter-spacing: 2px; }
    .t2 { font-size: 34px; font-weight: 700; color: #2E7D32; margin-top: -10px; }
    .t3 { font-size: 18px; color: #999; border-top: 1.5px solid #F0F0F0; display: inline-block; padding-top: 10px; margin-top: 10px; }
    
    /* 暖心语卡片 */
    .warm-box { background: #F9FBF9; padding: 25px; border-radius: 20px; border-left: 5px solid #A5D6A7; color: #444; font-size: 18px; line-height: 1.8; margin-bottom: 30px; text-align: left; }
    
    /* 题目排版 (左对齐) */
    .q-text { font-size: 22px; font-weight: 600; color: #333; text-align: left !important; margin-bottom: 25px; line-height: 1.5; }
    
    /* 卡片式选项按钮 */
    div.stButton > button {
        width: 100%; border-radius: 15px; height: 65px; font-size: 18px !important;
        border: 2px solid #E8F5E9; background-color: #FAFAFA; color: #333;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); margin-bottom: 15px;
    }
    div.stButton > button:hover { border-color: #4CAF50; background-color: #F1F8E9; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    
    /* 报告卡片 */
    .result-card { background: #FFFFFF; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 25px; border-left: 8px solid #E0E0E0; }
    .high-risk { border-left-color: #D32F2F !important; background-color: #FFF5F5; border: 2px solid #FFEBEE; border-left-width: 8px; }
    .alert-banner { background: #D32F2F; color: white; padding: 20px; border-radius: 15px; font-weight: bold; margin-bottom: 25px; }
    
    /* 微信转化卡片 (深度定制) */
    .wx-card { background: #E8F5E9; border-radius: 25px; padding: 35px; text-align: center; margin-top: 40px; box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1); }
    .wx-promo { text-align: left; display: inline-block; margin: 20px 0; font-size: 19px; line-height: 2.2; color: #1B5E20; font-weight: 500; }
    .report-id-box { font-size: 40px; font-weight: 900; color: #D32F2F; background: white; padding: 15px 35px; border-radius: 15px; border: 3px dashed #D32F2F; display: inline-block; margin: 25px 0; letter-spacing: 3px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 连续 1-85 题库录入 (左对齐内容) ---
QS_LIST = [
    # 1-78 计分题 (部分展示，逻辑完整)
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。",
    # ... 此处请补齐 3-58 题 ...
    "提到上学或考试，有头痛腹痛等生理反应。", "拒绝社交，有明显的社交回避或社恐。",
    "老师反馈纪律性差、孤僻或难以融入集体。", "在学校没有可以倾诉、互助支持的朋友。",
    "对校园规则极度不耐受，有明显逆反心。", "公共场合表现出局促感或不合时宜行为。",
    "电子产品是爆发家庭冲突的最主要诱因。", "近期长时间不洗头不换衣，不在意个人卫生。",
    "食欲极端波动（暴食或长期厌食）。", "表达过消极厌世或“我消失了更好”的念头。",
    "身上有不明划痕，或拔头发、啃指甲见血。", "对未来不抱期待，拒绝讨论任何计划。",
    "睡眠节律彻底混乱，黑白颠倒。", "对最亲近的人也表现出极度冷漠和隔绝。",
    "提到学校或老师，浑身发抖或剧烈抵触。", "玩游戏专注，面对学习坐不住、易走神。",
    "安静环境下，也无法停止身体扭动或晃动。", "无法耐心等别人说完，经常抢话、插话。",
    "在排队或等待场合，表现出超越年龄的焦躁。", "短时记忆黑洞，刚交代的事转头就忘。",
    "做作业或听讲时，极易被微小动静吸引。", "依赖甜食面食，极度讨厌蔬菜。",
    "伴有长期口臭、肚子胀气、便秘或大便不成形。", "长期过敏体质（鼻炎、腺样体、湿疹等）。",
    "进食大量糖面后，莫名亢奋或情绪崩溃。", "睡觉张口呼吸、盗汗、磨牙或频繁翻身。",
    "睡眠充足但眼圈常年发青或水肿。"
]

# 补全 79-85 背景题
BG_QS = ["是否确诊过ADHD/抑郁？", "尝试过哪些方式（咨询/药物）？", "之前方法为何失效？", "最想解决的三个痛点？", "是否有勇气参与改变？", "是否预约专家解读？", "是否有兴趣了解系统方案？"]

# --- 3. 核心逻辑处理 ---
if 'idx' not in st.session_state:
    st.session_state.update({'step': 'home', 'idx': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

def next_q(val):
    st.session_state.ans[st.session_state.idx] = val
    st.session_state.idx += 1
    st.rerun()

# --- 4. 流程渲染 ---
if st.session_state.step == 'home':
    st.markdown("""<div class='brand-box'><div class='t1'>家庭教育</div><div class='t2'>十维深度探查表</div><div class='t3'>( 脑科学专业版 )</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='warm-box'>这场跨越心与脑的对话，请放空杂念，给孩子和自己一次被“看见”的机会。</div>""", unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'testing'; st.rerun()

elif st.session_state.step == 'testing':
    idx = st.session_state.idx
    st.progress((idx + 1) / 85)
    
    # 统一连续编号 1-85
    st.markdown(f"<div class='q-text'>{idx+1}. {QS_LIST[idx] if idx < 78 else BG_QS[idx-78]}</div>", unsafe_allow_html=True)
    
    if idx < 78:
        c1, c2 = st.columns(2)
        if c1.button("0 (从不)", use_container_width=True, key=f"q{idx}0"): next_q(0)
        if c2.button("1 (偶尔)", use_container_width=True, key=f"q{idx}1"): next_q(1)
        if c1.button("2 (经常)", use_container_width=True, key=f"q{idx}2"): next_q(2)
        if c2.button("3 (总是)", use_container_width=True, key=f"q{idx}3"): next_q(3)
    else:
        ans_text = st.text_input("请填写您的回答（或输入'无'）")
        if st.button("下一步" if idx < 84 else "生成最终报告", use_container_width=True):
            next_q(ans_text)
            if idx == 84: st.session_state.step = 'report'; st.rerun()
            
    if idx > 0:
        if st.button("⬅️ 返回上一题", type="secondary"): st.session_state.idx -= 1; st.rerun()

elif st.session_state.step == 'report':
    st.markdown("### 📊 深度诊断报告")
    
    # 模拟话术计算逻辑 (此处应补全 DIM_TEXTS 字典)
    dimensions = ["系统", "家长", "关系", "动力", "学业", "社会化"]
    for dim in dimensions:
        avg = random.uniform(0, 3) # 实际应根据 session_state.ans 计算
        is_high = avg >= 1.9
        card_class = "result-card high-risk" if is_high else "result-card"
        status = "危险/力竭" if is_high else ("预警/疲劳" if avg >= 0.9 else "稳固/优秀")
        
        st.markdown(f"""<div class='{card_class}'>
            <b style='font-size:18px;'>{dim}维度评分：{status}</b><br>
            <p style='margin-top:10px; color:#555;'>在此维度的表现揭示了您家庭中潜在的深度逻辑...</p>
        </div>""", unsafe_allow_html=True)

    # 微信转化区域
    st.markdown(f"""
    <div class='wx-card'>
        <p style='color:#1B5E20; font-size:18px; line-height:1.6;'>
            <b>这份报告揭示了孩子的求救，也看见了您的委屈。</b><br>其实，您不需要独自扛着。
        </p>
        <div class='wx-promo'>
            1️⃣ 十个维度个性化改善方案<br>
            2️⃣ 30 分钟 1V1 深度解析<br>
            3️⃣ 特惠 198 元 (原价 598 元)
        </div>
        <p style='margin-top:20px; font-weight:bold;'>添加时请备注生成的数字：</p>
        <div class='report-id-box'>{st.session_state.rid}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("👉 点击添加老师，预约深度诊断", "https://work.weixin.qq.com/ca/...", use_container_width=True)
