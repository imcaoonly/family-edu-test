import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度适配 (解决首页标签窄、顶部白条问题) ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    /* 彻底消除顶部白条 */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    .stApp { background: #F8F9FA; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }

    /* 卡片容器 */
    .home-box {
        background: white; border-radius: 24px; padding: 35px 25px;
        margin: 10px auto; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        max-width: 500px; width: 100%;
    }

    /* 品牌标题 */
    .t1 { font-size: 16px; color: #90A4AE; font-weight: 500; }
    .t2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.2; }
    .t3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-top: 5px; }

    /* 按钮与选项：全量满幅对齐 */
    div.stButton > button {
        border-radius: 16px; height: 65px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E !important; color: white !important; border: none; 
        width: 100% !important; margin-bottom: 12px; display: block;
    }
    
    /* 返回按钮：暖橙色空心 */
    button[kind="secondary"] { 
        color: #FF7043 !important; border: 2px solid #FF7043 !important; background: transparent !important;
        font-weight: 600 !important; height: 50px !important; border-radius: 14px !important; width: 100% !important;
    }

    .q-title { font-size: 21px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0; }
    .em-red { color: #E53935 !important; font-weight: 800; }
    
    /* 解析卡片样式 */
    .res-card { padding: 20px; border-radius: 16px; margin-bottom: 15px; border-left: 6px solid; }
    .lv-green { background: #E8F5E9; border-color: #4CAF50; }
    .lv-orange { background: #FFF3E0; border-color: #FF9800; }
    .lv-red { background: #FFEBEE; border-color: #F44336; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态初始化 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 维度长文案数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "texts": [
        "【稳固】家庭系统运行稳健，孩子拥有安全感底色。即使面对外界压力，家庭内部也能提供有效的缓冲。",
        "【预警】系统平衡正在打破，地基出现细微裂缝，孩子开始通过“问题行为”来分担家庭系统的焦虑。",
        "【危险】地基严重动摇。孩子大脑常年处于“战或逃”生存模式，无法调动能量用于学习。"
    ]},
    "家长维度": {"range": range(8,18), "texts": [
        "【优秀】能量充沛，情绪自控力强。能够识别孩子的行为动机，管教温和而坚定。",
        "【内耗】内耗严重，管教伴随生理性无力。长期的焦虑导致家长就像亮起黄灯的仪表盘。",
        "【力竭】心理力竭。对管教已丧失信心，引导功能瘫痪，在潜意识里回避与孩子的深度链接。"
    ]},
    "关系维度": {"range": range(18,28), "texts": [
        "【信任】沟通畅通，边界清晰信任高。关系中不存在控制感，是孩子复原力的源头。",
        "【防御】防御性增强。孩子正在慢慢关上心门，若不更换沟通频率，他会习惯性在心理隔离。",
        "【断联】情感断联。你们之间现在是“信号屏蔽”状态。不疏通情感，所有的教育都是无效功。"
    ]},
    "动力维度": {"range": range(28,37), "texts": [
        "【旺盛】胜负欲强，生命力旺盛。颓废只是“暂时的死机”，重装系统就能跑起来。",
        "【下行】待机状态，缺乏持续推力。这种状态最容易在初高中阶段彻底熄火。",
        "【枯竭】动力彻底枯竭。已进入“节能模式”，对外界失去探索欲。需要通过底层激活让他活过来。"
    ]},
    "学业维度": {"range": range(37,48), "texts": [
        "【高效】脑硬件高配，执行功能没问题。现在的波动纯粹是情绪或态度的感冒。",
        "【疲劳】高代偿维持学业。努力很高产出低下。压力一旦超限会迅速厌学崩盘。",
        "【宕机】CPU 过载，宕机保护性关闭。这是大脑苦苦支撑的生理信号。"
    ]},
    "社会化": {"range": range(48,58), "texts": [
        "【自如】规则意识强，渴望社交归属感。这种链接是我们后期将他从手机拉回现实的最强抓手。",
        "【退缩】屏幕占据生命，现实社交回避。舒适区在萎缩，在虚拟世界寻找安全感。",
        "【受损】现实中找不到成就感。拒绝上学或老师极度抵触。需要重建他的现实社交自信。"
    ]}
}

import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. UI 深度适配 (解决首页标签窄、顶部白条问题) ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    /* 彻底消除顶部白条 */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    .stApp { background: #F8F9FA; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }

    /* 卡片容器 */
    .home-box {
        background: white; border-radius: 24px; padding: 35px 25px;
        margin: 10px auto; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        max-width: 500px; width: 100%;
    }

    /* 品牌标题 */
    .t1 { font-size: 16px; color: #90A4AE; font-weight: 500; }
    .t2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.2; }
    .t3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-top: 5px; }

    /* 按钮与选项：全量满幅对齐 */
    div.stButton > button {
        border-radius: 16px; height: 65px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E !important; color: white !important; border: none; 
        width: 100% !important; margin-bottom: 12px; display: block;
    }
    
    /* 返回按钮：暖橙色空心 */
    button[kind="secondary"] { 
        color: #FF7043 !important; border: 2px solid #FF7043 !important; background: transparent !important;
        font-weight: 600 !important; height: 50px !important; border-radius: 14px !important; width: 100% !important;
    }

    .q-title { font-size: 21px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0; }
    .em-red { color: #E53935 !important; font-weight: 800; }
    
    /* 解析卡片样式 */
    .res-card { padding: 20px; border-radius: 16px; margin-bottom: 15px; border-left: 6px solid; }
    .lv-green { background: #E8F5E9; border-color: #4CAF50; }
    .lv-orange { background: #FFF3E0; border-color: #FF9800; }
    .lv-red { background: #FFEBEE; border-color: #F44336; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态初始化 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 3. 维度长文案数据库 ---
DIM_DATA = {
    "系统维度": {"range": range(0,8), "texts": [
        "【稳固】家庭系统运行稳健，孩子拥有安全感底色。即使面对外界压力，家庭内部也能提供有效的缓冲。",
        "【预警】系统平衡正在打破，地基出现细微裂缝，孩子开始通过“问题行为”来分担家庭系统的焦虑。",
        "【危险】地基严重动摇。孩子大脑常年处于“战或逃”生存模式，无法调动能量用于学习。"
    ]},
    "家长维度": {"range": range(8,18), "texts": [
        "【优秀】能量充沛，情绪自控力强。能够识别孩子的行为动机，管教温和而坚定。",
        "【内耗】内耗严重，管教伴随生理性无力。长期的焦虑导致家长就像亮起黄灯的仪表盘。",
        "【力竭】心理力竭。对管教已丧失信心，引导功能瘫痪，在潜意识里回避与孩子的深度链接。"
    ]},
    "关系维度": {"range": range(18,28), "texts": [
        "【信任】沟通畅通，边界清晰信任高。关系中不存在控制感，是孩子复原力的源头。",
        "【防御】防御性增强。孩子正在慢慢关上心门，若不更换沟通频率，他会习惯性在心理隔离。",
        "【断联】情感断联。你们之间现在是“信号屏蔽”状态。不疏通情感，所有的教育都是无效功。"
    ]},
    "动力维度": {"range": range(28,37), "texts": [
        "【旺盛】胜负欲强，生命力旺盛。颓废只是“暂时的死机”，重装系统就能跑起来。",
        "【下行】待机状态，缺乏持续推力。这种状态最容易在初高中阶段彻底熄火。",
        "【枯竭】动力彻底枯竭。已进入“节能模式”，对外界失去探索欲。需要通过底层激活让他活过来。"
    ]},
    "学业维度": {"range": range(37,48), "texts": [
        "【高效】脑硬件高配，执行功能没问题。现在的波动纯粹是情绪或态度的感冒。",
        "【疲劳】高代偿维持学业。努力很高产出低下。压力一旦超限会迅速厌学崩盘。",
        "【宕机】CPU 过载，宕机保护性关闭。这是大脑苦苦支撑的生理信号。"
    ]},
    "社会化": {"range": range(48,58), "texts": [
        "【自如】规则意识强，渴望社交归属感。这种链接是我们后期将他从手机拉回现实的最强抓手。",
        "【退缩】屏幕占据生命，现实社交回避。舒适区在萎缩，在虚拟世界寻找安全感。",
        "【受损】现实中找不到成就感。拒绝上学或老师极度抵触。需要重建他的现实社交自信。"
    ]}
}

# --- 4. 1-85 全量题库数据 (严格按编号排序) ---
QS_CONTENT = [
    "1. 3岁前，主要抚养人频繁更换或长期中断。", "2. 早期曾连续2周以上见不到核心抚养人。",
    "3. 长辈深度参与管教，经常推翻您的决定。", "4. 父母教育标准不一，经常“一宽一严”。",
    "5. 幼年受委屈时极度粘人，无法离开抚养人。", "6. 近两年经历搬家、转学或财务大变动。",
    "7. 处理人际关系(如婆媳、夫妻矛盾)心力交瘁。", "8. 家人虽同住但各忙各的，缺乏交心时刻。",
    "9. 面对孩子问题，感到深深的无力感。", "10. 觉得若不是为了孩子，生活会更精彩自由。",
    "11. 吼叫后陷入“后悔自责-过度补偿”循环。", "12. 觉得孩子某些性格与您讨厌的特质一模一样。",
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

# --- 5. 测评引擎逻辑 ---
def show_quiz():
    cur = st.session_state.cur
    # 顶部极简进度条
    st.markdown(f"<div style='width:100%;'><div style='width:{(cur+1)/85*100}%; background:#FF7043; height:4px;'></div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='home-box'>", unsafe_allow_html=True)
    if cur < 78:
        st.markdown(f"<div class='q-title'>{QS_CONTENT[cur]}</div>", unsafe_allow_html=True)
        # 选项全满幅
        for label, val in [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]:
            if st.button(label, key=f"q_{cur}_{val}"):
                st.session_state.ans[cur] = val
                st.session_state.cur += 1
                st.rerun()
    else:
        # 背景题 79-85 (逻辑略)
        q = BG_QS[cur-78]
        st.markdown(f"<div class='q-title'>{q['q']}</div>", unsafe_allow_html=True)
        if q['type'] == 'multi':
            sel = st.multiselect("可多选", q['opts'], key=f"m_{cur}")
            if st.button("下一步", key=f"nb_{cur}"):
                st.session_state.ans[cur] = sel
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1
                st.rerun()
        else:
            sel = st.radio("请选择", q['opts'], key=f"s_{cur}", index=None)
            if sel and st.button("下一步", key=f"nb_{cur}"):
                st.session_state.ans[cur] = sel
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1
                st.rerun()

    if cur > 0:
        st.write("---")
        if st.button("⬅ 返回上一题", key=f"bk_{cur}", kind="secondary"):
            st.session_state.cur -= 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. 报告渲染逻辑 (严格按照严重程度变色) ---
def show_report():
    ans = st.session_state.ans
    st.markdown("<div class='home-box'>", unsafe_allow_html=True)
    st.markdown("<div class='t2'>深度解析报告</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#90A4AE; margin-bottom:20px;'>专属编号：{st.session_state.rid}</div>", unsafe_allow_html=True)

    # 1. 解析卡片：循环 6 个维度，根据平均分决定卡片颜色
    idx = 1
    for name, d in DIM_DATA.items():
        score = sum(ans.get(i, 0) for i in d['range']) / len(d['range'])
        # 关键逻辑：按严重程度分颜色 (0-0.8绿, 0.8-1.8橙, 1.8以上红)
        if score >= 1.8: cls = "lv-red"
        elif score >= 0.8: cls = "lv-orange"
        else: cls = "lv-green"
        
        lv_idx = 2 if score >= 1.8 else (1 if score >= 0.8 else 0)
        
        st.markdown(f"""
            <div class='res-card {cls}'>
                <div style='color:#1A237E; font-weight:800; font-size:18px;'>{idx}. {name} (严重指数: {score:.1f})</div>
                <div style='color:#455A64; margin-top:8px; line-height:1.6;'>{d['texts'][lv_idx]}</div>
            </div>
        """, unsafe_allow_html=True)
        idx += 1

    # 2. 专项预警 (59-78)
    if any(ans.get(i, 0) >= 2 for i in range(58, 66)):
        st.error("🚨 【红区警告】孩子目前处于极高压的生存模式，存在心理防线崩塌风险，请务必关注安全。")
    if any(ans.get(i, 0) >= 2 for i in range(66, 72)):
        st.warning("⚠️ 【橙区预警】检测到脑执行功能代偿过度，磨蹭、走神是生理性求救。")
    if any(ans.get(i, 0) >= 2 for i in range(72, 78)):
        st.info("ℹ️ 【蓝区提示】生理硬件基础（睡眠/代谢）不稳定，正在消耗孩子的学习意志。")

    # 3. 最终转化卡片 (三处标红)
    st.markdown(f"""
        <div class='home-box' style='border:2px solid #1A237E; margin-top:40px;'>
            <div style='font-weight:bold; color:#1A237E; font-size:18px;'>添加微信您可以获得：</div>
            <div style='margin:15px 0; line-height:2.2; font-size:17px;'>
                1. 十个维度<span class='em-red'>个性化</span>改善方案<br>
                2. <span class='em-red'>30 分钟 1V1</span> 深度解析<br>
                3. 特惠 <span class='em-red'>198 元</span>（原价 598 元）
            </div>
            <div style='text-align:center;'>
                <div style='font-size:30px; font-weight:900; color:#E53935; border:3px dashed #E53935; padding:10px; border-radius:12px; margin:15px 0;'>{st.session_state.rid}</div>
            </div>
            <button style='width:100%; height:65px; background:#1A237E; color:white; border-radius:15px; font-size:20px; font-weight:bold; border:none;'>👉 复制编号添加曹校长</button>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. 主循环控制 ---
if st.session_state.step == 'home':
    # (首页代码参考第一部分)
    pass
elif st.session_state.step == 'quiz':
    show_quiz()
elif st.session_state.step == 'report':
    show_report()
