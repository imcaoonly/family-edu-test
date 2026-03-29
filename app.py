import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 样式与视觉深度定制 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    /* 标题上移与紧凑化 */
    .title-row1 { text-align: center; font-size: 32px; font-weight: 800; color: #1B5E20; margin-top: -20px; }
    .title-row2 { text-align: center; font-size: 26px; font-weight: 700; color: #1B5E20; margin-top: -10px; }
    .title-sub { text-align: center; font-size: 15px; color: #666; margin-bottom: 15px; }
    /* 题目位置与单行优化 */
    .question-box { font-size: 20px; font-weight: 600; margin-bottom: 20px; text-align: center; color: #333; line-height: 1.5; }
    .stButton>button { border-radius: 12px; height: 3.2em; font-size: 16px; margin-bottom: 8px; }
    .report-card { padding: 15px; border-radius: 10px; background-color: #F8FAF8; border-left: 5px solid #2E7D32; margin-bottom: 12px; }
    .highlight-id { font-size: 26px; font-weight: 900; color: #D32F2F; background-color: #FFF3F3; padding: 2px 8px; border-radius: 4px; }
    </style>
    <div class='title-row1'>家庭教育</div>
    <div class='title-row2'>十维深度探查</div>
    <div class='title-sub'>(脑科学专业版)</div>
    """, unsafe_allow_html=True)

# --- 2. 题库数据：严格对标《系统识别题库》 ---
# 1-78题 计分项 [cite: 91-168]
QS_SCORE = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。", "长辈深度参与管教，经常推翻您的决定。", "父母教育标准不一，经常“一宽一严”。", "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。", "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。", # 系统
    "面对孩子问题，感到深深的无力感。", "觉得若不是为了孩子，生活会更精彩自由。", "吼叫后陷入“后悔自责—过度补偿”循环。", "觉得孩子某些性格与您讨厌的特质一模一样。", "极度在意老师或他人对孩子的负面评价。", "孩子表现与个人价值感挂钩，不出色感失败。", "管教时心跳加快、胸闷、手抖或大脑空白。", "觉得带孩子是孤军奋战，配偶无实质支持。", "睡眠质量差，入睡困难或报复性熬夜。", "内心焦虑、烦躁，很难获得平静。", # 家长
    "除了聊学习吃睡，很难进行开心闲聊。", "在校受委屈或丢脸会选择隐瞒，不告知。", "对您进房间或动用其物品有明显反感。", "经常反锁屋门，抗拒询问或靠近。", "情绪爆发时，本能想靠讲道理或强行压制。", "犯错后第一反应是撒谎、推诿或冷战。", "会翻看手机或日记来了解其真实想法。", "不敢在您面前表达真实不满、愤怒或意见。", "抱怨在家里没自由，或想要早点离家。", "沟通有明显防御性，您一开口他就烦。", # 关系
    "面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，立刻情绪崩塌或放弃。", "过度在意评价，因别人一句话就郁郁孤欢。", "对学习以外的事物也兴致索然，没爱好。", "经常说没意思、没劲，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。", "生命力在萎缩，越来越像一个“空心人”。", "即使做感兴趣的事，也难以保持长久热情。", "近期对以前喜欢的活动表现出明显冷感。", # 动力
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。", "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。", "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。", "坐姿东歪西倒，写作业时头低得非常近。", "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。", # 学业
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。", "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。", "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。", "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。", "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。", # 社会化
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。", "表达过消极厌世或“我消失了更好”的念头。", "身上有不明划痕，或拔头发、啃指甲见血。", "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。", "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。", # 情绪
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。", "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。", "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。", # 注意
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。", "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。", "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。" # 生理
]

# 79-85题 背景信息 
QS_BG = [
    ("1. 是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
    ("2. 为了解决问题，您之前尝试过哪些方式？", ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"], "multi"),
    ("3. 之前尝试的方法没有彻底生效的原因是？", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"], "multi"),
    ("4. 目前最迫切想解决的前三个痛点是？", ["关系/叛逆", "厌学/手机", "专注力/成绩", "情绪风险", "其它"], "multi"),
    ("5. 如果诊断根源在于“家庭系统及认知”，您是否有勇气参与改变？", ["非常有信心", "想尝试但需指导", "比较纠结", "只想改孩子"], "single"),
    ("6. 填完本表，您是否愿预约一次专业“全面分析解读”？", ["是", "否"], "single"),
    ("7. 如果需要投入时间及精力来彻底扭转局面，您是否有兴趣了解我们的系统方案？", ["是", "否"], "single")
]

# --- 3. 核心控制逻辑 ---
if 'idx' not in st.session_state:
    st.session_state.update({'step':'home', 'idx':0, 'ans':{}, 'rid':str(random.randint(100000, 999999))})

if st.session_state.step == 'home':
    st.info("💡 **这是一场跨越心与脑的对话，请放空杂念，给孩子和自己一次被“看见”的机会。**")
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'testing'; st.rerun()

elif st.session_state.step == 'testing':
    cur = st.session_state.idx
    st.progress((cur + 1) / 85)
    
    if cur < 78: # 计分题阶段
        st.write(f"第 {cur+1} 题 / 共 85 题")
        st.markdown(f"<div class='question-box'>{QS_SCORE[cur]}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("0 (从不)", use_container_width=True): 
            st.session_state.ans[cur] = 0; st.session_state.idx += 1; st.rerun()
        if c2.button("1 (偶尔)", use_container_width=True): 
            st.session_state.ans[cur] = 1; st.session_state.idx += 1; st.rerun()
        if c1.button("2 (经常)", use_container_width=True): 
            st.session_state.ans[cur] = 2; st.session_state.idx += 1; st.rerun()
        if c2.button("3 (总是)", use_container_width=True): 
            st.session_state.ans[cur] = 3; st.session_state.idx += 1; st.rerun()
    elif cur < 85: # 背景题阶段
        q_txt, opts, mode = QS_BG[cur-78]
        st.markdown(f"### {q_txt}")
        u_val = st.multiselect("可多选:", opts) if mode == "multi" else st.radio("请选择:", opts, index=None)
        if st.button("生成最终报告" if cur==84 else "继续下一步", use_container_width=True, disabled=not u_val):
            st.session_state.ans[cur] = u_val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.idx += 1
            st.rerun()
    
    if cur > 0:
        if st.button("⬅️ 返回上一题"): st.session_state.idx -= 1; st.rerun()

elif st.session_state.step == 'report':
    st.header("📊 深度探查诊断报告")
    st.warning("⚠️ **温馨提示**：分数越高，代表负荷与风险越大。")

    # 维度及话术逻辑
    DIM_LOGIC = {
        "家庭系统": (range(0,8), {
            "low": "地基非常扎实，孩子早期依恋关系好。好起来的速度会比常人快得多。",
            "mid": "整体稳定但有“微损耗”。孩子走得很累，若不统一标准，迟早演变成结构性问题。",
            "high": "“气压”极度不稳定，孩子所有能量都用来维稳了，无力搞学习。"
        }),
        "家长状态": (range(8,18), {
            "low": "您的心理建设很好。现在的困局缺的是一把精准的“手术刀”。",
            "mid": "处于“育儿倦怠”边缘。坚持带有一种强迫性牺牲感，提醒您该停下来修整认知了。",
            "high": "您的油箱已经干了。焦灼感会直接传染给孩子，咱们得先帮您加满油。"
        }),
        "亲子关系": (range(18,28), {
            "low": "情感管道通畅。只要心还在一起，任何教育技术都能100%发挥作用。",
            "mid": "缺乏“深链接”。沟通停留在事务层面，孩子正慢慢关上心门，需警惕习惯性隔离。",
            "high": "处于“信号屏蔽”状态。您说的每一句“为你好”都是攻击。不先疏通情感，教育就是徒劳。"
        })
    }

    scores = {}
    for name, (idxs, txts) in DIM_LOGIC.items():
        avg = sum(st.session_state.ans.get(i,0) for i in idxs) / len(idxs)
        scores[name] = avg
        if avg >= 1.9: color, level, desc = "#D32F2F", "危险", txts["high"]
        elif avg >= 0.9: color, level, desc = "#F57C00", "预警", txts["mid"]
        else: color, level, desc = "#388E3C", "优秀", txts["low"]
        
        st.markdown(f"""<div class='report-card' style='border-left-color:{color}'>
            <b style='color:{color}'>{name}维度：{avg:.2f}分 ({level})</b><br>
            <small style='color:#555'>{desc}</small></div>""", unsafe_allow_html=True)

    # 商业转化板块
    st.markdown("---")
    st.success(f"📌 **专属报告编号：** <span class='highlight-id'>{st.session_state.rid}</span>", unsafe_allow_html=True)
    st.markdown(f"""
    ### 🎁 您的测评权益已生效
    添加微信备注编号 **{st.session_state.rid}** 即可获得：
    1. **十个维度完整PDF报告** (含红灯预警与生理归因)
    2. **30分钟资深专家 1V1 深度解析**
    3. **限时特惠权益：198元 (原价598元)**
    """)
    st.link_button("👉 点击添加老师，预约深度诊断", "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f", use_container_width=True)
    
    fig = go.Figure(data=go.Scatterpolar(r=list(scores.values()), theta=list(scores.keys()), fill='toself', line_color='#1B5E20'))
    st.plotly_chart(fig, use_container_width=True)
