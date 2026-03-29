import streamlit as st
import random
import requests
import json
import plotly.graph_objects as go

# --- 1. 隐藏自带 UI 的样式设置 ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. 初始配置 ---
FEISHU_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/e0c47a6f-4e26-405c-87ff-7fc955c8c279"

# 题目数据库 (严格对应 1-79 题)
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

# --- 3. 核心逻辑处理 ---
if 'step' not in st.session_state:
    st.session_state.step = "start"
    st.session_state.current_q = 0
    st.session_state.ans = {}
    st.session_state.rid = str(random.randint(100000, 999999))

# 自动下一题的辅助函数
def next_question(val):
    st.session_state.ans[st.session_state.current_q] = val
    st.session_state.current_q += 1
    st.rerun()

# --- 4. 页面显示 ---
if st.session_state.step == "start":
    st.title("🌿 家庭教育十维深度探查表(脑科学版)")
    st.write("一场跨越心与脑的对话，请给孩子和自己一次被“看见”的机会。")
    age = st.slider("孩子周岁年龄", 1, 25, 7)
    if st.button("开始测评", use_container_width=True):
        st.session_state.age = age
        st.session_state.step = "testing"
        st.rerun()

elif st.session_state.step == "testing":
    total_qs = len(QUESTIONS)
    current_q = st.session_state.current_q

    if current_q < total_qs:
        st.progress(current_q / (total_qs + 1))
        st.subheader(f"第 {current_q + 1} 题 / 共 85 题")
        st.markdown(f"**{QUESTIONS[current_q]}**")
        
        # 选项：点击即自动跳转
        col1, col2 = st.columns(2)
        with col1:
            if st.button("0 (从不)", use_container_width=True): next_question(0)
            if st.button("1 (偶尔)", use_container_width=True): next_question(1)
        with col2:
            if st.button("2 (经常)", use_container_width=True): next_question(2)
            if st.button("3 (总是)", use_container_width=True): next_question(3)
        
        st.divider()
        # 底部导航
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if current_q > 0:
                if st.button("⬅️ 上一题", use_container_width=True):
                    st.session_state.current_q -= 1
                    st.rerun()
    else:
        # 80-85题背景信息部分
        st.subheader("最后几步：背景信息")
        q80 = st.multiselect("是否有过确诊史？", ["ADHD", "抑郁/焦虑", "其他", "暂无"])
        q83 = st.multiselect("目前最迫切想解决的痛点？", ["关系", "厌学", "专注力差", "情绪较大", "手机"])
        q84 = st.radio("是否有勇气参与改变？", ["有", "有，但需指导", "纠结", "只想改孩子"], horizontal=True)
        
        col_prev, col_submit = st.columns(2)
        with col_prev:
            if st.button("⬅️ 上一题", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()
        with col_submit:
            if st.button("✅ 生成报告", use_container_width=True):
                # 飞书推送
                msg = f"报告通知：编号{st.session_state.rid}\n年龄:{st.session_state.age}\n痛点:{q83}\n决心:{q84}"
                requests.post(FEISHU_URL, json={"msg_type":"text", "content":{"text":msg}})
                st.session_state.step = "report"
                st.rerun()

elif st.session_state.step == "report":
    st.title("📊 测评报告已生成")
    st.success(f"专属报告编号：{st.session_state.rid}")
    st.info("请长按截屏保存。添加沈老师微信获取198元深度解析方案。")
    if st.button("重新测评"):
        st.session_state.step = "start"
        st.session_state.current_q = 0
        st.session_state.ans = {}
        st.rerun()
