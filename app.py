import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 终极 UI 适配（强制按钮等宽 + 像素级去白） ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    /* 1. 彻底干掉顶部白条 */
    .block-container { padding-top: 0rem !important; }
    div[data-testid="stVerticalBlock"] > div:first-child { margin-top: -70px !important; }
    header, footer {visibility: hidden !important;}

    /* 2. 强制所有交互组件（按钮、多选、单选）100% 宽度 */
    div.row-widget.stButton > button, 
    div[data-testid="stForm"] button,
    .stMultiSelect, .stSelectbox, .stRadio, div.row-widget {
        width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* 3. 按钮美化：确保和卡片一样宽 */
    div.stButton > button {
        border-radius: 12px !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        background-color: #1A237E !important;
        color: white !important;
        border: none !important;
        display: block !important;
    }
    
    /* 返回按钮样式 */
    button[kind="secondary"] { 
        color: #FF7043 !important; 
        border: 2px solid #FF7043 !important; 
        background: transparent !important;
        height: 50px !important;
    }

    .stApp { background: #F8F9FA; }
    .home-box {
        background: white; border-radius: 20px; padding: 25px 20px;
        margin: 0 auto; box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        max-width: 500px; width: 100%;
    }

    .t2 { font-size: 32px; font-weight: 800; color: #1A237E; line-height: 1.1; }
    .q-title { font-size: 19px; font-weight: 600; color: #263238; margin: 25px 0; line-height: 1.5; }
    .em-red { color: #E53935 !important; font-weight: 800; }
    
    /* 进度条 */
    .stProgress > div > div > div > div { background-color: #FF7043 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态初始化 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 1-85 题全量题库 ---
QS_CONTENT = [
    "1. 3岁前，主要抚养人频繁更换或长期中断。", "2. 早期曾连续2周以上见不到核心抚养人。",
    "3. 长辈深度参与管教，经常推翻您的决定。", "4. 父母教育标准不一，经常“一宽一严”。",
    "5. 幼年受委屈时极度粘人，无法离开抚养人。", "6. 近两年经历搬家、转学或财务大变动。",
    "7. 处理人际关系(如婆媳、夫妻矛盾)心力交瘁。", "8. 家人虽同住但各忙各的，缺乏交心时刻。",
    "9. 面对孩子问题，感到深深的无力感。", "10. 觉得若不是为了孩子，生活会更精彩自由。",
    "11. 吼叫后陷入“后悔自责-过度补偿”循环。", "12. 觉得孩子某些性格与您讨厌的特质一模一样。",
    "13. 极度在意老师或他人对孩子的负面评价。", "14. 孩子表现与个人价值感挂钩。",
    "15. 管教时心跳加快、胸闷、手抖或大脑空白。", "16. 觉得带孩子是孤军奋战，配偶无实质支持。",
    "17. 睡眠质量差，入睡困难或报复性熬夜。", "18. 内心焦虑、烦躁，很难获得平静。",
    "19. 除了聊学习吃睡，很难进行开心闲聊。", "20. 在校受委屈或丢脸会选择隐瞒，不告知。",
    "21. 对您进房间或动用其物品有明显反感。", "22. 经常反锁屋门，抗拒询问或靠近。",
    "23. 情绪爆发时，本能想靠讲道理或强行压制。", "24. 犯错后第一反应是撒谎、推诿或冷战。",
    "25. 会翻看手机或日记来了解其真实想法。", "26. 不敢在您面前表达真实不满、愤怒或意见。",
    "27. 抱怨在家里没自由，或想要早点离家。", "28. 沟通有明显防御性，您一开口他就烦。",
    "29. 面对挑战，还没做就觉得肯定不行，想退缩。", "30. 游戏输了或遇难题，立刻情绪崩塌或放弃。",
    "31. 过度在意评价，因别人一句话就郁郁欢欢。", "32. 对学习以外的事物也兴致索然，没爱好。",
    "33. 经常说没意思、没劲，感到空虚。", "34. 要求极高且不容许失败，稍不如意就否定自己。",
    "35. 生命力在萎缩，越来越像一个“空心人”。", "36. 即使做感兴趣的事，也难以保持长久热情。",
    "37. 近期对以前喜欢的活动表现出明显冷感。", "38. 磨蹭拖延，通过各种准备动作逃避开始作业。",
    "39. 写作业时神游发呆或手脚小动作不停。", "40. 写字姿势扭曲、力道极重，容易疲劳。",
    "41. 经常“转头就忘”，频繁丢失课本或文具。", "42. 指令“左耳进耳出”，吼几遍才有反应。",
    "43. 阅读或抄写频繁跳行、漏字。", "44. 面对复杂任务，完全不知道从哪下手。",
    "45. 启动效率极低，反应速度明显慢于同龄人。", "46. 坐姿东倒西歪，写作业时头低得非常近。",
    "47. 处理多步骤指令时，中途断掉就直接放弃。", "48. 无法控制地咬指甲、咬衣领或笔头。",
    "49. 电子屏幕占据除学习外的绝大部分时间。", "50. 收手机时出现剧烈情绪爆发或肢体对抗。",
    "51. 为了玩手机经常撒谎，或熬夜偷玩。", "52. 提到上学或考试，有头痛腹痛等生理反应。",
    "53. 拒绝社交，有明显的社交回避或社恐。", "54. 老师反馈纪律性差、孤僻或难以融入集体。",
    "55. 在学校没有可以倾诉、互助支持的朋友。", "56. 对校园规则极度不耐受，有明显逆反心。",
    "57. 公共场合表现出局促感或不合时宜行为。", "58. 电子产品是爆发家庭冲突的最主要诱因。",
    "59. 近期长时间不洗头不换衣，不在意个人卫生。", "60. 食欲极端波动(暴食或长期厌食)。",
    "61. 表达过消极厌世或“我消失了更好”的念头。", "62. 身上有不明划痕，或拔头发、掐自己等行为。",
    "63. 对未来不抱期待，拒绝讨论任何计划。", "64. 睡眠节律彻底混乱，黑白颠倒。",
    "65. 对最亲近的人也表现出极度冷漠和隔绝。", "66. 提到学校或老师，浑身发抖或剧烈抵触。",
    "67. 玩游戏专注，面对学习坐不住、易走神。", "68. 安静环境下，也无法停止身体扭动或晃动。",
    "69. 无法耐心等别人说完，经常抢话、插话。", "70. 在排队或等待场合，表现出超越年龄的焦躁。",
    "71. 短时记忆黑洞，刚交代的事转头就忘。", "72. 做作业或听讲时，极易被微小动静吸引。",
    "73. 依赖甜食面食，极度讨厌蔬菜。", "74. 伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "75. 长期过敏体质(鼻炎、腺样体、湿疹等)。", "76. 进食大量糖面后，莫名亢奋或情绪崩溃。",
    "77. 睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "78. 睡眠充足但眼圈常年发青或水肿。"
]

BG_QS = [
    {"q": "79. 孩子是否有过确诊？", "type": "multi", "opts": ["ADHD", "抑郁/焦虑", "其他", "暂无"]},
    {"q": "80. 为了解决问题，您尝试过哪些方式？", "type": "multi", "opts": ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"]},
    {"q": "81. 之前方法未彻底生效的原因？", "type": "multi", "opts": ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏陪跑"]},
    {"q": "82. 目前最迫切想解决的痛点？", "type": "multi", "opts": ["关系焦虑", "厌学崩盘", "专注力差", "情绪易炸", "手机成瘾"]},
    {"q": "83. 您是否有勇气参与改变？", "type": "single", "opts": ["有", "有，但需指导", "纠结", "只想改孩子"]},
    {"q": "84. 您是否愿预约专业解读？", "type": "single", "opts": ["是", "否"]},
    {"q": "85. 是否有兴趣了解长期扭转方案？", "type": "single", "opts": ["是", "否"]}
]
# --- 4. 维度定义与解析文案 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "texts": [
        "【稳固】家庭系统运行稳健，孩子拥有安全感底色。即使面对外界压力，家庭内部也能提供有效的缓冲。",
        "【预警】系统平衡正在打破，地基出现细微裂缝，孩子开始通过“问题行为”来分担家庭系统的焦虑。",
        "【危险】地基严重动摇。孩子大脑常年处于“战或逃”生存模式，无法调动能量用于学习。"
    ]},
    "家长维度": {"range": range(8,18), "texts": [
        "【优秀】能量充沛，情绪自控力强。能够识别孩子的行为动机，管教温和而坚定。",
        "【内耗】内耗严重，管教伴随生理性无力。长期的焦虑导致家长就像亮起黄灯的仪表盘。",
        "【力竭】心理力竭。对管教已丧失信心，引导功能瘫痪，在潜意识里回避与孩子的深度链接。"
    ]},
    "关系维度": {"range": range(18,28), "texts": [
        "【信任】沟通畅通，边界清晰信任高。关系中不存在控制感，是孩子复原力的源头。",
        "【防御】防御性增强。孩子正在慢慢关上心门，若不更换沟通频率，他会习惯性在心理隔离。",
        "【断联】情感断联。你们之间现在是“信号屏蔽”状态。不疏通情感，所有的教育都是无效功。"
    ]},
    "动力维度": {"range": range(28,37), "texts": [
        "【旺盛】胜负欲强，生命力旺盛。颓废只是“暂时的死机”，重装系统就能跑起来。",
        "【下行】待机状态，缺乏持续推力。这种状态最容易在初高中阶段彻底熄火。",
        "【枯竭】动力彻底枯竭。已进入“节能模式”，对外界失去探索欲。需要通过底层激活让他活过来。"
    ]},
    "学业维度": {"range": range(37,48), "texts": [
        "【高效】脑硬件高配，执行功能没问题。现在的波动纯粹是情绪或态度的感冒。",
        "【疲劳】高代偿维持学业。努力很高产出低下。压力一旦超限会迅速厌学崩盘。",
        "【宕机】CPU 过载，宕机保护性关闭。这是大脑苦苦支撑的生理信号。"
    ]},
    "社会化": {"range": range(48,58), "texts": [
        "【自如】规则意识强，渴望社交归属感。这种链接是我们后期将他从手机拉回现实的最强抓手。",
        "【退缩】屏幕占据生命，现实社交回避。舒适区在萎缩，在虚拟世界寻找安全感。",
        "【受损】现实中找不到成就感。拒绝上学或老师极度抵触。需要重建他的现实社交自信。"
    ]}
}

# --- 5. 核心逻辑引擎 ---
if st.session_state.step == 'home':
    st.markdown("<div class='home-box'>", unsafe_allow_html=True)
    st.markdown("<div class='t1'>曹校长 脑科学专业版</div><div class='t2'>家庭教育</div><div class='t3'>十维深度探查表</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#546E7A; line-height:1.8; margin:25px 0;'>你好，我是曹校长。这是一场跨越心与脑的对话。接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。</div>", unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", key="start_btn"):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    # 强制等宽进度条渲染
    progress = int((cur / 85) * 100)
    st.markdown(f'<div style="width:100%; background:#ECEFF1; height:8px; margin-bottom:20px; border-radius:10px;"><div style="width:{progress}%; background:#FF7043; height:8px; border-radius:10px; transition:0.3s;"></div></div>', unsafe_allow_html=True)
    
    st.markdown("<div class='home-box'>", unsafe_allow_html=True)
    
    # 1-78题：分值题逻辑
    if cur < 78:
        st.markdown(f"<div class='q-title'>{QS_CONTENT[cur]}</div>", unsafe_allow_html=True)
        for label, val in [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]:
            if st.button(label, key=f"q_{cur}_{val}"):
                st.session_state.ans[cur] = val
                st.session_state.cur += 1
                st.rerun()
    # 79-85题：背景题逻辑 (强制校验必填)
    else:
        q = BG_QS[cur-78]
        st.markdown(f"<div class='q-title'>{q['q']}</div>", unsafe_allow_html=True)
        
        if q['type'] == 'multi':
            sel = st.multiselect("请至少选择一项", q['opts'], key=f"multi_{cur}")
            if st.button("确认进入下一题", key=f"next_{cur}"):
                if not sel: # 拦截逻辑
                    st.warning("⚠️ 此项为必填，请选择后再点击。")
                else:
                    st.session_state.ans[cur] = sel
                    if cur == 84: st.session_state.step = 'report'
                    else: st.session_state.cur += 1
                    st.rerun()
        else:
            sel = st.radio("请选择一项", q['opts'], key=f"radio_{cur}", index=None)
            if st.button("确认进入下一题", key=f"next_{cur}"):
                if sel is None: # 拦截逻辑
                    st.warning("⚠️ 此项为必填，请选择后再点击。")
                else:
                    st.session_state.ans[cur] = sel
                    if cur == 84: st.session_state.step = 'report'
                    else: st.session_state.cur += 1
                    st.rerun()

    # 返回按钮：强制全宽
    if cur > 0:
        st.write("---")
        if st.button("⬅ 返回上一题", key=f"back_{cur}", kind="secondary"):
            st.session_state.cur -= 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == 'report':
    ans = st.session_state.ans
    # 报告页压实顶部
    st.markdown("<div style='margin-top:-35px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='home-box'>", unsafe_allow_html=True)
    st.markdown("<div class='t2' style='text-align:center;'>报告解析</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#90A4AE; text-align:center; margin-bottom:15px;'>专属编号：{st.session_state.rid}</div>", unsafe_allow_html=True)

    # 雷达图渲染
    categories = list(DIM_DATA.keys())
    values = [sum(ans.get(i, 0) for i in d['range']) / len(d['range']) for d in DIM_DATA.values()]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(26, 35, 126, 0.2)', line=dict(color='#1A237E', width=2)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False, height=320, margin=dict(l=30, r=30, t=30, b=30))
    st.plotly_chart(fig, use_container_width=True)

    # 严重程度自动分色卡片
    for name, d in DIM_DATA.items():
        score = sum(ans.get(i, 0) for i in d['range']) / len(d['range'])
        if score >= 1.8: cls, lv = "lv-red", 2
        elif score >= 0.8: cls, lv = "lv-orange", 1
        else: cls, lv = "lv-green", 0
        st.markdown(f"<div class='res-card {cls}'><div style='font-weight:800; color:#1A237E;'>{name} (风险指数: {score:.1f})</div><div style='font-size:14px; color:#455A64; margin-top:5px; line-height:1.6;'>{d['texts'][lv]}</div></div>", unsafe_allow_html=True)

    # 最终转化卡片 (完整温情文案)
    st.markdown(f"""
        <div class='home-box' style='border:2px solid #1A237E; margin-top:30px; padding:20px;'>
            <div style='font-size:16px; color:#455A64; line-height:1.8; margin-bottom:15px;'>
                这份报告提示了孩子的求救，也看见了您的委屈。<br>
                <b>其实，您不需要独自扛着。</b>
            </div>
            <div style='font-weight:bold; color:#1A237E; font-size:17px;'>添加微信您可以获得：</div>
            <div style='margin:10px 0; line-height:2.2; font-size:15px;'>
                1. 十个维度<span class='em-red'>个性化</span>改善方案<br>
                2. <span class='em-red'>30 分钟 1V1</span> 深度解析<br>
                3. 特惠 <span class='em-red'>198 元</span>（原价 598 元）
            </div>
            <div style='text-align:center; background:#F5F5F5; border-radius:12px; padding:15px; margin:15px 0;'>
                <div style='font-size:12px; color:#90A4AE;'>长按复制编号添加曹校长：</div>
                <div style='font-size:36px; font-weight:900; color:#E53935; letter-spacing:3px;'>{st.session_state.rid}</div>
            </div>
            <button style='width:100% !important; background:#1A237E; color:white; height:65px; border-radius:15px; font-size:20px; font-weight:bold; border:none;'>👉 预约 1V1 深度解析方案</button>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
