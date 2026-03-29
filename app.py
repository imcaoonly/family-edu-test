import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 样式与双行标题 (严格遵循品牌视觉) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .title-row1 { text-align: center; font-size: 34px; font-weight: 800; color: #1B5E20; margin-bottom: 0px; }
    .title-row2 { text-align: center; font-size: 28px; font-weight: 700; color: #1B5E20; margin-top: -10px; }
    .title-sub { text-align: center; font-size: 16px; color: #666; margin-bottom: 30px; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-size: 16px; margin-bottom: 10px; }
    .report-box { padding: 20px; border-radius: 15px; background-color: #f9f9f9; border: 1px solid #ddd; margin-bottom: 20px; }
    </style>
    <div class='title-row1'>家庭教育</div>
    <div class='title-row2'>十维深度探查</div>
    <div class='title-sub'>(脑科学专业版)</div>
    """, unsafe_allow_html=True)

# --- 2. 题库配置 (严格对标《系统识别题库》) ---
# 1-78题 计分项 [cite: 267-344]
QS_SCORE = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。", "长辈深度参与管教，经常推翻您的决定。", "父母教育标准不一，经常“一宽一严”。", "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。", "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。", # 系统 1-8
    "面对孩子问题，感到深深的无力感。", "觉得若不是为了孩子，生活会更精彩自由。", "吼叫后陷入“后悔自责—过度补偿”循环。", "觉得孩子某些性格与您讨厌的特质一模一样。", "极度在意老师或他人对孩子的负面评价。", "孩子表现与个人价值感挂钩，不出色感失败。", "管教时心跳加快、胸闷、手抖或大脑空白。", "觉得带孩子是孤军奋战，配偶无实质支持。", "睡眠质量差，入睡困难或报复性熬夜。", "内心焦虑、烦躁，很难获得平静。", # 家长 9-18
    "除了聊学习吃睡，很难进行开心闲聊。", "在校受委屈或丢脸会选择隐瞒，不告知。", "对您进房间或动用其物品有明显反感。", "经常反锁屋门，抗拒询问或靠近。", "情绪爆发时，本能想靠讲道理或强行压制。", "犯错后第一反应是撒谎、推诿或冷战。", "会翻看手机或日记来了解其真实想法。", "不敢在您面前表达真实不满、愤怒或意见。", "抱怨在家里没自由，或想要早点离家。", "沟通有明显防御性，您一开口他就烦。", # 关系 19-28
    "面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，立刻情绪崩塌或放弃。", "过度在意评价，因别人一句话就郁郁孤欢。", "对学习以外的事物也兴致索然，没爱好。", "经常说没意思、没劲，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。", "生命力在萎缩，越来越像一个“空心人”。", "即使做感兴趣的事，也难以保持长久热情。", "近期对以前喜欢的活动表现出明显冷感。", # 动力 29-37
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。", "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。", "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。", "坐姿东吊西歪，写作业时头低得非常近。", "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。", # 学业 38-48
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。", "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。", "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。", "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。", "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。", # 社会化 49-58
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。", "表达过消极厌世或“我消失了更好”的念头。", "身上有不明划痕，或拔头发、啃指甲见血。", "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。", "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。", # 情绪 59-66
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。", "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。", "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。", # 注意 67-72
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。", "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。", "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。" # 生理 73-78
]

# 背景信息 (79-85题) [cite: 345-352]
QS_BG = [
    ("是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
    ("为了解决问题，您之前尝试过哪些方式？", ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"], "multi"),
    ("之前尝试的方法没有彻底生效的原因是？", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"], "multi"),
    ("目前最迫切想解决的前三个痛点是？", ["关系", "厌学", "专注力差", "情绪较大", "手机"], "multi"),
    ("如诊断根源在于“家庭系统及认知”，您是否有勇气参与改变？", ["有", "有，但需指导", "比较纠结", "只想改孩子"], "single"),
    ("填完后，是否愿预约一次专业“全面分析解读”？", ["是", "否"], "single"),
    ("如果需投入时间扭转局面，您是否有兴趣了解？", ["是", "否"], "single")
]

# --- 3. 核心逻辑控制 ---
if 'idx' not in st.session_state:
    st.session_state.update({'idx':0, 'ans':{}, 'step':'test', 'rid':str(random.randint(1000,9999))})

def move_next(val):
    st.session_state.ans[st.session_state.idx] = val
    st.session_state.idx += 1
    st.rerun()

if st.session_state.step == 'test':
    cur = st.session_state.idx
    st.progress((cur + 1) / 85)
    
    if cur < 78: # 计分题
        st.write(f"第 {cur+1} 题 / 共 85 题")
        st.markdown(f"### {QS_SCORE[cur]}")
        c1, c2 = st.columns(2)
        if c1.button("0 (从不)", use_container_width=True): move_next(0)
        if c2.button("1 (偶尔)", use_container_width=True): move_next(1)
        if c1.button("2 (经常)", use_container_width=True): move_next(2)
        if c2.button("3 (总是)", use_container_width=True): move_next(3)
    elif cur < 85: # 背景题
        q_txt, opts, mode = QS_BG[cur-78]
        st.markdown(f"### {q_txt}")
        u_val = st.multiselect("可多选:", opts) if mode == "multi" else st.radio("请选择:", opts, index=None)
        if st.button("生成最终报告" if cur==84 else "下一题", use_container_width=True, disabled=not u_val):
            st.session_state.ans[cur] = u_val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.idx += 1
            st.rerun()
    
    if cur > 0:
        if st.button("⬅️ 返回上一题"): st.session_state.idx -= 1; st.rerun()

elif st.session_state.step == 'report':
    st.balloons()
    st.header("📊 深度探查诊断报告")
    st.warning("⚠️ 重要提醒：分数越高，代表该维度的“负荷”或“风险”越大。")
    
    # --- 4. 维度计算与三段式解读 [cite: 191-239] ---
    DIM_DATA = {
        "家庭系统": (range(0,8), {
            "low": "您的家庭地基非常扎实，孩子早期依恋关系很好。意味着孩子好起来会比别人快得多。",
            "mid": "整体稳定但内部存在“微损耗”（如教育标准不一）。孩子走得很累，若不统一标准，迟早会演变成结构性问题。",
            "high": "家里的“气压”太不稳定了。孩子像在地震带上盖房子，所有能量都用来“维稳”了，无力搞学习。"
        }),
        "家长状态": (range(8,18), {
            "low": "您的心理建设做得很好。现在的困局不是您无能，而是手里缺一把精准的“手术刀”。",
            "mid": "您正处于“育儿倦怠”的边缘。坚持带有一种强迫性的自我牺牲感，提醒您该停下来修整认知模式了。",
            "high": "您的油箱已经干了。焦灼感会通过镜像神经元直接传染给孩子，咱们得先帮您把油加满。"
        }),
        "亲子关系": (range(18,28), {
            "low": "孩子还愿意跟您说真心话。只要情感管道通着，任何技术手段都能 100% 发挥作用。",
            "mid": "缺乏“深链接”。沟通维持在事务性交流，孩子正在慢慢关上心门，若不换频，他会习惯性隔离。",
            "high": "处于“信号屏蔽”状态。您说的每一句“为他好”都是攻击。不先疏通情感，所有教育都是徒劳。"
        }),
        "动力状态": (range(28,37), {
            "low": "孩子骨子里有胜负欲。目前的颓废只是暂时的死机，只要重装系统，他自己就能跑起来。",
            "mid": "处于“待机状态”。表现取决于环境压力而非内在渴望。推一下动一下，最容易在初高阶段熄火。",
            "high": "已进入“节能模式”，生命力萎缩。我们要通过底层激活，让他重新“活”过来。"
        }),
        "学业表现": (range(37,48), {
            "low": "大脑硬件配置高，成绩波动只是“小感冒”，很好修补。",
            "mid": "处于“高代偿”维持。用双倍意志力弥补脑效率不足，一旦难度超标，孩子会迅速厌学崩盘。",
            "high": "大脑CPU过载！写一个字能耗是常人三倍。必须用脑科学方法帮他降载。"
        }),
        "社会适应": (range(48,58), {
            "low": "社会化属性很好。这种对集体的归属感，是我们把他从手机世界拉回现实的最强抓手。",
            "mid": "电子世界吸引力正盖过现实。孩子处于社交舒适区萎缩期，若不干预，现实社交能力将持续退化。",
            "high": "他在现实世界找不到成就感，只能去虚拟世界吸氧。学校对他来说不是学习的地方，而是“刑场”。"
        })
    }

    scores = {}
    st.subheader("🔍 核心六维度分析")
    for name, (indices, texts) in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i,0) for i in indices) / len(indices)
        scores[name] = round(avg, 2)
        
        # 话术分档判定 
        if avg >= 1.9: color, level, txt = "red", "高分（危险）", texts["high"]
        elif avg >= 0.9: color, level, txt = "orange", "中分（预警）", texts["mid"]
        else: color, level, txt = "green", "低分（优秀）", texts["low"]
        
        with st.container():
            st.markdown(f"#### **{name}：{avg:.2f}分 ({level})**")
            st.markdown(f"<div class='report-box' style='border-left: 5px solid {color};'>{txt}</div>", unsafe_allow_html=True)

    # --- 5. 雷达图呈现 ---
    fig = go.Figure(data=go.Scatterpolar(r=list(scores.values()), theta=list(scores.keys()), fill='toself', line_color='#1B5E20'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- 6. 风险专项指标 [cite: 240-250] ---
    st.subheader("🚩 专项风险提示")
    
    # 情绪红灯 (59-66)
    emo_indices = range(58, 66)
    has_red_light = any(st.session_state.ans.get(i) == 3 for i in emo_indices)
    if has_red_light:
        st.error("🚨 **红灯警报**：当前孩子情绪安全水位极低，建议暂停学业施压，优先进行情感固着。")
    
    # 注意力状态 (67-72)
    att_avg = sum(st.session_state.ans.get(i,0) for i in range(66, 72)) / 6
    if att_avg > 1.5:
        st.info("💡 **神经发育提示**：数据高度疑似 ADHD 特质。孩子并非态度问题，而是由于脑功能整合缺陷，需要专业训练支持。")
        
    # 生理归因 (73-78)
    phy_avg = sum(st.session_state.ans.get(i,0) for i in range(72, 78)) / 6
    if phy_avg > 1.5:
        st.warning("🥬 **生理底层发现**：孩子目前表现出的易激惹或专注力差，很大程度上受生理代谢（如营养、过敏）影响，建议进行底层修复。")

    # --- 7. 商业闭环 (引导加微信)  ---
    st.markdown("---")
    st.markdown(f"""
    这份报告揭示了孩子的求救，也看见了您的委屈。其实，您不需要独自扛着。
    
    添加微信备注生成的数字 **{st.session_state.rid}** 即可获得：
    1. **十个维度个性化改善方案**
    2. **30分钟 1V1 深度解析**
    3. **特惠 198 元（原价 598 元）**
    """)
    WECOM_LINK = "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f"
    st.link_button("👉 点击添加老师，预约深度诊断", WECOM_LINK, use_container_width=True)
    st.caption(f"报告编号: {st.session_state.rid} (请保存截屏)")
