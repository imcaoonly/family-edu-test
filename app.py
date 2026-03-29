import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

# --- 1. UI 深度定制：深蓝品牌色 & 首页遮罩 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    .stApp { background: #F4F7F9; text-align: left !important; color: #455A64; }
    .home-mask {
        padding: 40px 25px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(26, 35, 126, 0.08);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(12px);
        margin-top: 20px;
    }
    .title-l1 { font-size: 16px; color: #90A4AE; font-weight: 500; letter-spacing: 1px; margin-bottom: 8px; }
    .title-l2 { font-size: 38px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 5px; }
    .title-l3 { font-size: 28px; font-weight: 700; color: #FF7043; margin-bottom: 25px; }
    .intro-text {
        font-size: 18px; color: #546E7A; line-height: 1.8; margin-bottom: 35px;
        border-left: 5px solid #FF7043; padding-left: 20px;
    }
    .q-text { font-size: 22px; font-weight: 600; color: #263238; line-height: 1.5; margin: 30px 0; }
    div.stButton > button {
        border-radius: 14px; height: 60px; font-size: 19px !important; font-weight: 700;
        background-color: #1A237E; color: white; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #0D47A1; transform: translateY(-2px); }
    .warning-banner { padding: 22px; border-radius: 16px; margin-bottom: 20px; color: white; font-weight: 600; line-height: 1.6; text-align: left; }
    .bg-red { background: #C62828; box-shadow: 0 4px 12px rgba(198,40,40,0.3); }
    .bg-orange { background: #E65100; box-shadow: 0 4px 12px rgba(230,81,0,0.3); }
    .bg-blue { background: #0D47A1; box-shadow: 0 4px 12px rgba(13,71,161,0.3); }
    .report-id { font-size: 42px; font-weight: 900; color: #C62828; background: #FFF; padding: 15px 35px; border-radius: 15px; border: 3px dashed #C62828; display: inline-block; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心题库录入 (1-78 题全量) ---
QUESTIONS_78 = [
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
    "指令“左耳进右耳出”，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。",
    "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。",
    "坐姿东倒西歪，写作业时头低得非常近。", "处理多步骤指令时，中途断掉就直接放弃。",
    "无法控制地咬指甲、咬衣领或笔头。",
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。",
    "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。",
    "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。",
    "在校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。",
    "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。",
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。",
    "表达过消极厌世或“我消失了更好”的念头。", "身上有不明划痕，或拔头发、啃指甲见血。",
    "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。",
    "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。",
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。",
    "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。",
    "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。",
    "依赖甜食、面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖、面后，莫名亢奋或情绪崩溃。",
    "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。"
]

# --- 3. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 5. 背景信息题库 (79-85 题) ---
BG_QUESTIONS = [
    {"q": "孩子之前是否有过明确的官方诊断？", "type": "radio", "options": ["ADHD/多动症", "抑郁/焦虑", "对立违抗(ODD)", "暂无/不确定"]},
    {"q": "为了解决现状，您尝试过哪些方式？", "type": "multiselect", "options": ["心理咨询", "药物治疗", "严格管控", "参加父母课程", "感统训练"]},
    {"q": "您认为之前的尝试未彻底生效的原因是？", "type": "multiselect", "options": ["不落地", "不系统", "孩子不配合", "大人难坚持", "缺乏专业陪伴"]},
    {"q": "目前您最迫切想解决的三个痛点是？", "type": "multiselect", "options": ["亲子关系", "厌学/拒学", "专注力/成绩", "情绪/易怒", "手机/网瘾"]},
    {"q": "如果根源在家庭系统，您是否有勇气参与改变？", "type": "radio", "options": ["非常有勇气", "有，但需专业指导", "比较纠结", "只想改孩子"]},
    {"q": "如需投入 3-6 个月扭转局面，您是否有兴趣了解？", "type": "radio", "options": ["是", "否"]},
    {"q": "您是否愿意预约一次 1V1 全面深度解析？", "type": "radio", "options": ["愿意", "考虑一下"]}
]

# --- 6. 答题逻辑补充：背景题 ---
if st.session_state.step == 'bg_quiz':
    bg_idx = st.session_state.cur - 78
    if bg_idx < len(BG_QUESTIONS):
        st.progress((st.session_state.cur + 1) / 85)
        q_item = BG_QUESTIONS[bg_idx]
        st.markdown(f"<div class='q-text'>背景信息 {bg_idx+1}: {q_item['q']}</div>", unsafe_allow_html=True)
        
        if q_item['type'] == "radio":
            for i, opt in enumerate(q_item['options']):
                if st.button(opt, key=f"bg_{bg_idx}_{i}", use_container_width=True):
                    st.session_state.ans[st.session_state.cur] = opt
                    st.session_state.cur += 1
                    st.rerun()
        else:
            selected = st.multiselect("请选择（可多选）:", q_item['options'], key=f"multi_{bg_idx}")
            if st.button("下一题 ➡️", use_container_width=True) and selected:
                st.session_state.ans[st.session_state.cur] = selected
                st.session_state.cur += 1
                st.rerun()
    else:
        st.session_state.step = 'report'
        st.rerun()

# --- 7. 结果页逻辑 ---
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是匹配您测评结果的唯一凭证，请截屏保存。</div>", unsafe_allow_html=True)
    
    # --- A. 1-6 维度均分与雷达图 ---
    dim_scores = {}
    interpret_list = []
    
    # 引用第一部分定义的 DIMENSION_INTERPRETS
    # (注：此字典需在第一部分中定义的 DIMENSION_INTERPRETS 包含 系统、家长、关系、动力、学业、社会)
    for dim_name, cfg in DIMENSION_INTERPRETS.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in cfg["range"]) / len(cfg["range"])
        dim_scores[dim_name] = avg
        # 话术匹配逻辑
        if avg <= 0.8:
            txt = f"<b>【{dim_name}维度：低负荷】</b><br>{cfg['low']}"
        elif avg <= 1.8:
            txt = f"<b>【{dim_name}维度：中位波动】</b><br>{cfg['mid']}"
        else:
            txt = f"<b>【{dim_name}维度：高压预警】</b><br>{cfg['high']}"
        interpret_list.append(txt)

    # 雷达图渲染
    fig = go.Figure(data=go.Scatterpolar(
        r=list(dim_scores.values()),
        theta=list(dim_scores.keys()),
        fill='toself',
        line_color='#1A237E',
        fillcolor='rgba(26, 35, 126, 0.3)'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- B. 展示 1-6 维度深度分析 ---
    st.markdown("### 🔍 十维深度深度探查分析")
    for item in interpret_list:
        st.markdown(f"<div style='margin-bottom:20px; line-height:1.6;'>{item}</div>", unsafe_allow_html=True)

    # --- C. 7-9 专项警报逻辑 (原版话术还原) ---
    st.markdown("---")
    
    # 7. 情绪红灯 (59-66题 -> 索引58-65)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)) or st.session_state.ans.get(60, 0) >= 2:
        st.markdown("""<div class='warning-banner bg-red'>
            ⚠️ 【最高级别红色警报】<br>
            监测到孩子目前存在明显的生存危机或极度情绪创伤（如厌世念头、自伤、极度冷漠）。<br>
            此时任何关于学习的督促都是在“火上浇油”。请务必立刻停止施压，寻求专业心理干预，确保生命安全是当前家庭的第一要务！
        </div>""", unsafe_allow_html=True)

    # 8. ADHD 脑特性 (67-72题 -> 索引66-71)
    adhd_score = sum(st.session_state.ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_score >= 1.5:
        st.markdown("""<div class='warning-banner bg-orange'>
            ⚠️ 【脑特性深度预警】<br>
            孩子表现出典型的高多动、冲动或注意力黑洞特质。这并非“态度不端正”，而是前额叶皮质执行功能发育的暂时性滞后。<br>
            单纯的说教和惩罚只会破坏自尊，建议采用脑科学感统律动结合的行为管理方案进行“弯道超车”。
        </div>""", unsafe_allow_html=True)

    # 9. 底层生理基础 (73-78题 -> 索引72-77)
    bio_score = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_score >= 1.5:
        st.markdown("""<div class='warning-banner bg-blue'>
            ⚠️ 【底层生理地基预警】<br>
            监测到孩子伴有明显的肠脑轴失调或慢性生理压力迹象（如长期过敏、睡眠呼吸障碍、眼圈发青、情绪易炸）。<br>
            当身体处于慢性炎症或缺氧状态时，大脑会自动切换到“生存模式”而非“学习模式”。建议先进行生理节律的系统调理。
        </div>""", unsafe_allow_html=True)

    # --- D. 最终转化引导 ---
    st.markdown(f"""
        <div style='background:#E8EAF6; padding:35px; border-radius:24px; text-align:center; border:1px solid #C5CAE9; margin-top:40px;'>
            <p style='color:#1A237E; font-size:18px; font-weight:600;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div class='report-id'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:22px; font-weight:bold; box-shadow: 0 6px 15px rgba(26,35,126,0.2);">👉 点击添加老师，预约 1V1 解析</a>
            <p style='margin-top:15px; color:#546E7A; font-size:14px;'>提示：添加时请备注编号 {st.session_state.rid}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。")
