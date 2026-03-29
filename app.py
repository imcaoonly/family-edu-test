import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 深度 UI 定制 ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    .stApp { background: #F0F2F5; font-family: "PingFang SC", sans-serif; }
    
    /* 卡片容器：找回边距感 */
    .main-card {
        background: white; border-radius: 20px; padding: 30px 22px;
        margin: 15px auto; box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        max-width: 460px; 
    }

    /* 文字强调 */
    .t1 { font-size: 14px; color: #90A4AE; }
    .t2 { font-size: 34px; font-weight: 800; color: #1A237E; margin: 5px 0; }
    .t3 { font-size: 24px; font-weight: 700; color: #FF7043; }
    .em-red { color: #C62828; font-weight: 800; }

    /* 按钮：深蓝满色，适配卡片宽度 */
    div.stButton > button {
        border-radius: 12px; height: 58px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E !important; color: white !important; border: none;
        width: 100%; transition: 0.3s; margin-bottom: 10px;
    }
    
    /* 选项条：橙色空心 */
    div.stRadio > div > label { 
        border: 2px solid #FF7043 !important; border-radius: 12px; padding: 15px; 
        color: #FF7043 !important; font-weight: 600; margin-bottom: 10px; width: 100%;
    }

    /* 维度卡片三级警戒色 */
    .res-card { padding: 20px; border-radius: 15px; margin-bottom: 15px; background: #FFF; border-top: 6px solid #DDD; }
    .lv-green { border-top-color: #4CAF50; background: #F1F8E9; }
    .lv-orange { border-top-color: #FF9800; background: #FFF3E0; }
    .lv-red { border-top-color: #F44336; background: #FFEBEE; }

    /* 警报 Banner */
    .alert-banner { padding: 15px; border-radius: 10px; color: white; font-weight: 700; margin: 10px 0; font-size: 15px; }
    .bg-red { background: #C62828; } .bg-orange { background: #EF6C00; } .bg-blue { background: #1565C0; }

    /* 专属编号 */
    .rid-box { font-size: 38px; font-weight: 900; color: #C62828; border: 3px dashed #C62828; padding: 10px 25px; display: inline-block; margin: 15px 0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态与题库 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# 1-78 题全量 (由于篇幅仅示意，实际运行时请确保此处包含所有 78 条话术)
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
    {"q": "79. 是否有过确诊？", "type": "multi", "opts": ["ADHD", "抑郁/焦虑", "其他", "暂无"]},
    {"q": "80. 尝试过哪些方式？", "type": "multi", "opts": ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"]},
    {"q": "81. 未生效的原因？", "type": "multi", "opts": ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏陪跑"]},
    {"q": "82. 最迫切想解决的痛点？", "type": "multi", "opts": ["关系焦虑", "厌学崩盘", "专注力差", "情绪易炸", "手机成瘾"]},
    {"q": "83. 是否有勇气参与改变？", "type": "single", "opts": ["有", "有，但需指导", "纠结", "只想改孩子"]},
    {"q": "84. 是否愿预约深度解析？", "type": "single", "opts": ["是", "否"]},
    {"q": "85. 是否有兴趣了解改进方案？", "type": "single", "opts": ["是", "否"]}
]

# --- 3. 逻辑引擎 ---

if st.session_state.step == 'home':
    st.markdown(f"""
        <div class='main-card'>
            <div class='t1'>曹校长 脑科学专业版</div>
            <div class='t2'>家庭教育</div>
            <div class='t3'>十维深度探查表</div>
            <div style='color:#546E7A; line-height:1.7; margin:25px 0; border-left:4px solid #FF7043; padding-left:15px;'>
                这是一场跨越心与脑的对话。<br>
              你好，我是曹校长。<br><br>
             接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
             这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。

            </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 开始深度测评"):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    # 【进度条位置】
    st.progress((cur + 1) / 85)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if cur < 78:
        st.markdown(f"<div style='font-size:20px; font-weight:600; margin-bottom:25px;'>{QUESTIONS_78[cur]}</div>", unsafe_allow_html=True)
        for t, v in [("0 (从不)",0), ("1 (偶尔)",1), ("2 (经常)",2), ("3 (总是)",3)]:
            if st.button(t, key=f"q_{cur}_{v}"):
                st.session_state.ans[cur] = v
                st.session_state.cur += 1
                st.rerun()
    else:
        q = BG_QS[cur-78]
        st.markdown(f"<div style='font-size:20px; font-weight:600; margin-bottom:20px;'>{q['q']}</div>", unsafe_allow_html=True)
        if q['type'] == 'multi':
            sel = st.multiselect("可多选", q['opts'], key=f"m_{cur}")
            if st.button("确认进入下一题", key=f"next_{cur}"):
                st.session_state.ans[cur] = sel
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1
                st.rerun()
        else:
            sel = st.radio("请选择", q['opts'], key=f"s_{cur}", index=None)
            if sel and st.button("确认进入下一题", key=f"next_{cur}"):
                st.session_state.ans[cur] = sel
                if cur == 84: st.session_state.step = 'report'
                else: st.session_state.cur += 1
                st.rerun()

    # 返回按钮：动态 ID 根除报错
    if cur > 0:
        st.write("---")
        if st.button("⬅ 返回上一题", key=f"back_{cur}"):
            st.session_state.cur -= 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == 'report':
    # 结果页逻辑 (同前，包含三色卡片和警报 Banner)
    st.balloons()
    st.success("测评完成！正在生成报告...")
    # ... (省略重复的渲染代码)
