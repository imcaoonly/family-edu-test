import streamlit as st
import plotly.graph_objects as go
import random

# --- 1. 终极视觉锁定 (CSS Overwrite) ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 首页单屏锁定 */
    .home-lock {
        height: 100vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
    }

    /* 三行标题严格对齐 */
    .l1 { color: #90A4AE; font-size: 16px; margin-bottom: 5px; }
    .l2 { color: #1A237E; font-size: 38px; font-weight: 900; margin-bottom: 5px; line-height: 1.2; }
    .l3 { color: #FF7043; font-size: 28px; font-weight: bold; margin-bottom: 30px; }
    
    /* 毛玻璃引导语 */
    .glass-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        color: #37474F;
        line-height: 1.8;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* 答题页左对齐与按钮样式 */
    .stButton > button {
        width: 100%;
        text-align: left !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
        margin-bottom: 10px;
    }
    
    /* 验证码红框 */
    .rid-box {
        border: 2px dashed #FF5252;
        padding: 15px;
        text-align: center;
        margin: 20px 0;
        border-radius: 8px;
        background-color: #FFF5F5;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 完整题库加载 (1-85题) ---
QUESTIONS = [
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
    "近期对以前喜欢的活动表现出明显冷感。",
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。",
    "写字姿势扭曲、力道极重，容易疲劳。", "经常“转头就忘”，频繁丢失课本或文具。",
    "指令“左耳进右耳出”，
