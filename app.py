import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. UI 深度定制：深蓝品牌色 & 首页遮罩 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

# 颜色定义：主色 #1A237E (深蓝), 强调色 #FF7043 (暖橙), 辅助色 #455A64 (深灰蓝)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    .stApp { background: #F4F7F9; text-align: left !important; color: #455A64; }

    /* 首页专用遮盖容器 (Mask) */
    .home-mask {
        padding: 40px 25px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(26, 35, 126, 0.08);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(12px);
        margin-top: 20px;
    }

    /* 三行标题规范：左对齐 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }

    /* 老友感引导语 */
    .intro-text {
        font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 35px;
        border-left: 5px solid #FF7043; padding-left: 20px;
    }

    /* 题目样式 */
    .q-text { font-size: 22px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0; }

    /* 按钮样式：深蓝底色 */
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #0D47A1; transform: translateY(-2px); }

    /* 核心报警 Banner */
    .warning-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; line-height: 1.6; text-align: left; }
    .bg-red { background: #C62828; box-shadow: 0 4px 12px rgba(198,40,40,0.3); }
    .bg-orange { background: #E65100; box-shadow: 0 4px 12px rgba(230,81,0,0.3); }
    .bg-blue { background: #0D47A1; box-shadow: 0 4px 12px rgba(13,71,161,0.3); }

    /* 转化区编号 */
    .report-id { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 15px 35px; border-radius: 15px; border: 3px dashed #C62828; display: inline-block; margin: 20px 0; }
    /* 雷达图解读卡片 */
    .dim-card { background: white; padding: 20px; border-radius: 15px; margin: 15px 0; border-left: 5px solid #1A237E; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .dim-title { font-size: 20px; font-weight: 700; color: #1A237E; margin-bottom: 10px;}
    .dim-interpretation { font-size: 16px; color: #546E7A; line-height: 1.7; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心题库录入 (基于提供的《系统识别题库.docx》) ---
QUESTIONS_78 = [
    "1. 3岁前，主要抚养人频繁更换或长期中断。",
    "2. 早期曾连续2周以上见不到核心抚养人。",
    "3. 长辈深度参与管教，经常推翻您的决定。",
    "4. 父母教育标准不一，经常“一宽一严”。",
    "5. 幼年受委屈时极度粘人，无法离开抚养人。",
    "6. 近两年经历搬家、转学或财务大变动。",
    "7. 处理人际关系(如婆媳、夫妻矛盾)心力交瘁。",
    "8. 家人虽同住但各忙各的，缺乏交心时刻。",
    "9. 面对孩子问题，感到深深的无力感。",
    "10. 觉得若不是为了孩子，生活会更精彩自由。",
    "11. 吼叫后陷入“后悔自责一过度补偿”循环。",
    "12. 觉得孩子某些性格与您讨厌的特质一模一样。",
    "13. 极度在意老师或他人对孩子的负面评价。",
    "14. 孩子表现与个人价值感挂钩。",
    "15. 管教时心跳加快、胸闷、手抖或大脑空白。",
    "16. 觉得带孩子是孤军奋战，配偶无实质支持。",
    "17. 睡眠质量差，入睡困难或报复性熬夜。",
    "18. 内心焦虑、烦躁，很难获得平静。",
    "19. 除了聊学习吃睡，很难进行开心闲聊。",
    "20. 在校受委屈或丢脸会选择隐瞒，不告知。",
    "21. 对您进房间或动用其物品有明显反感。",
    "22. 经常反锁屋门，抗拒询问或靠近。",
    "23. 情绪爆发时，本能想靠讲道理或强行压制。",
    "24. 犯错后第一反应是撒谎、推诿或冷战。",
    "25. 会翻看手机或日记来了解其真实想法。",
    "26. 不敢在您面前表达真实不满、愤怒或意见。",
    "27. 抱怨在家里没自由，或想要早点离家。",
    "28. 沟通有明显防御性，您一开口他就烦。",
    "29. 面对挑战，还没做就觉得肯定不行，想退缩。",
    "30. 游戏输了或遇难题，立刻情绪崩塌或放弃。",
    "31. 过度在意评价，因别人一句话就郁郁寡欢。",
    "32. 对学习以外的事物也兴致索然，没爱好。",
    "33. 经常说没意思、没劲，感到空虚。",
    "34. 要求极高且不容许失败，稍不如意就否定自己。",
    "35. 生命力在萎缩，越来越像一个“空心人”。",
    "36. 即使做感兴趣的事，也难以保持长久热情。",
    "37. 近期对以前喜欢的活动表现出明显冷感。",
    "38. 磨蹭拖延，通过各种准备动作逃避开始作业。",
    "39. 写作业时神游发呆或手脚小动作不停。",
    "40. 写字姿势扭曲、力道极重，容易疲劳。",
    "41. 经常“转头就忘”，频繁丢失课本或文具。",
    "42. 指令“左耳进右耳出”，吼几遍才有反应。",
    "43. 阅读或抄写频繁跳行、漏字。",
    "44. 面对复杂任务，完全不知道从哪下手。",
    "45. 启动效率极低，反应速度明显慢于同龄人。",
    "46. 坐姿东倒西歪，写作业时头低得非常近。",
    "47. 处理多步骤指令时，中途断掉就直接放弃。",
    "48. 无法控制地咬指甲、咬衣领或笔头。",
    "49. 电子屏幕占据除学习外的绝大部分时间。",
    "50. 收手机时出现剧烈情绪爆发或肢体对抗。",
    "51. 为了玩手机经常撒谎，或熬夜偷玩。",
    "52. 提到上学或考试，有头痛腹痛等生理反应。",
    "53. 拒绝社交，有明显的社交回避或社恐。",
    "54. 老师反馈纪律性差、孤僻或难以融入集体。",
    "55. 在学校没有可以倾诉、互助支持的朋友。",
    "56. 对校园规则极度不耐受，有明显逆反心。",
    "57. 公共场合表现出局促感或不合时宜行为。",
    "58. 电子产品是爆发家庭冲突的最主要诱因。",
    "59. 近期长时间不洗头不换衣，不在意个人卫生。",
    "60. 食欲极端波动(暴食或长期厌食)。",
    "61. 表达过消极厌世或“我消失了更好”的念头。",
    "62. 身上有不明划痕，或拔头发、掐自己等行为。",
    "63. 对未来不抱期待，拒绝讨论任何计划。",
    "64. 睡眠节律彻底混乱，黑白颠倒。",
    "65. 对最亲近的人也表现出极度冷漠和隔绝。",
    "66. 提到学校或老师，浑身发抖或剧烈抵触。",
    "67. 玩游戏专注，面对学习坐不住、易走神。",
    "68. 安静环境下，也无法停止身体扭动或晃动。",
    "69. 无法耐心等别人说完，经常抢话、插话。",
    "70. 在排队或等待场合，表现出超越年龄的焦躁。",
    "71. 短时记忆黑洞，刚交代的事转头就忘。",
    "72. 做作业或听讲时，极易被微小动静吸引。",
    "73. 依赖甜食面食，极度讨厌蔬菜。",
    "74. 伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "75. 长期过敏体质(鼻炎、腺样体、湿疹等)。",
    "76. 进食大量糖面后，莫名亢奋或情绪崩溃。",
    "77. 睡觉张口呼吸、盗汗、磨牙或频繁翻身。",
    "78. 睡眠充足但眼圈常年发青或水肿。"
]

BG_QS = [
    "79. 是否有过确诊?(多选): ADHD、抑郁/焦虑、其他、暂无",
    "80. 为了解决问题，您之前尝试过哪些方式?(多选): 心理咨询、药物治疗、增加严管、上父母课、其他",
    "81. 之前尝试的方法没有彻底生效的原因是?(多选): 不落地、不系统、没法坚持、孩子不配合、缺乏专业陪跑",
    "82. 目前最迫切想解决的前三个痛点是?(多选): 关系、厌学、专注力差、情绪较大、手机",
    "83. 如诊断根源在于“家庭系统及认知”，您是否有勇气参与改变?(单选): 有、有，但需指导、比较纠结、只想改孩子",
    "84. 填完后，是否愿预约一次专业“全面分析解读”?(单选): 是、否",
    "85. 如果需投入时间扭转局面，您是否有兴趣了解?(单选): 是、否"
]

# --- 3. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 4. 页面流程 ---

# A. 首页：遮罩感 + 三行标题 + 老友文案
if st.session_state.step == 'home':
    st.markdown("""
        <div class='home-mask'>
            <div class='title-l1'>曹校长 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是曹校长。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'; st.rerun()

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    total_q = 85
    st.progress((cur + 1) / total_q)
    
    if cur < 78:
        st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS_78[cur]}</div>", unsafe_allow_html=True)
        opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
        c1, c2 = st.columns(2)
        for i, (txt, val) in enumerate(opts):
            with (c1 if i % 2 == 0 else c2):
                if st.button(txt, key=f"btn_q_{cur}_{i}", use_container_width=True):
                    st.session_state.ans[cur] = val
                    st.session_state.cur += 1
                    st.rerun()
    else:
        # 处理背景题 (79-85)
        idx = cur - 78
        st.markdown(f"<div class='q-text'>{cur+1}. {BG_QS[idx]}</div>", unsafe_allow_html=True)
        if idx in [0, 1, 2, 3]:  # 多选背景题
            options = BG_QS[idx].split(": ")[1].split("、")
            selected = st.multiselect(f"请选择 ({BG_QS[idx].split(':')[0]})", options, key=f"bg_multi_{idx}")
            if st.button("下一题", key=f"next_bg_{idx}"):
                st.session_state.ans[cur] = ", ".join(selected) if selected else "未选"
                st.session_state.cur += 1
                st.rerun()
        elif idx in [4, 5, 6]:  # 单选背景题
            options = BG_QS[idx].split(": ")[1].split("、")
            selected = st.radio(f"请选择 ({BG_QS[idx].split(':')[0]})", options, key=f"bg_single_{idx}")
            if st.button("下一题", key=f"next_bg_single_{idx}"):
                st.session_state.ans[cur] =
