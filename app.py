import streamlit as st
import random
import plotly.graph_objects as go

# --- 1. 样式与双行标题定制 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .title-container { text-align: center; margin-bottom: 30px; line-height: 1.4; }
    .title-row1 { font-size: 32px; font-weight: 800; color: #1B5E20; display: block; }
    .title-row2 { font-size: 28px; font-weight: 700; color: #1B5E20; display: block; }
    .title-sub { font-size: 18px; color: #666; font-weight: 400; display: block; margin-top: 8px; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心题库：严格对标《系统识别题库》(1-78题) ---
QUESTIONS_SCORE = [
    "3岁前，主要抚养人频繁更换或长期中断。", "早期曾连续2周以上见不到核心抚养人。", "长辈深度参与管教，经常推翻您的决定。",
    "父母教育标准不一，经常“一宽一严”。", "幼年受委屈时极度粘人，无法离开抚养人。", "近两年经历搬家、转学或财务大变动。",
    "处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "家人虽同住但各忙各的，缺乏交心时刻。", # 维度1: 系统
    "面对孩子问题，感到深深的无力感。", "觉得若不是为了孩子，生活会更精彩自由。", "吼叫后陷入“后悔自责—过度补偿”循环。",
    "觉得孩子某些性格与您讨厌的特质一模一样。", "极度在意老师或他人对孩子的负面评价。", "孩子表现与个人价值感挂钩，不出色感失败。",
    "管教时心跳加快、胸闷、手抖或大脑空白。", "觉得带孩子是孤军奋战，配偶无实质支持。", "睡眠质量差，入睡困难或报复性熬夜。", "内心焦虑、烦躁，很难获得平静。", # 维度2: 家长
    "除了聊学习吃睡，很难进行开心闲聊。", "在校受委屈或丢脸会选择隐瞒，不告知。", "对您进房间或动用其物品有明显反感。",
    "经常反锁屋门，抗拒询问或靠近。", "情绪爆发时，本能想靠讲道理或强行压制。", "犯错后第一反应是撒谎、推诿或冷战。",
    "会翻看手机或日记来了解其真实想法。", "不敢在您面前表达真实不满、愤怒或意见。", "抱怨在家里没自由，或想要早点离家。", "沟通有明显防御性，您一开口他就烦。", # 维度3: 关系
    "面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，立刻情绪崩塌或放弃。", "过度在意评价，因别人一句话就郁郁孤欢。",
    "对学习以外的事物也兴致索然，没爱好。", "经常说没意思、没劲，感到空虚。", "要求极高且不容许失败，稍不如意就否定自己。",
    "生命力在萎缩，越来越像一个“空心人”。", "即使做感兴趣的事，也难以保持长久热情。", "近期对以前喜欢的活动表现出明显冷感。", # 维度4: 动力
    "磨蹭拖延，通过各种准备动作逃避开始作业。", "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。",
    "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。", "阅读或抄写频繁跳行、漏字或笔画写反。",
    "面对复杂任务，完全不知道从哪下手。", "启动效率极低，反应速度明显慢于同龄人。", "坐姿东倒西歪，写作业时头低得非常近。",
    "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。", # 维度5: 学业
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。", "为了玩手机经常撒谎，或熬夜偷玩。",
    "提到上学或考试，有头痛腹痛等生理反应。", "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。",
    "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。", "公共场合表现出局促感或不合时宜行为。",
    "电子产品是爆发家庭冲突的最主要诱因。", # 维度6: 社会化
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。", "表达过消极厌世或“我消失了更好”的念头。",
    "身上有不明划痕，或拔头发、啃指甲见血。", "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。",
    "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。", # 维度7: 情绪
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。", "无法耐心等别人说完，经常抢话、插话。",
    "在排队或等待场合，表现出超越年龄的焦躁。", "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。", # 维度8: 注意
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。", "长期过敏体质（鼻炎、腺样体、湿疹等）。",
    "进食大量糖面后，莫名亢奋或情绪崩溃。", "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。" # 维度9: 生理
]

# --- 3. 初始化 ---
if 'idx' not in st.session_state:
    st.session_state.update({'step':"home", 'idx':0, 'ans':{}, 'rid':str(random.randint(100000, 999999))})

def next_q(val):
    st.session_state.ans[st.session_state.idx] = val
    st.session_state.idx += 1
    st.rerun()

# --- 4. 逻辑分段运行 ---
if st.session_state.step == "home":
    st.markdown("""<div class='title-container'><span class='title-row1'>家庭教育</span><span class='title-row2'>十维深度探查</span><span class='title-sub'>(脑科学版)</span></div>""", unsafe_allow_html=True)
    st.info("这是一场跨越心与脑的对话，请给孩子和自己一次被“看见”的机会。")
    if st.button("开始深度测评", use_container_width=True):
        st.session_state.step = "testing"; st.rerun()

elif st.session_state.step == "testing":
    cur = st.session_state.idx
    
    # 物理隔离计分题 (0-77 索引)
    if cur < 78:
        st.progress((cur + 1) / 85)
        st.write(f"第 {cur + 1} 题 / 共 85 题")
        st.markdown(f"### {QUESTIONS_SCORE[cur]}")
        cols = st.columns(2)
        if cols[0].button("0 (从不)", use_container_width=True): next_q(0)
        if cols[1].button("1 (偶尔)", use_container_width=True): next_q(1)
        if cols[0].button("2 (经常)", use_container_width=True): next_q(2)
        if cols[1].button("3 (总是)", use_container_width=True): next_q(3)
        if cur > 0 and st.button("⬅️ 返回上题"): st.session_state.idx -= 1; st.rerun()
            
    # 物理隔离背景题 (78-84 索引)
    elif cur < 85:
        bg_qs = [
            ("是否有过确诊史？", ["ADHD", "抑郁/焦虑", "对立违抗", "暂无"], "multi"),
            ("尝试过哪些干预？", ["心理咨询", "药物治疗", "感统/律动", "父母课", "其他"], "multi"),
            ("失效主因？", ["不够系统", "不够落地", "孩子抗拒", "缺乏陪跑"], "multi"),
            ("最迫切痛点？", ["厌学手机", "情绪风险", "专注力成绩", "亲子冲突"], "multi"),
            ("改变勇气？", ["非常有信心", "想尝试但无力", "比较纠结", "只想改孩子"], "single"),
            ("预约解读？", ["是", "否"], "single"),
            ("您的身份？", ["爸爸", "妈妈", "其他"], "single")
        ]
        q_txt, opts, mode = bg_qs[cur - 78]
        st.subheader(f"背景摸排 ({cur+1}/85)")
        st.markdown(f"### {q_txt}")
        u_in = st.multiselect("请勾选:", opts) if mode == "multi" else st.radio("请选择:", opts, index=None)
        
        if st.button("生成最终报告" if cur == 84 else "继续下一步", use_container_width=True, disabled=not u_in):
            st.session_state.ans[cur] = u_in
            if cur < 84:
                st.session_state.idx += 1; st.rerun()
            else:
                st.session_state.step = "report"; st.rerun()

elif st.session_state.step == "report":
    st.balloons()
    st.markdown("<h2 style='text-align: center;'>十维深度探查报告</h2>", unsafe_allow_html=True)
    
    # 维度映射逻辑
    DIM_IDX = {
        "系统": range(0,8), "家长": range(8,18), "关系": range(18,28),
        "动力": range(28,37), "学业": range(37,48), "社会化": range(48,58),
        "情绪": range(58,66), "注意": range(66,72), "生理": range(72,78)
    }
    res = {k: round(sum(st.session_state.ans.get(i,0) for i in v)/len(v), 2) for k,v in DIM_IDX.items()}

    # 绘制雷达图
    radar_labels = ["系统", "家长", "关系", "动力", "学业", "社会化"]
    fig = go.Figure(data=go.Scatterpolar(r=[res[l] for l in radar_labels], theta=radar_labels, fill='toself'))
    st.plotly_chart(fig, use_container_width=True)

    # 深度解析与转化引导
    st.success(f"报告编号：{st.session_state.rid}")
    st.markdown(f"""
    ---
    这份报告揭示了孩子的求救，也看见了您的委屈。
    添加微信备注编号 **{st.session_state.rid}** 即可获得：
    1. 十个维度个性化改善方案 | 2. 30分钟 1V1 深度解析
    """)
    st.link_button("👉 点击添加老师，预约深度诊断", "https://work.weixin.qq.com/ca/cawcde91ed29d8de9f", use_container_width=True)
