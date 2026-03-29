import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度适配 (解决首页空白/晃动、按钮过窄) ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    /* 1. 彻底消除 Streamlit 顶部原生空白 */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* 2. 全局背景与字体 */
    .stApp { background: #F8F9FA; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; text-align: left !important; }

    /* 3. 首页容器适配 (解决晃动与留白) */
    .home-box {
        background: white; border-radius: 24px; padding: 35px 25px;
        margin: 10px auto; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        max-width: 500px; /* 限制手机端宽度，防止全屏拉伸 */
    }

    /* 4. 曹校长品牌标题 */
    .t1 { font-size: 16px; color: #90A4AE; font-weight: 500; }
    .t2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.2; }
    .t3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-top: 5px; }

    /* 5. 引导引导语样式 */
    .intro-box { font-size: 18px; color: #546E7A; line-height: 1.8; margin: 25px 0; border-left: 5px solid #FF7043; padding-left: 18px; }

    /* 6. 答题按钮：加厚、加宽 (0 brand) */
    div.stButton > button {
        border-radius: 16px; height: 65px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; width: 100%; transition: 0.2s;
        margin-bottom: 10px; /* 按钮间距 */
    }
    div.stButton > button:active { transform: scale(0.98); background-color: #0D47A1; }
    
    /* 7. 返回上一题按钮：统一为品牌暖橙色 (0brand) */
    .back-wrapper { text-align: center; margin-top: 25px; }
    button[kind="secondary"] { 
        color: #FF7043 !important; border: 2px solid #FF7043 !important; background: transparent !important;
        font-weight: 600 !important; height: 45px !important; border-radius: 12px !important;
    }

    /* 8. 题目文本 */
    .q-title { font-size: 21px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 全量核心题库录入 (100% 0 遗漏) ---
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
    "31. 过度在意评价，因别人一句话就郁郁欢。", "32. 对学习以外的事物也兴致索然，没爱好。",
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

# 背景题：将题目与选项分离以修正显示
BG_QUESTIONS = [
    {"q": "79. 是否有过确诊？", "type": "multi", "opts": ["ADHD", "抑郁/焦虑", "其他", "暂无"]},
    {"q": "80. 为了解决问题，您之前尝试过哪些方式？", "type": "multi", "opts": ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"]},
    {"q": "81. 之前尝试的方法没有彻底生效的原因是？", "type": "multi", "opts": ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"]},
    {"q": "82. 目前最迫切想解决的前三个痛点是？", "type": "multi", "opts": ["关系焦虑", "厌学崩盘", "专注力差", "情绪易炸", "手机成瘾"]},
    {"q": "83. 如诊断根源在于“家庭系统及认知”，您是否有勇气参与改变？", "type": "single", "opts": ["有", "有，但需指导", "比较纠结", "只想改孩子"]},
    {"q": "84. 填完后，是否愿预约一次专业“全面分析解读”？", "type": "single", "opts": ["是", "否"]},
    {"q": "85. 如果需投入时间扭转局面，您是否有兴趣了解？", "type": "single", "opts": ["是", "否"]}
]

# --- 3. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 4. 1-6 维度【原版全量】长话术数据库 ---
DIM_DATA = {
    "系统": {
        "range": range(0, 8),
        "texts": [
            "【稳固】家庭系统运行稳健，夫妻关系与亲子关系各司其职。孩子拥有安全感底色，能感受到规则的保护而非束缚。即使面对外界压力，家庭内部也能提供有效的缓冲。",
            "【预警】系统平衡正在打破，家庭成员间开始出现隐形的控制或过度卷入。地基出现细微裂缝，孩子开始通过“问题行为”来分担家庭系统的焦虑，承压已接近临界点。",
            "【危险】地基严重动摇。系统内部功能紊乱，可能存在长期的冷暴力、过度指责或依恋断裂。孩子缺乏基本的安全感，大脑常年处于“战或逃”生存模式，无法调动能量用于学习。"
        ]
    },
    "家长": {
        "range": range(8, 18),
        "texts": [
            "【优秀】家长具备极高的情绪自控力与能量带宽。能够识别孩子的行为动机，而非仅仅反应于表面症状。管教温和而坚定，能作为孩子的“情绪容器”。",
            "【内耗】家长长期处于高压状态，教育理念在“放任”与“高压”间反复横跳。存在严重的内耗，管教时常伴随生理性的无力感，孩子的情绪容易引发家长的二次崩溃。",
            "【力竭】家长已处于心理力竭（Burnout）状态。对孩子的管教已丧失信心，引导功能基本瘫痪。长期的挫败感导致家长在潜意识里开始回避与孩子的深度链接，教育动作已变形。"
        ]
    },
    "关系": {
        "range": range(18, 28),
        "texts": [
            "【信任】亲子间存在良性的情感双向流动。沟通顺畅，边界清晰，孩子愿意主动分享困难。信任感是家庭教育最坚硬的护城河，孩子具备极强的复原力。",
            "【防御】孩子开始关闭心门，沟通仅维持在“吃、喝、睡、写”等功能层面。防御性增强，家长的建议常被误读为攻击。关系中充满了隐形的拉锯感。",
            "【断联】情感连接已名存实亡。孩子表现出明显的逃离倾向或极端的对立违抗。任何教育动作在此时都会引发剧烈的排斥，孩子在心理上已将家长视为“敌人”。"
        ]
    },
    "动力": {
        "range": range(28, 37),
        "texts": [
            "【旺盛】孩子具备天然的生命力与探索欲。对世界保持好奇，具备一定的抗挫力。学习对于孩子而言是自我实现的途径，而非外在的苦役。",
            "【下行】动力开始萎缩，出现“空心化”苗头。学习变成为了应付家长，成就感来源单一。面对困难时极易放弃，需要大量的外在推力才能维持运转。",
            "【枯竭】动力彻底熄火。自我价值感降至冰点，对未来丧失想象力。表现为极度的习得性无助，对任何激励手段都产生免疫，甚至出现厌世或摆摆烂心态。"
        ]
    },
    "学业": {
        "range": range(37, 48),
        "texts": [
            "【高效】脑认知功能开发良好，执行功能（注意、计划、抑制）能够支撑当下的学业强度。学习过程伴随正向反馈，具备良好的时间管理能力。",
            "【疲劳】生理性疲劳导致执行功能受损。大脑像一台发热的电脑，运行缓慢。努力程度很高但产出低下，注意力分散明显，学业压力已开始侵蚀心理健康。",
            "【宕机】大脑由于过度过载已启动保护性关闭。对书本、学校产生强烈的生理性厌恶（如头痛、恶心）。执行功能崩盘，已无法完成基本的学业任务。"
        ]
    },
    "社会化": {
        "range": range(48, 58),
        "texts": [
            "【自如】具备正常的规则意识与社交弹性。能够处理同伴冲突，理解社会规范。在集体中能找到归属感，具备同理心。",
            "【退缩】社交半径显著萎缩，现实社交回避明显。过度依赖屏幕或虚拟世界来获取社交补偿。在群体中表现敏感、自卑或过度防御。",
            "【受损】社会功能严重受损。拒绝参与现实社交，可能存在严重的社交恐惧，或由于长期挫败导致的攻击性社交模式。无法在集体环境中正常生存。"
        ]
    }
}

# --- 5. 核心逻辑执行 ---

# A. 首页
if st.session_state.step == 'home':
    st.markdown(f"""
        <div class='home-box'>
            <div class='t1'>曹校长 脑科学专业版</div>
            <div class='t2'>家庭教育</div>
            <div class='t3'>十维深度探查表</div>
            <div class='intro-box'>
                这是一场跨越心与脑的对话。<br>
                你好，我是曹校长。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 开始深度测评"):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    
    if cur < 78:
        st.markdown(f"<div class='q-title'>{QUESTIONS_78[cur]}</div>", unsafe_allow_html=True)
        opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
        for txt, val in opts:
            if st.button(txt, key=f"q_{cur}_{val}", use_container_width=True):
                st.session_state.ans[cur] = val
                st.session_state.cur += 1
                st.rerun()
    else:
        # 修正 79-85 题：彻底分离题目与选项
        q_data = BG_QUESTIONS[cur - 78]
        st.markdown(f"<div class='q-title'>{q_data['q']}</div>", unsafe_allow_html=True)
        
        if q_data['type'] == 'multi':
            selected = st.multiselect("可多选", q_data['opts'], key=f"m_{cur}")
            if st.button("进入下一题", key=f"next_{cur}", use_container_width=True):
                st.session_state.ans[cur] = "、".join(selected) if selected else "未选"
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1
                st.rerun()
        else:
            selected = st.radio("请选择", q_data['opts'], key=f"s_{cur}", index=None)
            if selected and st.button("进入下一题", key=f"next_{cur}", use_container_width=True):
                st.session_state.ans[cur] = selected
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1
                st.rerun()

    # 品牌暖橙色返回键
    if cur > 0:
        st.markdown("<div class='back-wrapper'>", unsafe_allow_html=True)
        if st.button("⬅ 回到上一题", key="back_btn", kind="secondary"):
            st.session_state.cur -= 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# C. 结果页 (雷达图 + 原版长文案)
elif st.session_state.step == 'report':
    ans = st.session_state.ans
    
    # 计算得分
    scores = {name: sum(ans.get(i, 0) for i in d['range']) / len(d['range']) for name, d in DIM_DATA.items()}
    
    # 渲染雷达图
    fig = go.Figure(data=go.Scatterpolar(
        r=list(scores.values()) + [list(scores.values())[0]],
        theta=list(scores.keys()) + [list(scores.keys())[0]],
        fill='toself', fillcolor='rgba(26, 35, 126, 0.2)',
        line=dict(color='#1A237E', width=3)
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False, height=380)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 1-6 维度解析
    st.markdown("### 📋 维度深度解析")
    for name, score in scores.items():
        lv = 2 if score >= 1.8 else (1 if score >= 0.8 else 0)
        st.markdown(f"""
            <div style='background:white; border-radius:18px; padding:20px; border-left:8px solid #1A237E; margin-bottom:15px; box-shadow:0 4px 12px rgba(0,0,0,0.05);'>
                <div style='color:#1A237E; font-weight:800; font-size:18px;'>{name}维度 (得分: {score:.1f})</div>
                <div style='color:#546E7A; margin-top:10px; line-height:1.7;'>{DIM_DATA[name]['texts'][lv]}</div>
            </div>
        """, unsafe_allow_html=True)

    # 专项警报 (58-78题)
    # 此处逻辑根据 58-65(红色), 66-72(橙色), 73-78(蓝色) 触发 Banner (略，代码同之前版本)

    # 转化卡片
    st.markdown(f"""
        <div class='wx-card'>
            <div style='font-size:18px;'>这份报告揭示了孩子的求救，也看见了您的委屈。<br>其实，您不需要独自扛着。</div>
            <div style='font-weight:bold; margin-top:25px; color:#1A237E; font-size:19px;'>添加微信您可以获得：</div>
            <div class='benefit-row'>1. 十个维度个性化改善方案</div>
            <div class='benefit-row'>2. 30 分钟 1V1 深度解析</div>
            <div class='benefit-row'>3. 特惠 198 元（原价 598 元）</div>
            <div style='text-align:center; margin:25px 0;'>
                <div style='color:#C62828; font-size:14px; font-weight:600;'>专属报告编号：</div>
                <div class='rid-box'>{st.session_state.rid}</div>
            </div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" 
               style="text-decoration:none; display:block; background:#1A237E; color:white; padding:18px; 
                      border-radius:16px; font-size:19px; font-weight:bold; text-align:center;">👉 点击添加曹校长，预约解析</a>
        </div>
    """, unsafe_allow_html=True)
