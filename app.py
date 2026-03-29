import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go

# --- 1. UI 深度定制：解决等宽、去白、手机适配 ---
st.set_page_config(page_title="曹校长·脑科学专业版", layout="centered")

st.markdown("""
    <style>
    /* 彻底压制原生组件空白 */
    .block-container { padding-top: 0rem !important; }
    header, footer, [data-testid="stToolbar"] { display: none !important; }
    
    /* 核心：强制所有按钮在手机端 100% 等宽，解决偏移问题 */
    div[data-testid="column"], div.row-widget { width: 100% !important; }
    
    /* 深蓝品牌按钮定制 */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 16px !important;
        background-color: #1A237E !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: none !important;
        margin-bottom: 8px !important;
    }

    /* 返回按钮：暖橙色空心，用于视觉区分 */
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #FF7043 !important;
        border: 2px solid #FF7043 !important;
        height: 48px !important;
        margin-top: 10px !important;
    }

    /* 容器美化 */
    .main-box {
        background: white; border-radius: 24px; padding: 30px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        max-width: 500px; margin: 10px auto;
    }
    .title-l1 { font-size: 15px; color: #90A4AE; letter-spacing: 1px; }
    .title-l2 { font-size: 34px; font-weight: 800; color: #1A237E; line-height: 1.1; }
    .title-l3 { font-size: 24px; font-weight: 700; color: #FF7043; margin-bottom: 20px; }
    .q-text { font-size: 20px; font-weight: 600; color: #263238; margin: 25px 0; line-height: 1.5; }
    
    /* 预警卡片样式 */
    .warning-card { padding: 18px; border-radius: 15px; margin-bottom: 12px; color: white; font-weight: 500; }
    .bg-red { background: #C62828; border-left: 6px solid #5D0F0D; }
    .bg-orange { background: #E65100; border-left: 6px solid #9E3600; }
    .bg-blue { background: #0D47A1; border-left: 6px solid #062C63; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态初始化 ---
if 'step' not in st.session_state:
    st.session_state.update({
        'step': 'home', 
        'cur': 0, 
        'ans': {}, 
        'rid': str(random.randint(100000, 999999))
    })

# --- 3. 全量题库 (对照《系统识别题库.docx》) ---
QUESTIONS_85 = [
    "1. 3岁前，主要抚养人频繁更换或长期中断。", "2. 早期曾连续2周以上见不到核心抚养人。",
    "3. 长辈深度参与管教，经常推翻您的决定。", "4. 父母教育标准不一，经常“一宽一严”。",
    "5. 幼年受委屈时极度粘人，无法离开抚养人。", "6. 近两年经历搬家、转学或财务大变动。",
    "7. 处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "8. 家人虽同住但各忙各的，缺乏交心时刻。",
    "9. 面对孩子问题，感到深深的无力感。", "10. 觉得若不是为了孩子，生活会更精彩自由。",
    "11. 吼叫后陷入“后悔自责—过度补偿”循环。", "12. 觉得孩子某些性格与您讨厌的特质一模一样。",
    "13. 极度在意老师或他人对孩子的负面评价。", "14. 孩子表现与个人价值感挂钩，不出色感失败。",
    "15. 管教时心跳加快、胸闷、手抖或大脑空白。", "16. 觉得带孩子是孤军奋战，配偶无实质支持。",
    "17. 睡眠质量差，入睡困难或报复性熬夜。", "18. 内心焦虑、烦躁，很难获得平静。",
    "19. 除了聊学习吃睡，很难进行开心闲聊。", "20. 在校受委屈或丢脸会选择隐瞒，不告知。",
    "21. 对您进房间或动用其物品有明显反感。", "22. 经常反锁屋门，抗拒询问或靠近。",
    "23. 情绪爆发时，本能想靠讲道理或强行压制。", "24. 犯错后第一反应是撒谎、推诿或冷战。",
    "25. 会翻看手机或日记来了解其真实想法。", "26. 不敢在您面前表达真实不满、愤怒或意见。",
    "27. 抱怨在家里没自由，或想要早点离家。", "28. 沟通有明显防御性，您一开口他就烦。",
    "29. 面对挑战，还没做就觉得肯定不行，想退缩。", "30. 游戏输了或遇难题，立刻情绪崩塌或放弃。",
    "31. 过度在意评价，因别人一句话就郁郁欢欢。", "32. 对学习以外的事物也兴致索然，没爱好。",
    "33. 经常说没意思、没劲，感到空虚。", "34. 要求极高且不容许失败，稍不如意就否定自己。",
    "35. 生命力在萎缩，越来越像一个“空心人”。", "36. 即使做感兴趣的事，也难以保持长久热情。",
    "37. 近期对以前喜欢的活动表现出明显冷感。", "38. 磨蹭拖延，通过各种准备动作逃避开始作业。",
    "39. 写作业时神游发呆或手脚小动作不停。", "40. 写字姿势扭曲、力道极重，容易疲劳。",
    "41. 经常“转头就忘”，频繁丢失课本或文具。", "42. 指令“左耳进右耳出”，吼几遍才有反应。",
    "43. 阅读或抄写频繁跳行、漏字或笔画写反。", "44. 面对复杂任务，完全不知道从哪下手。",
    "45. 启动效率极低，反应速度明显慢于同龄人。", "46. 坐姿东倒西歪，写作业时头低得非常近。",
    "47. 处理多步骤指令时，中途断掉就直接放弃。", "48. 无法控制地咬指甲、咬衣领或笔头。",
    "49. 电子屏幕占据除学习外的绝大部分时间。", "50. 收手机时出现剧烈情绪爆发或肢体对抗。",
    "51. 为了玩手机经常撒谎，或熬夜偷玩。", "52. 提到上学或考试，有头痛腹痛等生理反应。",
    "53. 拒绝社交，有明显的社交回避或社恐。", "54. 老师反馈纪律性差、孤僻或难以融入集体。",
    "55. 在学校没有可以倾诉、互助支持的朋友。", "56. 对校园规则极度不耐受，有明显逆反心。",
    "57. 公共场合表现出局促感或不合时宜行为。", "58. 电子产品是爆发家庭冲突的最主要诱因。",
    "59. 近期长时间不洗头不换衣，不在意个人卫生。", "60. 食欲极端波动（暴食或长期厌食）。",
    "61. 表达过消极厌世或“我消失了更好”的念头。", "62. 身上有不明划痕，或拔头发、啃指甲见血。",
    "63. 对未来不抱期待，拒绝讨论任何计划。", "64. 睡眠节律彻底混乱，黑白颠倒。",
    "65. 对最亲近的人也表现出极度冷漠和隔绝。", "66. 提到学校或老师，浑身发抖或剧烈抵触。",
    "67. 玩游戏专注，面对学习坐不住、易走神。", "68. 安静环境下，也无法停止身体扭动或晃动。",
    "69. 无法耐心等别人说完，经常抢话、插话。", "70. 在排队或等待场合，表现出超越年龄的焦躁。",
    "71. 短时记忆黑洞，刚交代的事转头就忘。", "72. 做作业或听讲时，极易被微小动静吸引。",
    "73. 依赖甜食、面食，极度讨厌蔬菜。", "74. 伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "75. 长期过敏体质（鼻炎、腺样体、湿疹等）。", "76. 进食大量糖、面后，莫名亢奋或情绪崩溃。",
    "77. 睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "78. 睡眠充足但眼圈常年发青或水肿。"
]

BG_QS_DATA = [
    {"q": "79. 孩子是否有过确诊？", "type": "multi", "opts": ["ADHD", "抑郁/焦虑", "其他", "暂无"]},
    {"q": "80. 为了解决问题，您尝试过哪些方式？", "type": "multi", "opts": ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"]},
    {"q": "81. 方法未生效的原因？", "type": "multi", "opts": ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"]},
    {"q": "82. 目前最迫切想解决的痛点？", "type": "multi", "opts": ["关系焦虑", "厌学崩盘", "专注力差", "情绪易炸", "手机成瘾"]},
    {"q": "83. 您是否有勇气参与改变？", "type": "single", "opts": ["有", "有，但需指导", "纠结", "只想改孩子"]},
    {"q": "84. 是否愿预约专业“全面分析解读”？", "type": "single", "opts": ["是", "否"]},
    {"q": "85. 是否有兴趣了解长期扭转方案？", "type": "single", "opts": ["是", "否"]}
]# --- 4. 逻辑引擎：处理答题与回溯 ---

def get_level(score):
    """根据均分判断话术层级：0.8分以下为低，1.8分以下为中，以上为高"""
    if score <= 0.8: return "low"
    if score <= 1.8: return "mid"
    return "high"

if st.session_state.step == 'home':
    st.markdown("""
        <div class='main-box'>
            <div class='title-l1'>HelloADHDer 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div style='color:#546E7A; line-height:1.8; margin-bottom:30px; border-left:5px solid #FF7043; padding-left:15px;'>
                这是一场跨越心与脑的对话。<br>你好，我是曹校长。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。这不仅是一份问卷，更是给孩子和你自己一次被“看见”的机会。
            </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", key="start_game_btn"):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    # 顶部进度条
    st.progress((cur + 1) / 85)
    
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    
    # --- 1-78 题：打分制 ---
    if cur < 78:
        st.markdown(f"<div class='q-text'>{QUESTIONS_85[cur]}</div>", unsafe_allow_html=True)
        opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
        # 强制单列布局，确保手机端按钮 100% 宽度且整齐
        for i, (txt, val) in enumerate(opts):
            if st.button(txt, key=f"q_{cur}_opt_{val}"):
                st.session_state.ans[cur] = val
                st.session_state.cur += 1
                st.rerun()
                
    # --- 79-85 题：背景信息 ---
    elif cur < 85:
        q = BG_QS_DATA[cur-78]
        st.markdown(f"<div class='q-text'>{q['q']}</div>", unsafe_allow_html=True)
        if q['type'] == 'multi':
            sel = st.multiselect("请选择（可多选）", q['opts'], key=f"multi_{cur}")
            if st.button("下一步", key=f"next_{cur}"):
                if not sel: st.warning("请至少选择一项")
                else:
                    st.session_state.ans[cur] = sel
                    st.session_state.cur += 1
                    st.rerun()
        else:
            sel = st.radio("请选择", q['opts'], key=f"radio_{cur}", index=None)
            if st.button("下一步", key=f"next_{cur}"):
                if sel is None: st.warning("请选择一项")
                else:
                    st.session_state.ans[cur] = sel
                    if cur == 84: st.session_state.step = 'report'
                    else: st.session_state.cur += 1
                    st.rerun()

    # --- 核心修复：返回上一题 (解决 TypeError) ---
    if cur > 0:
        st.write("---")
        if st.button("⬅ 返回上一题", key=f"back_btn_logic_{cur}", kind="secondary"):
            st.session_state.cur = max(0, st.session_state.cur - 1)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. 深度解析报告页 ---
elif st.session_state.step == 'report':
    # 严格按照《指南》划分维度题号
    DIM_MAP = {
        "系统": list(range(0, 8)),    # 1-8题
        "家长": list(range(8, 18)),   # 9-18题
        "关系": list(range(18, 28)),  # 19-28题
        "动力": list(range(28, 37)),  # 29-37题
        "学业": list(range(37, 48)),  # 38-48题
        "社会化": list(range(48, 58)) # 49-58题
    }
    # 计算维度均分
    scores = {name: sum(st.session_state.ans.get(i, 0) for i in idxs)/len(idxs) for name, idxs in DIM_MAP.items()}
    
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.markdown("<div class='title-l2' style='text-align:center;'>深度解析报告</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; color:#90A4AE; margin-bottom:15px;'>报告编号：{st.session_state.rid}</div>", unsafe_allow_html=True)
    
    # 雷达图渲染
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(scores.values()), theta=list(scores.keys()), fill='toself', 
                                  fillcolor='rgba(26, 35, 126, 0.3)', line=dict(color='#1A237E', width=3)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False, height=380, margin=dict(l=40,r=40,t=30,b=30))
    st.plotly_chart(fig, use_container_width=True)

    # --- 专项风险预警 (红/黄/蓝牌) ---
    # 1. 情绪红灯 (59-66题)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warning-card bg-red'>⚠️ 红色警报：情绪水位极低。孩子目前处于生存危机或极度创伤状态，请立刻停止施压，寻求专业心理干预。</div>", unsafe_allow_html=True)

    # 2. ADHD 预警 (67-72题)
    adhd_avg = sum(st.session_state.ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_avg >= 1.5:
        st.markdown("<div class='warning-card bg-orange'>⚠️ 橙色预警：典型 ADHD 脑特性。孩子表现出的多动或走神非态度问题，而是前额叶执行功能滞后。</div>", unsafe_allow_html=True)

    # 3. 生理底层 (73-78题)
    bio_avg = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_avg >= 1.5:
        st.markdown("<div class='warning-card bg-blue'>⚠️ 蓝色预警：底层生理失调。监测到肠脑轴或慢性生理压力，建议先调理睡眠与节律。</div>", unsafe_allow_html=True)

    # --- 1-6 维度三层级话术 ---
    st.markdown("### 🔍 维度深度拆解")
    texts = {
        "系统": {
            "low": "您的家庭地基非常扎实，孩子安全感底色亮，好起来会比别人快得多。",
            "mid": "家庭基础稳定但存在‘微损耗’，建议统一教育标准，防止结构性问题。",
            "high": "家里的‘气压’不稳定。孩子能量全用来维稳了，无力搞学习。"
        },
        "家长": {
            "low": "您的心理建设很好。现在的困局不是您无能，而是缺一把精准的‘手术刀’。",
            "mid": "您正处于‘育儿倦怠’边缘。现在的您像亮起黄灯的仪表盘，该停下来修整了。",
            "high": "您的油箱已经干了。焦灼感会传染给孩子，咱们得先帮您把油加满。"
        },
        "关系": {
            "low": "宝贵的是孩子还愿意说真心话。只要情感管道通着，任何训练都能事半功倍。",
            "mid": "缺乏‘深链接’。孩子正在慢慢关上心门，若不换频率，他会习惯性隔离。",
            "high": "处于‘信号屏蔽’状态。不先疏通情感，所有的教育都是无效功。"
        },
        "动力": {
            "low": "孩子骨子里是有胜负欲的。现在的颓废只是‘暂时死机’，重启就好。",
            "mid": "生命力处于‘待机状态’。推一下动一下，最容易在压力大时彻底熄火。",
            "high": "已进入‘节能模式’。这是典型的生命力萎缩，需通过底层激活让他活过来。"
        },
        "学业": {
            "low": "大脑硬件配置高，执行功能没问题。现在的波动纯粹是‘小感冒’，好修补。",
            "mid": "属于‘高代偿’维持。他在用双倍意志力弥补脑效率不足，一旦难度超限就会崩盘。",
            "high": "这是‘大脑CPU过载’。他写一个字消耗别人三倍能量，必须降载。"
        },
        "社会化": {
            "low": "社会化属性好，渴望链接。这是把他从手机拉回现实的最强抓手。",
            "mid": "电子世界吸引力正盖过现实。如果不干预，他会彻底逃避到虚拟世界。",
            "high": "在现实找不到成就感只能去网络吸氧。学校对他来说是‘刑场’，需重建自信。"
        }
    }

    for dim, score in scores.items():
        lvl = get_level(score)
        with st.expander(f"{dim}维度：{score:.1f}分 ({'稳固' if lvl=='low' else '预警' if lvl=='mid' else '危险'})", expanded=(score > 1.5)):
            st.write(texts[dim][lvl])

    # --- 转化区 ---
    st.markdown(f"""
        <div style='background:#E8EAF6; padding:35px; border-radius:24px; text-align:center; border:1px solid #C5CAE9; margin-top:30px;'>
            <p style='color:#1A237E; font-size:18px; font-weight:600;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div style='font-size:42px; font-weight:900; color:#C62828; margin:15px 0; border:3px dashed #C62828; display:inline-block; padding:10px 30px;'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/..." target="_blank" style="text-decoration:none;">
                <div style="background:#1A237E; color:white; padding:18px; border-radius:15px; font-weight:bold; font-size:22px;">👉 点击预约 1V1 深度解析</div>
            </a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
