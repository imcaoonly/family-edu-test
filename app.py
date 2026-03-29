import streamlit as st
import random
import requests
import json
import plotly.graph_objects as go

# --- 1. 强效视觉屏蔽：彻底杀掉右下角头像、标签和所有官方 UI ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    /* 屏蔽右下角红色标签、头像及所有浮动小图标 */
    [data-testid="stStatusWidget"] {display:none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .viewerBadge_link__1S137 {display: none !important;}
    div[class^="viewerBadge"] {display: none !important;}
    button[title="Manage app"] {display: none !important;}
    #root > div:nth-child(1) > div > div > div > div > section > div > div > div > div.viewerBadge_container__1QSob {display:none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 基础配置 ---
FEISHU_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/e0c47a6f-4e26-405c-87ff-7fc955c8c279"
WECOM_LINK = "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" # 你的统一获客链接

# 维度题目范围 
DIM_MAP = {
    "家庭系统": list(range(0, 8)),      # 1-8题
    "家长状态": list(range(8, 18)),     # 9-18题
    "亲子关系": list(range(18, 28)),    # 19-28题
    "动力状态": list(range(28, 37)),    # 29-37题
    "学业管理": list(range(37, 47)),    # 38-47题
    "社会适应": list(range(47, 57))     # 48-57题
}

# 1-79题完整题目列表 
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

# --- 3. 初始化状态 ---
if 'step' not in st.session_state:
    st.session_state.step = "start"
    st.session_state.current_q = 0
    st.session_state.ans = {}
    st.session_state.rid = str(random.randint(100000, 999999))

def next_q(val):
    st.session_state.ans[st.session_state.current_q] = val
    st.session_state.current_q += 1
    st.rerun()

# --- 4. 流程控制 ---
if st.session_state.step == "start":
    st.title("🌿 家庭教育十维深度探查表")
    st.caption("(脑科学专业版)")
    age = st.slider("孩子周岁年龄", 1, 25, 7)
    if st.button("开始深度测评", use_container_width=True):
        st.session_state.age = age
        st.session_state.step = "testing"
        st.rerun()

elif st.session_state.step == "testing":
    cur = st.session_state.current_q
    total_計分 = len(QUESTIONS) # 79道
    
    if cur < total_計分:
        st.progress((cur + 1) / 85)
        st.subheader(f"第 {cur + 1} 题 / 共 85 题")
        st.markdown(f"### {QUESTIONS[cur]}")
        # 选项：0-3分 
        col1, col2 = st.columns(2)
        with col1:
            if st.button("0 (从不)", use_container_width=True): next_q(0)
            if st.button("2 (经常)", use_container_width=True): next_q(2)
        with col2:
            if st.button("1 (偶尔)", use_container_width=True): next_q(1)
            if st.button("3 (总是)", use_container_width=True): next_q(3)
        if cur > 0:
            if st.button("⬅️ 返回上一题"):
                st.session_state.current_q -= 1
                st.rerun()
    elif cur < 85:
        # 处理 80-85 背景题 
        st.subheader(f"第 {cur + 1} 题 / 共 85 题")
        bg_qs = [
            ("是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"]),
            ("尝试过哪些方式？", ["心理咨询", "药物治疗", "严管", "父母课", "其他"]),
            ("失效的原因是？", ["不落地", "不系统", "没坚持", "孩子不配合", "没陪跑"]),
            ("最迫切的痛点？", ["关系", "厌学", "专注力", "情绪", "手机"]),
            ("是否有勇气参与改变？", ["有", "需指导", "纠结", "只想改孩子"]),
            ("是否预约分析解读？", ["是", "否"])
        ]
        q_idx = cur - 79
        q_text, opts = bg_qs[q_idx]
        st.markdown(f"### {q_text}")
        selected = st.multiselect("请选择(可多选):", opts) if q_idx < 4 else st.radio("请选择:", opts)
        
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("⬅️ 上一题"):
                st.session_state.current_q -= 1
                st.rerun()
        with col_nav2:
            if st.button("下一题" if cur < 84 else "✅ 完成并生成报告", use_container_width=True):
                st.session_state.ans[cur] = selected
                if cur < 84:
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    # 推送飞书并跳转报告
                    msg = f"报告生成提醒\n编号:{st.session_state.rid}\n年龄:{st.session_state.age}\n状态:完成"
                    requests.post(FEISHU_URL, json={"msg_type":"text", "content":{"text":msg}})
                    st.session_state.step = "report"
                    st.rerun()

elif st.session_state.step == "report":
    st.title("📊 深度探查报告")
    st.success(f"报告编号：{st.session_state.rid}")
    
    # 1. 计算维度平均分
    scores = {}
    for name, idxs in DIM_MAP.items():
        val = sum(st.session_state.ans.get(i, 0) for i in idxs) / len(idxs)
        scores[name] = round(val, 2)
    
    # 2. 视觉雷达图
    fig = go.Figure(data=go.Scatterpolar(r=list(scores.values()), theta=list(scores.keys()), fill='toself', line_color='#1B5E20'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. 垂直滚动话术分析
    st.markdown("---")
    for name, score in scores.items():
        st.markdown(f"#### 📍 {name}维度分析")
        if score >= 1.8:
            st.error(f"得分：{score} (高危负荷) - 核心系统已失衡，必须立刻干预。")
        elif score >= 0.8:
            st.warning(f"得分：{score} (代偿警戒) - 表面尚稳，但底层动力已严重消耗。")
        else:
            st.info(f"得分：{score} (良性状态) - 基础较好，适合作为修复的突破点。")
            
    # 4. 198元获客转化
    st.markdown("---")
    st.markdown(f"### 💡 下一步建议\n这份报告揭示了“心脑失调”的根源。添加沈老师微信，备注编号 **{st.session_state.rid}**，领取 **198元** 专家1V1面诊及个性化改善方案。")
    st.link_button("👉 点击添加老师，预约深度解析", WECOM_LINK, use_container_width=True)
