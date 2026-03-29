import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度定制：锁定首页 + 0 品牌露出 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 彻底屏蔽原生组件 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* 全局背景与字体 */
    .stApp { background: #F4F7F9; text-align: left !important; color: #455A64; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }

    /* 首页锁定：单屏显示，禁止滑动 */
    .home-lock {
        height: 100vh; overflow: hidden; display: flex; flex-direction: column; justify-content: center; padding: 25px;
        background: white; border-radius: 0;
    }

    /* 曹校长品牌三行标题规范 */
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 5px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-top: 5px; }

    /* 引导语 */
    .intro-text { font-size: 18px; color: #546E7A; line-height: 1.8; margin: 30px 0; border-left: 5px solid #FF7043; padding-left: 20px; }

    /* 题目与按钮 */
    .q-text { font-size: 22px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0; }
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; width: 100%; transition: 0.2s;
    }
    div.stButton > button:active { transform: scale(0.98); background-color: #0D47A1; }

    /* 结果页：专项警报 Banner */
    .warn-banner { padding: 25px; border-radius: 18px; margin-bottom: 25px; color: white; font-weight: 600; line-height: 1.8; text-align: left; }
    .bg-red { background: #C62828; box-shadow: 0 8px 20px rgba(198,40,40,0.2); }
    .bg-orange { background: #E65100; box-shadow: 0 8px 20px rgba(230,81,0,0.2); }
    .bg-blue { background: #0D47A1; box-shadow: 0 8px 20px rgba(13,71,161,0.2); }

    /* 1-6 维度解析卡片 */
    .dim-card { padding: 25px; border-radius: 18px; background: white; border: 1px solid #E0E0E0; border-left: 8px solid #1A237E; margin-bottom: 20px; line-height: 1.8; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .dim-title { font-size: 20px; font-weight: 700; color: #1A237E; margin-bottom: 10px; }

    /* 微信转化卡片 */
    .wx-card {
        background: #FFFFFF; padding: 35px; border-radius: 24px; 
        border: 2px solid #E8EAF6; box-shadow: 0 15px 45px rgba(26,35,126,0.15);
        text-align: left; margin-top: 40px;
    }
    .benefit-row { font-size: 17px; font-weight: 700; color: #1A237E; margin: 15px 0; border-bottom: 1px dashed #E8EAF6; padding-bottom: 10px; }
    .rid-box { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 10px 30px; border-radius: 12px; border: 3px dashed #C62828; display: block; margin: 25px auto; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 核心数据库：1-85 题录 ---
QUESTIONS_78 = [
    "1. 3岁前，主要抚养人频繁更换或长期中断。", "2. 早期曾连续2周以上见不到核心抚养人。", 
    "3. 长辈深度参与管教，经常推翻您的决定。", "4. 父母教育标准不一，经常“一宽一严”。",
    "5. 幼年受委屈时极度粘人，无法离开抚养人。", "6. 近两年经历搬家、转学或财务大变动。",
    "7. 处理人际关系(如婆媳、夫妻矛盾)心力交瘁。", "8. 家人虽同住但各忙各的，缺乏交心时刻。",
    "9. 面对孩子问题，感到深深的无力感。", "10. 觉得若不是为了孩子，生活会更精彩自由。",
    "11. 吼叫后陷入“后悔自责一过度补偿”循环。", "12. 觉得孩子某些性格与您讨厌的特质一模一样。",
    "13. 极度在意老师或他人对孩子的负面评价。", "14. 孩子表现与个人价值感挂钩。",
    "15. 管教时心跳加快、胸闷、手抖或大脑空白。", "16. 觉得带孩子是孤军奋战，配偶无实质支持。",
    "17. 睡眠质量差，入睡困难或报复性熬夜。", "18. 内心焦虑、烦躁，很难获得平静。",
    "19. 除了聊学习吃睡，很难进行开心闲聊。", "20. 在校受委屈或丢脸会选择隐瞒，不告知。",
    "21. 对您进房间或动用其物品有明显反感。", "22. 经常反锁屋门，抗拒询问或靠近。",
    "23. 情绪爆发时，本能想靠讲道理或强行压制。", "24. 犯错后第一反应是撒谎、推诿或冷战。",
    "25. 会翻看手机或日记来了解其真实想法。", "26. 不敢在您面前表达真实不满、愤怒或意见。",
    "27. 抱怨在家里没自由，或想要早点离家。", "28. 沟通有明显防御性，您一开口他就烦。",
    "29. 面对挑战，还没做就觉得肯定不行，想退缩。", "30. 游戏输了或遇难题，立刻情绪崩塌或放弃。",
    "31. 过度在意评价，因别人一句话就郁郁寡欢。", "32. 对学习以外的事物也兴致索然，没爱好。",
    "33. 经常说没意思、没劲，感到空虚。", "34. 要求极高且不容许失败，稍不如意就否定自己。",
    "35. 生命力在萎缩，越来越像一个“空心人”。", "36. 即使做感兴趣的事，也难以保持长久热情。",
    "37. 近期对以前喜欢的活动表现出明显冷感。", "38. 磨蹭拖延，通过各种准备动作逃避开始作业。",
    "39. 写作业时神游发呆或手脚小动作不停。", "40. 写字姿势扭曲、力道极重，容易疲劳。",
    "41. 经常“转头就忘”，频繁丢失课本或文具。", "42. 指令“左耳进右耳出”，吼几遍才有反应。",
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
    "79. 是否有过确诊?(多选): ADHD、抑郁/焦虑、其他、暂无",
    "80. 为了解决问题，您之前尝试过哪些方式?(多选): 心理咨询、药物治疗、增加严管、上父母课、其他",
    "81. 之前尝试的方法没有彻底生效的原因是?(多选): 不落地、不系统、没法坚持、孩子不配合、缺乏专业陪跑",
    "82. 目前最迫切想解决的前三个痛点是?(多选): 关系、厌学、专注力差、情绪较大、手机",
    "83. 如诊断根源在于“家庭系统及认知”，您是否有勇气参与改变?(单选): 有、有，但需指导、比较纠结、只想改孩子",
    "84. 填完后，是否愿预约一次专业“全面分析解读”?(单选): 是、否",
    "85. 如果需投入时间扭转局面，您是否有兴趣了解?(单选): 是、否"
]

# --- 4. 逻辑引擎 ---

# A. 首页
if st.session_state.step == 'home':
    st.markdown("""
        <div class='home-lock'>
            <div class='title-l1'>曹校长 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是曹校长。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    
    if cur < 78:
        st.markdown(f"<div class='q-text'>{QUESTIONS_78[cur]}</div>", unsafe_allow_html=True)
        opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
        c1, c2 = st.columns(2)
        for i, (txt, val) in enumerate(opts):
            with (c1 if i % 2 == 0 else c2):
                if st.button(txt, key=f"q_{cur}_{i}"):
                    st.session_state.ans[cur] = val
                    st.session_state.cur += 1; st.rerun()
    else:
        idx = cur - 78
        st.markdown(f"<div class='q-text'>{cur+1}. {BG_QS[idx]}</div>", unsafe_allow_html=True)
        options = BG_QS[idx].split(": ")[1].split("、")
        if idx in [0, 1, 2, 3]: # 多选
            selected = st.multiselect("请选择 (多选)", options, key=f"m_{idx}")
            if st.button("下一题", key=f"nb_{idx}"):
                st.session_state.ans[cur] = ", ".join(selected) if selected else "未选"
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1; st.rerun()
        else: # 单选
            selected = st.radio("请选择", options, key=f"r_{idx}")
            if st.button("下一题", key=f"sb_{idx}"):
                st.session_state.ans[cur] = selected
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1; st.rerun()
    
    if cur > 0:
        st.write("")
        if st.button("⬅ 回到上一题", key="back"):
            st.session_state.cur -= 1; st.rerun()

# C. 结果页
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px;'>📸 提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    ans = st.session_state.ans
    
    # --- 专项警报 (7-9维度) ---
    if any(ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown(f"<div class='warn-banner bg-red'>⚠️ 【最高级别红色警报】<br>监测到孩子目前存在明显的生存危机或极度情绪创伤（如厌世念头、自伤、极度冷漠）。此时任何关于学习的督促都是在“火上浇油”。请务必立刻停止施压，寻求专业心理干预，确保生命安全是当前家庭的第一要务！</div>", unsafe_allow_html=True)
    
    adhd_avg = sum(ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_avg >= 1.5:
        st.markdown(f"<div class='warn-banner bg-orange'>⚠️ 【脑特性深度预警】<br>孩子表现出典型的高多动、冲动或注意力黑洞特质。这并非“态度不端正”，而是前额叶皮质执行功能发育的暂时性滞后。单纯的说教和惩罚只会破坏自尊，建议采用脑科学感统律动方案。</div>", unsafe_allow_html=True)

    bio_avg = sum(ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_avg >= 1.5:
        st.markdown(f"<div class='warn-banner bg-blue'>⚠️ 【底层生理地基预警】<br>监测到孩子伴有明显的肠脑轴失调或慢性生理压力迹象（如过敏、睡眠呼吸障碍、眼圈发青）。当身体处于生存模式时，大脑无法进入学习模式。建议先进行生理节律调理。</div>", unsafe_allow_html=True)

    # --- 1-6 维度长话术 ---
    DIM_TEXTS = {
        "系统": {"r": range(0,8), "lv": ["【稳固】地基牢固，依恋关系安全。","【预警】地基有裂缝，系统承压接近临界。","【危险】地基动摇，孩子缺乏基本安全感。"]},
        "家长": {"r": range(8,18), "lv": ["【优秀】能量充沛，情绪自控力强。","【内耗】内耗严重，管教伴随生理性无力。","【力竭】心理力竭，已丧失引导能力。"]},
        "关系": {"r": range(18,28), "lv": ["【信任】沟通畅通，边界清晰信任高。","【防御】防御性增强，沟通仅维持功能层面。","【断联】情感断联，孩子有明显逃离倾向。"]},
        "动力": {"r": range(28,37), "lv": ["【旺盛】生机勃勃，具备天然抗挫力。","【下行】动力萎缩，出现空心化苗头。","【枯竭】动力枯竭，自我价值感低。"]},
        "学业": {"r": range(37,48), "lv": ["【高效】脑认知高效，执行力强。","【疲劳】生理性疲劳导致执行功能受损。","【宕机】大脑保护性关闭，对学业抗拒。"]},
        "社会化": {"r": range(48,58), "lv": ["【自如】规则意识强，社交半径正常。","【退缩】依赖屏幕，现实社交回避明显。","【受损】社会功能受损，拒绝参与现实生活。"]}
    }

    for dim, info in DIM_TEXTS.items():
        avg = sum(ans.get(i, 0) for i in info['r']) / len(info['r'])
        idx = 2 if avg >= 1.8 else (1 if avg >= 0.8 else 0)
        st.markdown(f"<div class='dim-card'><div class='dim-title'>{dim}维度解析</div>{info['lv'][idx]}</div>", unsafe_allow_html=True)

    # --- 微信转化卡片 ---
    st.markdown(f"""
        <div class='wx-card'>
            <p style='font-size:18px;'>这份报告揭示了孩子的求救，也看见了您的委屈。<br>其实，您不需要独自扛着。</p>
            <p style='font-weight:bold; margin-top:20px; color:#1A237E;'>添加微信您可以获得：</p>
            <div class='benefit-row'>1. 十个维度个性化改善方案</div>
            <div class='benefit-row'>2. 30 分钟 1V1 深度解析</div>
            <div class='benefit-row'>3. 特惠 198 元（原价 598 元）</div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='color:#546E7A; font-size:15px; text-align:center;'>添加时请备注生成的数字</p>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold; text-align:center;">👉 点击添加曹校长，领取以上福利</a>
        </div>
    """, unsafe_allow_html=True)
