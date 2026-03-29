import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 样式与视觉定制 (彻底清爽 & 三行标题) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底隐藏所有官方元素 */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    
    /* 标题严格三行美化 */
    .title-box { text-align: center; color: #1B5E20; margin-bottom: 30px; }
    .t-main { font-size: 36px; font-weight: 800; line-height: 1.2; }
    .t-sub { font-size: 30px; font-weight: 700; line-height: 1.2; }
    .t-mini { font-size: 16px; color: #888; border-top: 1px solid #eee; display: inline-block; padding-top: 8px; margin-top: 10px; }
    
    /* 题目与卡片美化 */
    .q-text { font-size: 20px; font-weight: 600; color: #333; margin: 25px 0; line-height: 1.5; }
    .report-card { padding: 20px; border-radius: 12px; background-color: #F9F9F9; border-left: 6px solid #2E7D32; margin-bottom: 20px; }
    .alert-red { padding: 20px; border-radius: 12px; background-color: #FFF5F5; border-left: 6px solid #D32F2F; color: #B71C1C; font-weight: bold; }
    
    /* 微信转化板块强化 */
    .wx-section { background: #FFFFFF; border: 2px solid #E8F5E9; border-radius: 15px; padding: 25px; text-align: center; margin-top: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .report-id { font-size: 34px; font-weight: 900; color: #D32F2F; background: #FFF0F0; padding: 10px 25px; border-radius: 10px; border: 2px dashed #D32F2F; display: inline-block; margin: 20px 0; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心数据 (手动补全，杜绝 NameError) ---
# 计分题 1-78
QS_LIST = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。",
    "长辈深度参与管教，经常推翻您的决定。", "父母教育标准不一，经常“一宽一严”。",
    "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。",
    "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。",
    "面对孩子问题，感到深深的无力感。", "觉得若不是为了孩子，生活会更精彩自由。",
    "吼叫后陷入“后悔自责—过度补偿”循环。", "觉得孩子某些性格与您讨厌的特质一模一样。",
    "极度在意老师或他人对孩子的负面评价。", "孩子表现与个人价值感挂钩，不出色感失败。",
    "管教时心跳加快、胸闷、手抖或大脑空白。", "觉得带孩子是孤军奋战，配偶无实质支持。",
    "睡眠质量差，入睡困难或报复性熬夜。", "内心焦虑、烦躁，很难获得平静。",
    "除了聊学习吃睡，很难进行开心闲聊。", "在校受委屈或丢脸会选择隐瞒，不告知。",
    "对您进房间或动用其物品有明显反感。", "经常反锁屋门，抗拒询问或靠近。",
    "情绪爆发时，本能想靠讲道理或强行压制。", "犯错后第一反应是撒谎、推诿或冷战。",
    "会翻看手机或日记来了解其真实想法。", "不敢在您面前表达真实不满、愤怒或意见。",
    "抱怨在家里没自由，或想要早点离家。", "沟通有明显防御性，您一开口他就烦。",
    "面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，立刻情绪崩塌或放弃。",
    "过度在意评价，因别人一句话就郁郁寡欢。", "对学习以外的事物也兴致索然，没爱好。",
    "经常说没意思、没劲，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。",
    "生命力在萎缩，越来越像一个“空心人”。", "即使做感兴趣的事，也难以保持长久热情。",
    "近期对以前喜欢的活动表现出明显冷感。", "磨蹭拖延，通过各种准备动作逃避开始作业。",
    "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。",
    "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。",
    "阅读或抄写频繁跳行、漏字或笔画写反。", "面对复杂任务，完全不知道从哪下手。",
    "启动效率极低，反应速度明显慢于同龄人。", "坐姿东倒西歪，写作业时头低得非常近。",
    "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。",
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。",
    "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。",
    "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。",
    "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。",
    "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。",
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。",
    "表达过消极厌世或“我消失了更好”的念头。", "身上有不明划痕，或拔头发、啃指甲见血。",
    "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。",
    "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。",
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。",
    "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。",
    "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。",
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。",
    "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。"
]

# 背景题
BG_LIST = [
    ("79. 是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
    ("80. 为了解决问题，您尝试过哪些方式？", ["心理咨询", "药物治疗", "增加严管", "父母课", "其他"], "multi"),
    ("81. 之前方法未生效的原因？", ["不落地", "不系统", "没法坚持", "不配合", "缺陪跑"], "multi"),
    ("82. 目前最想解决的三个痛点？", ["关系/叛逆", "厌学/手机", "专注力/成绩", "情绪", "社交"], "multi"),
    ("83. 您是否有勇气参与改变？", ["非常愿意", "愿意但需指导", "纠结", "只想改孩子"], "single"),
    ("84. 是否预约专家解读？", ["是", "否"], "single"),
    ("85. 是否有兴趣了解系统方案？", ["是", "否"], "single")
]

# --- 3. 状态与逻辑逻辑 (彻底修复冒号与变量报错) ---
if 'idx' not in st.session_state:
    st.session_state.update({'step': 'home', 'idx': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

def next_q(val):
    st.session_state.ans[st.session_state.idx] = val
    st.session_state.idx += 1
    st.rerun()

# --- 4. 界面渲染 ---
if st.session_state.step == 'home':
    st.markdown("""
        <div class='title-box'>
            <div class='t-main'>家庭教育</div>
            <div class='t-sub'>十维深度探查表</div>
            <div class='t-mini'>( 脑科学专业版 )</div>
        </div>
        """, unsafe_allow_html=True)
    st.info("一场跨越心与脑的对话，请放空杂念，给孩子和自己一次被“看见”的机会。")
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'testing'; st.rerun()

elif st.session_state.step == 'testing':
    idx = st.session_state.idx
    st.progress((idx + 1) / 85)
    
    if idx < 78:
        st.write(f"**第 {idx+1} 题 / 共 85 题**")
        st.markdown(f"<div class='q-text'>{idx+1}. {QS_LIST[idx]}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("0 (从不)", use_container_width=True, key=f"ans_{idx}_0"): next_q(0)
        if c2.button("1 (偶尔)", use_container_width=True, key=f"ans_{idx}_1"): next_q(1)
        if c1.button("2 (经常)", use_container_width=True, key=f"ans_{idx}_2"): next_q(2)
        if c2.button("3 (总是)", use_container_width=True, key=f"ans_{idx}_3"): next_q(3)
    else:
        q_txt, opts, mode = BG_LIST[idx-78]
        st.markdown(f"### {q_txt}")
        u_val = st.multiselect("多选", opts) if mode=="multi" else st.radio("单选", opts, index=None)
        if st.button("查看诊断报告" if idx==84 else "下一步", use_container_width=True, disabled=not u_val):
            st.session_state.ans[idx] = u_val
            if idx == 84: st.session_state.step = 'report'
            else: st.session_state.idx += 1
            st.rerun()
    
    if idx > 0: # 严格检查冒号
        if st.button("⬅️ 返回上一题"):
            st.session_state.idx -= 1
            st.rerun()

elif st.session_state.step == 'report':
    st.header("📊 深度诊断结果")
    
    # 维度定义
    DIM_MAP = {
        "系统": (range(0,8), "早期依恋与稳定性"), "家长": (range(8,18), "父母心理能量"),
        "关系": (range(18,28), "情感通道状态"), "动力": (range(28,37), "生命力激活"),
        "学业": (range(37,48), "执行功能损耗"), "社会化": (range(48,58), "社交与现实自信")
    }
    
    scores = {}
    for name, (idxs, meaning) in DIM_MAP.items():
        avg = sum(st.session_state.ans.get(i,0) for i in idxs) / len(idxs)
        scores[name] = avg
        level = "高分危险" if avg >= 1.9 else ("中位预警" if avg >= 0.9 else "稳固优秀")
        color = "#D32F2F" if avg >= 1.9 else ("#F57C00" if avg >= 0.9 else "#388E3C")
        
        with st.expander(f"🔍 {name}维度分析：{level}", expanded=True):
            st.markdown(f"<div class='report-card' style='border-left-color:{color}'><b>深度解读：</b>{meaning} (均分:{avg:.2f})</div>", unsafe_allow_html=True)

    # 专项预警逻辑
    st.subheader("🚩 关键风险提示")
    # 7. 情绪红灯
    if any(st.session_state.ans.get(i) == 3 for i in range(58, 66)):
        st.markdown("<div class='alert-red'>🚨 红灯警报：孩子情绪水位极低，请立即停止施压，优先情感固着！</div>", unsafe_allow_html=True)
    # 9. 底层营养
    if sum(st.session_state.ans.get(i,0) for i in range(72, 78))/6 > 1.
