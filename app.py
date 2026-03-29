import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 样式与视觉定制 (极致排版) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .title-row1 { text-align: center; font-size: 34px; font-weight: 800; color: #1B5E20; margin-bottom: 0px; }
    .title-row2 { text-align: center; font-size: 28px; font-weight: 700; color: #1B5E20; margin-top: -10px; }
    .title-sub { text-align: center; font-size: 16px; color: #666; margin-bottom: 30px; }
    /* 题目单行显示 */
    .question-box { font-size: 20px; font-weight: 600; margin-bottom: 25px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: center; color: #333; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-size: 16px; }
    .report-card { padding: 18px; border-radius: 12px; background-color: #F0F4F0; border-left: 5px solid #2E7D32; margin-bottom: 15px; }
    .highlight-id { font-size: 24px; font-weight: 900; color: #D32F2F; text-decoration: underline; }
    </style>
    <div class='title-row1'>家庭教育</div>
    <div class='title-row2'>十维深度探查</div>
    <div class='title-sub'>(脑科学专业版)</div>
    """, unsafe_allow_html=True)

# --- 2. 题库数据 (1-78计分 + 7道背景) ---
QS_SCORE = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。", "长辈深度参与管教，经常推翻您的决定。", "父母教育标准不一，经常“一宽一严”。", "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。", "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。", # 系统 1-8
    "面对孩子问题，感到深深的无力感。", "觉得若不是为了孩子，生活会更精彩自由。", "吼叫后陷入“后悔自责—过度补偿”循环。", "觉得孩子某些性格与您讨厌的特质一模一样。", "极度在意老师或他人对孩子的负面评价。", "孩子表现与个人价值感挂钩，不出色感失败。", "管教时心跳加快、胸闷、手抖或大脑空白。", "觉得带孩子是孤军奋战，配偶无实质支持。", "睡眠质量差，入睡困难或报复性熬夜。", "内心焦虑、烦躁，很难获得平静。", # 家长 9-18
    "除了聊学习吃睡，很难进行开心闲聊。", "在校受委屈或丢脸会选择隐瞒，不告知。", "对您进房间或动用其物品有明显反感。", "经常反锁屋门，抗拒询问或靠近。", "情绪爆发时，本能想靠讲道理或强行压制。", "犯错后第一反应是撒谎、推诿或冷战。", "会翻看手机或日记来了解其真实想法。", "不敢在您面前表达真实不满、愤怒或意见。", "抱怨在家里没自由，或想要早点离家。", "沟通有明显防御性，您一开口他就烦。", # 关系 19-28
    "面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，立刻情绪崩塌或放弃。", "过度在意评价，因别人一句话就郁郁孤欢。", "对学习以外的事物也兴致索然，没爱好。", "经常说没意思、没劲，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。", "生命力在萎缩，越来越像一个“空心人”。", "即使做感兴趣的事，也难以保持长久热情。", "近期对以前喜欢的活动表现出明显冷感。", # 动力 29-37
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。", "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。", "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。", "坐姿东歪西倒，写作业时头低得非常近。", "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。", # 学业 38-48
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。", "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。", "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。", "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。", "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。", # 社会化 49-58
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。", "表达过消极厌世或“我消失了更好”的念头。", "身上有不明划痕，或拔头发、啃指甲见血。", "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。", "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。", # 情绪 59-66
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。", "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。", "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。", # 注意 67-72
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。", "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。", "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。" # 生理 73-78
]

QS_BG = [
    ("是否有过确诊？", ["ADHD", "抑郁/焦虑", "对立违抗", "暂无"], "multi"),
    ("之前尝试过哪些方式？", ["心理咨询", "药物治疗", "感统训练", "父母课程", "其他"], "multi"),
    ("方法未生效的原因？", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏陪跑"], "multi"),
    ("目前最迫切想解决的痛点？", ["关系", "厌学", "专注力", "情绪", "手机"], "multi"),
    ("是否有勇气参与家庭系统改变？", ["有", "有，但需指导", "纠结", "只想改孩子"], "single"),
    ("是否愿预约资深专家解读？", ["是", "否"], "single"),
    ("是否有兴趣了解扭转方案？", ["是", "否"], "single")
]

# --- 3. 状态管理 ---
if 'idx' not in st.session_state:
    st.session_state.update({'step':'home', 'idx':0, 'ans':{}, 'rid':str(random.randint(100000, 999999))})

# --- 4. 逻辑流控制 ---
if st.session_state.step == 'home':
    st.info("💡 **这是一场跨越心与脑的对话，请放空杂念，给孩子和自己一次被“看见”的机会。**")
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'testing'; st.rerun()

elif st.session_state.step == 'testing':
    cur = st.session_state.idx
    st.progress((cur + 1) / 85)
    
    if cur < 78:
        st.write(f"第 {cur+1} 题 / 共 85 题")
        st.markdown(f"<div class='question-box'>{QS_SCORE[cur]}</div>", unsafe_allow_html=True)
        cols = st.columns(2)
        if cols[0].button("0 (从不)", use_container_width=True): 
            st.session_state.ans[cur] = 0; st.session_state.idx += 1; st.rerun()
        if cols[1].button("1 (偶尔)", use_container_width=True): 
            st.session_state.ans[cur] = 1; st.session_state.idx += 1; st.rerun()
        if cols[0].button("2 (经常)", use_container_width=True): 
            st.session_state.ans[cur] = 2; st.session_state.idx += 1; st.rerun()
        if cols[1].button("3 (总是)", use_container_width=True): 
            st.session_state.ans[cur] = 3; st.session_state.idx += 1; st.rerun()
    elif cur < 85:
        q_txt, opts, mode = QS_BG[cur-78]
        st.markdown(f"### {q_txt}")
        u_val = st.multiselect("请多选:", opts) if mode == "multi" else st.radio("请选择:", opts, index=None)
        if st.button("生成最终报告" if cur==84 else "继续下一步", use_container_width=True, disabled=not u_val):
            st.session_state.ans[cur] = u_val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.idx += 1
            st.rerun()
    
    if cur > 0:
        if st.button("⬅️ 返回上一题"): st.session_state.idx -= 1; st.rerun()

elif st.session_state.step == 'report':
    st.balloons()
    st.header("📋 深度探查诊断报告")
    st.warning("⚠️ **分数越高，代表负荷与风险越大**。0-0.8分为优秀，0.9-1.8分为预警，1.9-3.0分为危险。")

    # 维度话术库
    DIM_TEXTS = {
        "家庭系统": (range(0,8), "地基稳固度", {
            "low": "地基非常扎实，孩子早期依恋关系好，未来逆袭的速度会比常人快得多。",
            "mid": "整体稳定但内部有“微损耗”。孩子走得很累，若不统一标准，迟早演变成结构性问题。",
            "high": "“气压”太不稳定，孩子所有能量都用来维稳了，无力搞学习。"
        }),
        "关系通道": (range(18,28), "沟通质量", {
            "low": "情感管道通畅，孩子还愿意说真心话，任何教育技术都能100%发挥作用。",
            "mid": "缺乏“深链接”，沟通停留在事务层面。孩子正慢慢关上心门，若不换频，他会习惯隔离。",
            "high": "信号屏蔽状态，您说的每一句“为你好”都是攻击。不疏通情感，所有教育都是无效功。"
        }),
        "动力生命力": (range(28,37), "自驱核心", {
            "low": "骨子里有胜负欲，颓废只是暂时死机。只要重装系统，他自己就能跑起来。",
            "mid": "处于待机状态，推一下动一下。最容易在初高阶段因为压力剧增而彻底熄火。",
            "high": "进入节能模式，生命力萎缩。必须通过底层激活，让他重新活过来。"
        })
    }

    # 计算与展示
    scores = {}
    for name, (indices, title, txts) in DIM_TEXTS.items():
        avg = sum(st.session_state.ans.get(i,0) for i in indices) / len(indices)
        scores[name] = avg
        if avg >= 1.9: level, color, desc = "危险", "#D32F2F", txts["high"]
        elif avg >= 0.9: level, color, desc = "预警", "#F57C00", txts["mid"]
        else: level, color, desc = "优秀", "#388E3C", txts["low"]
        
        st.markdown(f"""<div class='report-card' style='border-left-color:{color}'>
            <b style='color:{color}'>{name}：{avg:.2f}分 ({level})</b><br>
            <small style='color:#555'>{desc}</small></div>""", unsafe_allow_html=True)

    # 关键信息显眼化板块
    st.markdown("---")
    st.error(f"⚠️ **重要提醒**：系统已基于您的回答锁定核心归因点。")
    st.success(f"📌 **专属报告编号：** <span class='highlight-id'>{st.session_state.rid}</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    ### 🎁 您的测评权益已生效
    添加专家微信，备注编号 **{st.session_state.rid}** 即可领取：
    1. **10维度完整PDF诊断报告** (含生理归因分析)
    2. **30分钟资深专家 1V1 深度解读**
    3. **特惠权益：198元 (原价598元)**
    """)
    
    st.link_button("👉 点击添加老师，领取深度改善方案", "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f", use_container_width=True)
    st.caption("请截屏保存此页面，以免编号丢失。")

    # 雷达图仅作为视觉辅助
    fig = go.Figure(data=go.Scatterpolar(r=list(scores.values()), theta=list(scores.keys()), fill='toself', line_color='#1B5E20'))
    st.plotly_chart(fig, use_container_width=True)
