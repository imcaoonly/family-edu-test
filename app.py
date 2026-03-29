import streamlit as st
import plotly.graph_objects as go
import random

# --- 1. 视觉锁定与样式 ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .home-lock { height: 100vh; overflow: hidden; display: flex; flex-direction: column; justify-content: center; }
    .l1 { color: #90A4AE; font-size: 16px; }
    .l2 { color: #1A237E; font-size: 38px; font-weight: 900; margin: 5px 0; }
    .l3 { color: #FF7043; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .glass-box {
        background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px);
        padding: 20px; border-radius: 15px; color: #37474F; line-height: 1.8;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); margin-bottom: 20px;
    }
    .stButton > button { width: 100%; text-align: left !important; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .rid-box { border: 2px dashed #FF5252; padding: 15px; text-align: center; margin: 20px 0; border-radius: 8px; background-color: #FFF5F5; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 初始化数据 ---
if 'step' not in st.session_state: st.session_state.step = "HOME"
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'current_q' not in st.session_state: st.session_state.current_q = 1
if 'rid' not in st.session_state: st.session_state.rid = random.randint(100000, 999999) # 6位验证码 

# --- 3. 完整题库 (已修复引号冲突) [cite: 6-83] ---
QUESTIONS = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。",
    "长辈深度参与管教，经常推翻您的决定。", "父母教育标准不一，经常‘一宽一严’。",
    "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。",
    "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。",
    "面对孩子问题，感到深深的无力感。", "觉得若不是为了孩子，生活会更精彩自由。",
    "吼叫后陷入‘后悔自责—过度补偿’循环。", "觉得孩子某些性格与您讨厌的特质一模一样。",
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
    "经常说‘没意思、没劲’，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。",
    "生命力在萎缩，越来越像一个‘空心人’。", "即使做感兴趣的事，也难以保持长久热情。",
    "近期对以前喜欢的活动表现出明显冷感。",
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。",
    "写字姿势扭曲、力道极重，容易疲劳。", "经常‘转头就忘’，频繁丢失课本或文具。",
    "指令‘左耳进右耳出’，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。",
    "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。",
    "坐姿东倒西歪，写作业时头低得非常近。", "处理多步骤指令时，中途断掉就直接放弃。",
    "无法控制地咬指甲、咬衣领或笔头。",
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。",
    "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。",
    "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。",
    "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。",
    "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。",
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。",
    "表达过消极厌世或‘我消失了更好’的念头。", "身上有不明划痕，或拔头发、啃指甲见血。",
    "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。",
    "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。",
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。",
    "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。",
    "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。",
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。",
    "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。"
]

# --- 4. 路由逻辑 ---
if st.session_state.step == "HOME":
    st.markdown('<div class="home-lock">', unsafe_allow_html=True)
    st.markdown('<div class="l1">曹校长 脑科学专业版</div>', unsafe_allow_html=True)
    st.markdown('<div class="l2">家庭教育</div>', unsafe_allow_html=True)
    st.markdown('<div class="l3">十维深度探查表</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glass-box">{st.session_state.get("intro", "这是一场跨越心与脑的对话。<br>你好，我是曹校长。<br><br>接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。")}</div>', unsafe_allow_html=True) # [cite: 151-154]
    if st.button("👉 开始测评"):
        st.session_state.step = "QUIZ"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "QUIZ":
    idx = st.session_state.current_q
    if idx <= 78:
        st.write(f"进度：{idx} / 85")
        st.subheader(QUESTIONS[idx-1])
        for i, lbl in enumerate(["从不", "偶尔", "经常", "总是"]): # [cite: 4, 95-98]
            if st.button(lbl, key=f"q{idx}_{i}"):
                st.session_state.answers[idx] = i
                st.session_state.current_q += 1
                st.rerun()
    else:
        st.success("核心测评已完成，请点击下方按钮生成报告。")
        if st.button("生成深度分析报告"):
            st.session_state.step = "RESULT"
            st.rerun()

elif st.session_state.step == "RESULT":
    st.markdown("### 📸 您的深度诊断报告")
    ans = st.session_state.answers
    
    # 维度计分 [cite: 101, 107]
    def avg(s, e): return sum(ans.get(i, 0) for i in range(s, e+1)) / (e - s + 1)
    dims = {"系统": avg(1,8), "家长": avg(9,18), "关系": avg(19,28), "动力": avg(29,37), "学业": avg(38,48), "社会化": avg(49,58)}

    # 雷达图 [cite: 101]
    fig = go.Figure(data=go.Scatterpolar(r=list(dims.values()), theta=list(dims.keys()), fill='toself', line_color='#1A237E'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # 红灯预警 [cite: 143]
    if any(ans.get(i, 0) == 3 for i in range(59, 67)):
        st.error("🔴 红灯警报：当前孩子情绪安全水位极低，建议暂停学业施压，优先进行情感固着。")

    # 转化区 [cite: 157-164]
    st.markdown(f"""
        <div style="border: 2px solid #1A237E; padding: 20px; border-radius: 15px; background: #F8F9FA;">
            <p>这份报告揭示了孩子的求救，也看见了您的委屈。其实，您不需要独自扛着。</p>
            <div class="rid-box">
                <span style="color: #D32F2F; font-size: 28px; font-weight: 900; letter-spacing: 5px;">{st.session_state.rid}</span><br>
                <small>添加微信请备注此 6 位编号</small>
            </div>
            <div style="background-color: #1A237E; color: white; text-align: center; padding: 12px; border-radius: 10px; font-weight: bold;">
                👉 添加曹校长，领取 1V1 解析福利
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。") #
