import streamlit as st
import random
import requests
import plotly.graph_objects as go

# --- 1. 视觉屏蔽与样式 ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDeployButton {display:none;} [data-testid="stStatusWidget"] {display:none;}
    div[class*="viewerBadge"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 基础配置 ---
FEISHU_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/e0c47a6f-4e26-405c-87ff-7fc955c8c279"
WECOM_LINK = "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f"

# 维度与题号精准映射 (使用 0 轴索引，题号-1)
DIM_CONFIG = {
    "1.家庭系统": {"ids": list(range(0, 8)), "type": "radar"},   # 1-8题
    "2.家长状态": {"ids": list(range(8, 18)), "type": "radar"},  # 9-18题
    "3.亲子关系": {"ids": list(range(18, 28)), "type": "radar"}, # 19-28题
    "4.动力状态": {"ids": list(range(28, 37)), "type": "radar"}, # 29-37题
    "5.学业管理": {"ids": list(range(37, 48)), "type": "radar"}, # 38-48题
    "6.社会化适应": {"ids": list(range(48, 58)), "type": "radar"}, # 49-58题
    "7.情绪状态": {"ids": list(range(58, 66)), "type": "risk"},   # 59-66题
    "8.注意力状态": {"ids": list(range(66, 72)), "type": "risk"}, # 67-72题
    "9.底层生理": {"ids": list(range(72, 79)), "type": "body"}    # 73-79题
}

# 题库全量导入 (1-79题)
QUESTIONS = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。", "长辈深度参与管教，经常推翻您的决定。",
    "父母教育标准不一，经常“一宽一严”。", "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。",
    "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。", "面对孩子问题，感到深深的无力感。",
    "觉得若不是为了孩子，生活会更精彩自由。", "吼叫后陷入“后悔自责—过度补偿”循环。", "觉得孩子某些性格与您讨厌的特质一模一样。",
    "极度在意老师或他人对孩子的负面评价。", "孩子表现与个人价值感挂钩，不出色感失败。", "管教时心跳加快、胸闷、手抖或大脑空白。",
    "觉得带孩子是孤军奋战，配偶无实质支持。", "睡眠质量差，入睡困难或报复性熬夜。", "内心焦虑、烦躁，很难获得平静。",
    "除了聊学习吃睡，很难进行开心闲聊。", "在校受委屈或丢脸会选择隐瞒，不告知。", "对您进房间或动用其物品有明显反感。",
    "经常反锁屋门，抗拒询问或靠近。", "情绪爆发时，本能想靠讲道理或强行压制。", "犯错后第一反应是撒谎、推诿或冷战。",
    "会翻看手机或日记来了解其真实想法。", "不敢在您面前表达真实不满、愤怒或意见。", "抱怨在家里没自由，或想要早点离家。", "沟通有明显防御性，您一开口他就烦。",
    "面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，立刻情绪崩塌或放弃。", "过度在意评价，因别人一句话就郁郁寡欢。",
    "对学习以外的事物也兴致索然，没爱好。", "经常说没意思、没劲，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。",
    "生命力在萎缩，越来越像一个“空心人”。", "即使做感兴趣的事，也难以保持长久热情。", "近期对以前喜欢的活动表现出明显冷感。",
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。",
    "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。",
    "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。", "坐姿东倒西歪，写作业时头低得非常近。",
    "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。", "电子屏幕占据除学习外的绝大部分时间。",
    "收手机时出现剧烈情绪爆发或肢体对抗。", "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。",
    "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。", "在学校没有可以倾诉、互助支持的朋友。",
    "对校园规则极度不耐受，有明显逆反心。", "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。",
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。", "表达过消极厌世或“我消失了更好”的念头。",
    "身上有不明划痕，或拔头发、啃指甲见血。", "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。",
    "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。", "玩游戏专注，面对学习坐不住、易走神。",
    "安静环境下，也无法停止身体扭动或晃动。", "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。",
    "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。", "依赖甜食面食，极度讨厌蔬菜。",
    "伴有长期口臭、肚子胀气、便秘或大便不成形。", "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。",
    "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。"
]

# --- 3. 报告话术库 (按指南全量录入) ---
REPORT_TEXTS = {
    "1.家庭系统": {
        "low": "您的家庭地基非常扎实，孩子早期依恋关系很好。这意味着孩子内心的安全感底色是亮的，只要解决表层的功能问题，他好起来会比别人快得多。",
        "mid": "您的家庭基础整体是稳定的，但内部存在一些‘微损耗’（如教育标准不一）。孩子现在像是在顺风和逆风交替的环境下航行，虽然没翻船，但走得很累。如果不统一标准，这些微损耗迟早会演变成大的结构性问题。",
        "high": "家里的‘气压’太不稳定了。孩子现在就像在地震带上盖房子，他把所有的能量都用来‘维稳’了，根本没有余力去搞学习。"
    },
    "2.家长状态": {
        "low": "您的心理建设做得很好。您是孩子最稳的后盾。现在的困局不是您无能，而是您手里缺一把精准的‘手术刀’。",
        "mid": "您正处于‘育儿倦怠’的边缘。您依然在坚持，但这种坚持带有一种强迫性的自我牺牲感。现在的您就像亮起黄灯的仪表盘，提醒您该停下来修整认知模式了，否则下一步就是彻底的无力感。",
        "high": "您现在的油箱已经干了。您在用透支自己的方式陪跑，这种焦灼感会通过镜像神经元直接传染给孩子，咱们得先帮您把油加满。"
    },
    "3.亲子关系": {
        "low": "最宝贵的是，孩子还愿意跟您说真心话。只要情感管道通着，任何技术手段都能 100% 发挥作用。",
        "mid": "你们之间没有大冲突，但缺乏‘深链接’。孩子正在慢慢关上心门，如果您不主动更换沟通频率，他会习惯性地在心理上与您隔离。",
        "high": "你们之间现在是‘信号屏蔽’状态。您说的每一句‘为他好’，在他听来都是攻击。不先疏通情感，所有的教育都是无效功。"
    },
    "4.动力状态": {
        "low": "孩子骨子里是有胜负欲和生命力的。他现在的颓废只是‘暂时的死机’，只要重装系统，他自己就能跑起来。",
        "mid": "孩子的生命力处于‘待机状态’。他想好但缺乏持续推力。这种状态最容易在初高中阶段因为压力剧增而彻底熄火。",
        "high": "孩子已经进入了‘节能模式’，对外界失去了探索欲。这是典型的生命力萎缩，我们要通过底层激活，让他重新‘活’过来。"
    },
    "5.学业管理": {
        "low": "孩子的大脑硬件配置其实很高，执行功能没问题。现在的成绩波动，纯粹是情绪或态度的小感冒，很好修补。",
        "mid": "孩子目前的学业表现是一种‘高代偿’维持。他在用双倍的意志力弥补脑启动效率不足。一旦难度超过极限，会迅速崩盘。",
        "high": "这不是态度问题，是‘大脑CPU过载’。他写一个字消耗的能量是别人的三倍。必须用脑科学的方法帮他降载。"
    },
    "6.社会化适应": {
        "low": "孩子的社会化属性很好，他渴望链接。这种对集体的归属感，是我们后期把他从手机世界拉回现实的最强抓手。",
        "mid": "电子世界对他吸引力正在盖过现实。如果现在不干预，他会越来越倾向于在虚拟世界寻找安全感，现实社交能力将持续退化。",
        "high": "他在现实世界里找不到成就感，只能去虚拟世界吸氧。学校对他来说不是学习的地方，而是‘刑场’。"
    }
}

# --- 4. 状态管理 ---
if 'idx' not in st.session_state:
    st.session_state.update({'step': "start", 'idx': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

def next_q(val):
    st.session_state.ans[st.session_state.idx] = val
    st.session_state.idx += 1
    st.rerun()

# --- 5. 测评流程 ---
if st.session_state.step == "start":
    st.markdown("<h1 style='text-align: center;'>家庭教育十维深度探查</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>（脑科学专业版）</p>", unsafe_allow_html=True)
    age = st.slider("孩子周岁年龄", 1, 25, 7)
    if st.button("开始深度测评", use_container_width=True):
        st.session_state.step = "testing"
        st.rerun()

elif st.session_state.step == "testing":
    curr = st.session_state.idx
    # A. 1-79题计分项
    if curr < 79:
        st.progress((curr + 1) / 85)
        st.subheader(f"第 {curr + 1} 题 / 共 85 题")
        st.markdown(f"### {QUESTIONS[curr]}")
        cols = st.columns(2)
        if cols[0].button("0 (从不)", use_container_width=True): next_q(0)
        if cols[1].button("1 (偶尔)", use_container_width=True): next_q(1)
        if cols[0].button("2 (经常)", use_container_width=True): next_q(2)
        if cols[1].button("3 (总是)", use_container_width=True): next_q(3)
        if curr > 0 and st.button("⬅️ 返回上一题"):
            st.session_state.idx -= 1
            st.rerun()
    # B. 80-85题背景信息 (拦截逻辑)
    elif curr < 85:
        bg_qs = [
            ("是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
            ("尝试过哪些方式？", ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"], "multi"),
            ("方法未生效的原因？", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"], "multi"),
            ("最迫切的前三个痛点？", ["关系", "厌学", "专注力差", "情绪较大", "手机"], "multi"),
            ("是否有勇气参与改变？", ["有", "有，但需指导", "比较纠结", "只想改孩子"], "single"),
            ("是否愿预约分析解读？", ["是", "否"], "single")
        ]
        q_txt, opts, q_tp = bg_qs[curr - 79]
        st.subheader(f"背景信息 ({curr+1}/85)")
        st.markdown(f"### {q_txt}")
        u_in = st.multiselect("请选择 (必填):", opts) if q_tp == "multi" else st.radio("请选择 (必填):", opts, index=None)
        
        btn_label = "生成报告" if curr == 84 else "下一步"
        if st.button(btn_label, use_container_width=True, disabled=not u_in):
            st.session_state.ans[curr] = u_in
            if curr < 84:
                st.session_state.idx += 1
                st.rerun()
            else:
                st.session_state.step = "report"
                requests.post(FEISHU_URL, json={"msg_type":"text","content":{"text":f"报告已生成:{st.session_state.rid}"}})
                st.rerun()

elif st.session_state.step == "report":
    st.markdown("<h2 style='text-align: center;'>📊 深度探查报告</h2>", unsafe_allow_html=True)
    st.success(f"报告编号：{st.session_state.rid}")
    
    # 1. 计算均分
    scores = {}
    for dim, cfg in DIM_CONFIG.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in cfg["ids"]) / len(cfg["ids"])
        scores[dim] = round(avg, 2)

    # 2. 雷达图 (1-6维度)
    radar_labels = list(scores.keys())[:6]
    radar_values = list(scores.values())[:6]
    fig = go.Figure(data=go.Scatterpolar(r=radar_values, theta=radar_labels, fill='toself', line_color='#1B5E20'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # 3. 核心维度深度解析 (1-6)
    st.divider()
    st.markdown("### 🔍 核心维度深度归因")
    for dim in radar_labels:
        s = scores[dim]
        level = "high" if s >= 1.9 else "mid" if s >= 0.9 else "low"
        color = "#D32F2F" if level=="high" else "#FBC02D" if level=="mid" else "#388E3C"
        st.markdown(f"#### <span style='color:{color}'>● {dim}：{s}分</span>", unsafe_allow_html=True)
        st.write(REPORT_TEXTS[dim][level])

    # 4. 专项风险警报 (7-9)
    st.divider()
    st.markdown("### 🧠 风险专项与底层生理")
    # 7. 情绪警报
    e_score = scores["7.情绪状态"]
    has_suicide = any(st.session_state.ans.get(i) == 3 for i in range(58, 66)) # 59-66题是否有3分
    if e_score >= 1.5 or has_suicide:
        st.error(f"❗ 情绪风险 ({e_score}分)：这是【红灯警告】。孩子现在的沉默是他在呼救。建议暂停学业施压，优先进行情感固着。")
    
    # 8. 注意力预警
    a_score = scores["8.注意力状态"]
    if a_score >= 1.5:
        st.warning(f"⚠️ 注意力预警 ({a_score}分)：数据高度疑似 ADHD 特质。孩子大脑天生自带“降噪功能缺陷”，需要专业的脑功能整合训练，而非一味责骂。")

    # 9. 生理归因
    b_score = scores["9.底层生理"]
    if b_score >= 1.5:
        st.info(f"🧬 生理基础 ({b_score}分)：孩子的部分行为受生理代谢（如营养、过敏）影响。生理基础不稳，心智无法成长，建议配合律动方案进行底层修复。")

    # 5. 结尾与引导
    st.divider()
    st.warning("⚠️ 提示：请【长按截屏】保存此报告结果，作为后续面诊依据。")
    st.markdown(f"""
    ### 🌿 结语
    这份报告揭示了孩子的求救，也看见了您的委屈。
    其实，您不需要独自扛着。
    
    **添加老师微信您可以获得：**
    1. **十个维度**个性化改善方案
    2. **30分钟** 1V1深度解析
    3. **特惠198元**（原价598元）
    
    **添加时请备注生成的数字：** 👉 **{st.session_state.rid}**
    """)
    st.link_button("👉 点击添加老师，预约深度诊断", WECOM_LINK, use_container_width=True)
