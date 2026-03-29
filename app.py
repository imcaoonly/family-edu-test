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
                # C. 结果页
elif st.session_state.step == 'report':
    # 顶部截屏提醒
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。</div>", unsafe_allow_html=True)
    
    # --- 1. 计分与维度均分计算 ---
    # 根据《指南》定义计算六个核心维度和三个专项维度的均分
    ans = st.session_state.ans
    dim_ranges = {
        '系统': (0, 8),    # 1-8题
        '家长': (8, 18),   # 9-18题
        '关系': (18, 28),  # 19-28题
        '动力': (28, 37),  # 29-37题
        '学业': (37, 48),  # 38-48题
        '社会化': (48, 58), # 49-58题
    }
    # 计算核心维度均分
    dim_scores = {}
    for name, (start, end) in dim_ranges.items():
        total = sum([ans.get(i, 0) for i in range(start, end)])
        dim_scores[name] = total / (end - start)  # 均分
    
    # 计算专项维度均分
    emotion_avg = sum([ans.get(i, 0) for i in range(58, 66)]) / 8
    adhd_avg = sum([ans.get(i, 0) for i in range(66, 72)]) / 6
    bio_avg = sum([ans.get(i, 0) for i in range(72, 78)]) / 6
    
    # --- 2. 绘制六维雷达图 ---
    categories = list(dim_scores.keys())
    values = list(dim_scores.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # 首尾相接形成闭合图形
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(26, 35, 126, 0.3)',  # 主色深蓝，半透明填充
        line=dict(color='#1A237E', width=3),  # 主色深蓝边框
        name='家庭生态六维探查',
        hovertemplate='%{theta}: %{r:.2f}分<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
                ticktext=['0', '0.5', '1.0', '1.5', '2.0', '2.5', '3.0'],
                tickfont=dict(size=10),
                color='#546E7A'
            ),
            angularaxis=dict(color='#455A64', gridcolor='#BDBDBD')
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',  # 透明背景
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- 3. 六维度个性化解读 ---
    st.subheader("✍️ 核心维度深度解读")
    st.write("---")
    
    # 依据《指南》中定义的三段式话术，为每个维度生成解读
    interpretations = {
        '系统': {
            0.8: "您的家庭地基非常扎实，孩子早期依恋关系很好。这意味着孩子内心的安全感底色是亮的，只要解决表层的功能问题，他好起来会比别人快得多。",
            1.8: "您的家庭基础整体是稳定的，但内部存在一些‘微损耗’(如教育标准不一)。孩子现在像是在顺风和逆风交替的环境下航行，虽然没翻船，但走得很累。如果不统一标准，这些微损耗迟早会演变成大的结构性问题。",
            3.0: "家里的‘气压’太不稳定了。孩子现在就像在地震带上盖房子，他把所有的能量都用来‘维稳’了，根本没有余力去搞学习。"
        },
        '家长': {
            0.8: "您的心理建设做得很好。您是孩子最稳的后盾。现在的困局不是您无能，而是您手里缺一把精准的‘手术刀’。",
            1.8: "您正处于‘育儿倦怠’的边缘。您依然在坚持，但这种坚持带有一种强迫性的自我牺牲感。现在的您就像亮起黄灯的仪表盘，提醒您该停下来修整认知模式了，否则下一步就是彻底的无力感。",
            3.0: "您现在的油箱已经干了。您在用透支自己的方式陪跑，这种焦灼感会通过镜像神经元直接传染给孩子，咱们得先帮您把油加满。"
        },
        '关系': {
            0.8: "最宝贵的是,孩子还愿意跟您说真心话。只要情感管道通着,任何技术手段(如律动、脑训练)都能 100%发挥作用。",
            1.8: "你们之间没有大冲突,但缺乏‘深链接’。目前的沟通仅维持在生活琐事的‘事务性交流’上。孩子正在慢慢关上心门，虽然还没锁死，但如果您不主动更换沟通频率，他会习惯性地在心理上与您隔离。",
            3.0: "你们之间现在是‘信号屏蔽’状态。您说的每一句‘为他好’，在他听来都是攻击。不先疏通情感，所有的教育都是无效功。"
        },
        '动力': {
            0.8: "孩子骨子里是有胜负欲和生命力的。他现在的颓废只是‘暂时的死机’，只要重装系统，他自己就能跑起来。",
            1.8: "孩子的生命力处于‘待机状态’。他有想好的愿望，但缺乏持续的推力。他现在的表现取决于环境的压力大小，而不是内在的渴望。这种‘推一下动一下’的状态，最容易在初高中阶段因为压力剧增而彻底熄火。",
            3.0: "孩子已经进入了‘节能模式’，对外界失去了探索欲。这是典型的生命力萎缩我们要通过底层激活，让他重新‘活’过来。"
        },
        '学业': {
            0.8: "孩子的大脑硬件配置其实很高，执行功能没问题。现在的成绩波动，纯粹是情绪或态度的小感冒，很好修补。",
            1.8: "孩子目前的学业表现还在维持，但这是一种‘高代偿’的维持。他是在用双倍的意志力去弥补脑启动效率的不足。这种状态非常危险，一旦功课难度超过他的代偿极限，孩子会迅速出现厌学崩盘。",
            3.0: "这不是态度问题，是**‘大脑CPU过载’**。他写一个字消耗的能量是别人的三倍。他在苦苦支撑，咱们得用脑科学的方法帮他降载。"
        },
        '社会化': {
            0.8: "孩子的社会化属性很好，他渴望链接。这种对集体的归属感，是我们后期把他从手机世界拉回现实的最强抓手。",
            1.8: "孩子尚未完全脱离现实，但电子世界对他吸引力正在盖过现实。他处于社交的‘舒适区’萎缩期。如果现在不干预，他会越来越倾向于在虚拟世界寻找安全感，现实社交能力将持续退化。",
            3.0: "他在现实世界里找不到成就感，只能去虚拟世界吸氧。学校对他来说不是学习的地方，而是‘刑场’，我们要重建他的现实社交自信。"
        }
    }
    
    for dim, score in dim_scores.items():
        thresholds = list(interpretations[dim].keys())
        thresholds.sort()
        # 根据得分找到对应的解读
        if score <= thresholds[0]:
            text = interpretations[dim][thresholds[0]]
        elif score <= thresholds[1]:
            text = interpretations[dim][thresholds[1]]
        else:
            text = interpretations[dim][thresholds[2]]
        
        st.markdown(f"""
        <div class='dim-card'>
            <div class='dim-title'>{dim} ({score:.2f} 分)</div>
            <div class='dim-interpretation'>{text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("### ⚠️ 专项风险探查")
    
    # --- 4. 专项风险维度高分触发（独立显示，不进雷达图）---
    
    # 1. 情绪红灯 (59-66题)
    if any(ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("""<div class='warning-banner bg-red'>
            ⚠️ 【最高级别红色警报】<br>
            监测到孩子目前存在明显的生存危机或极度情绪创伤（如厌世念头、自伤、极度冷漠）。<br>
            此时任何关于学习的督促都是在“火上浇油”。请务必立刻停止施压，寻求专业心理干预，确保生命安全是当前家庭的第一要务！
        </div>""", unsafe_allow_html=True)
    elif emotion_avg >= 1.5:  # 均分超过1.5也触发预警
        st.markdown("""<div class='warning-banner bg-orange'>
            ⚠️ 【情绪安全预警】<br>
            孩子的情绪安全水位较低。这可能表现为长期的情绪低落、易怒或封闭自我。<br>
            建议优先关注孩子的心理状态，建立安全的沟通渠道，再考虑学业问题。
        </div>""", unsafe_allow_html=True)
    
    # 2. ADHD 脑特性 (67-72题)
    if adhd_avg >= 1.5:
        st.markdown("""<div class='warning-banner bg-orange'>
            ⚠️ 【脑特性深度预警】<br>
            孩子表现出典型的高多动、冲动或注意力黑洞特质。这并非“态度不端正”，而是前额叶皮质执行功能发育的暂时性滞后。<br>
            单纯的说教和惩罚只会破坏自尊，建议采用脑科学感统律动结合的行为管理方案进行“弯道超车”。
        </div>""", unsafe_allow_html=True)
    
    # 3. 底层生理基础 (73-78题)
    if bio_avg >= 1.5:
        st.markdown("""<div class='warning-banner bg-blue'>
            ⚠️ 【底层生理地基预警】<br>
            监测到孩子伴有明显的肠脑轴失调或慢性生理压力迹象（如长期过敏、睡眠呼吸障碍、眼圈发青、情绪易炸）。<br>
            当身体处于慢性炎症或缺氧状态时，大脑会自动切换到“生存模式”而非“学习模式”。建议先进行生理节律的系统调理。
        </div>""", unsafe_allow_html=True)
    
    # --- 5. 转化区 ---
    st.markdown(f"""
        <div style='background:#E8EAF6; padding:35px; border-radius:24px; text-align:center; border:1px solid #C5CAE9; margin-top:40px;'>
            <p style='color:#1A237E; font-size:18px; font-weight:600;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div class='report-id'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:22px; font-weight:bold; box-shadow: 0 6px 15px rgba(26,35,126,0.2);">👉 点击添加老师，预约 1V1 解析</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。")
