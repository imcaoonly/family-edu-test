import streamlit as st
import random

# --- 1. 极致视觉定制 (左对齐 & 深灰蓝 & 品牌绿) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    .brand-box { text-align: center; margin-bottom: 35px; }
    .t1 { font-size: 38px; font-weight: 800; color: #1B5E20; }
    .t2 { font-size: 32px; font-weight: 700; color: #2E7D32; margin-top: 5px; }
    .t3 { font-size: 16px; color: #888; border-top: 1px solid #eee; display: inline-block; padding-top: 8px; margin-top: 10px; }
    
    .warm-box { background: #F9FBF9; padding: 25px; border-radius: 20px; border-left: 6px solid #A5D6A7; color: #444; font-size: 18px; line-height: 1.8; margin-bottom: 30px; text-align: left; }
    
    .q-container { text-align: left !important; margin: 30px 0; }
    .q-text { font-size: 22px; font-weight: 600; color: #455A64; line-height: 1.6; }
    
    .res-card { padding: 25px; border-radius: 20px; background: #FFF; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 8px solid #E0E0E0; text-align: left; }
    .res-high { border-left-color: #D32F2F !important; background-color: #FFF5F5; border: 1.5px solid #FFEBEE; border-left-width: 8px; }
    
    .alert-banner { background: #D32F2F; color: white; padding: 20px; border-radius: 15px; font-weight: bold; margin-bottom: 25px; line-height: 1.6; text-align: left; }
    
    .wx-section { background: #E8F5E9; border-radius: 25px; padding: 35px; text-align: center; margin-top: 40px; border: 1px solid #C8E6C9; }
    .promo-list { text-align: left; display: inline-block; margin: 20px 0; font-size: 19px; line-height: 2.2; color: #1B5E20; font-weight: 500; }
    .report-id { font-size: 42px; font-weight: 900; color: #D32F2F; background: #FFFFFF; padding: 15px 35px; border-radius: 15px; border: 3px dashed #D32F2F; display: inline-block; margin: 20px 0; letter-spacing: 3px; }
    
    .screenshot-tip { color: #D32F2F; font-weight: bold; background: #FFEBEE; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px solid #FFCDD2; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 完整 1-85 题库 [cite: 6-91] ---
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
    "近期对以前喜欢的活动表现出明显冷感。", "磨蹭拖延，通过各种准备动作逃避开始作业。",
    "写作业时神游发呆或手脚小动作不停。", "写字姿势扭曲、力道极重，容易疲劳。",
    "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进耳出”，吼几遍才有反应。",
    "阅读或抄写频繁跳行、漏字或笔画写反。", "面对复杂任务，完全不知道从哪下手。",
    "启动效率极低，反应速度明显慢于同龄人。", "坐姿东倒西歪，写作业时头低得非常近。",
    "处理多步骤指令时，中途断掉就直接放弃。", "无法控制地咬指甲、咬衣领或笔头。",
    "电子屏幕占据除学习外的绝大部分时间。", "收手机时出现剧烈情绪爆发或肢体对抗。",
    "为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，有头痛腹痛等生理反应。",
    "拒绝社交，有明显的社交回避或社恐。", "老师反馈纪律性差、孤僻或难以融入集体。",
    "在学校没有可以倾诉、互助支持的朋友。", "对校园规则极度不耐受，有明显逆反心。",
    "公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。",
    "近期长时间不洗头不换衣，不在意个人卫生。", "食欲极端波动（暴食或长期厌食）。",
    "表达过消极厌世或“我消失了更好”的念头。", "身上有不明划痕，或拔头发、啃指甲见血。",
    "对未来不抱期待，拒绝讨论任何计划。", "睡眠节律彻底混乱，黑白颠倒。",
    "对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，浑身发抖或剧烈抵触。",
    "玩游戏专注，面对学习坐不住、易走神。", "安静环境下，也无法停止身体扭动或晃动。",
    "无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，表现出超越年龄的焦躁。",
    "短时记忆黑洞，刚交代的事转头就忘。", "做作业或听讲时，极易被微小动静吸引。",
    "依赖甜食面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。",
    "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖面后，莫名亢奋或情绪崩溃。",
    "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。"
]

BG_QS = [
    ("是否有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
    ("之前尝试过哪些方式？", ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"], "multi"),
    ("方法未生效的原因？", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏陪跑"], "multi"),
    ("最迫切的前三个痛点？", ["关系", "厌学", "专注力", "情绪", "手机"], "multi"),
    ("是否有勇气参与家庭改变？", ["有", "需指导", "纠结", "只想改孩子"], "single"),
    ("是否愿预约专业解读？", ["是", "否"], "single"),
    ("是否有兴趣了解扭转方案？", ["是", "否"], "single")
]

# --- 3. 完整诊断话术库 (无省略版) ---
DIAG_DATA = {
    "系统维度 (1-8题)": {
        "range": range(0, 8),
        "texts": [
            "【稳固】家庭地基牢固，早期依恋关系安全，环境变动适应力强。目前的挑战多为表层技巧问题。",
            "【内耗】地基出现裂缝。早期抚养或环境变动留下了隐形不安，系统承压接近临界点，家庭动力开始偏移。",
            "【动荡】地基动摇。系统动力紊乱，孩子在家庭中缺乏基本的安全感支撑，任何教养技巧在动摇的地基上都难以生效。"
        ]
    },
    "家长维度 (9-18题)": {
        "range": range(8, 18),
        "texts": [
            "【能量充沛】能够理性区分自身价值与孩子的表现，情绪自控力强，具备高质量引导的心理空间。",
            "【内耗预警】能量消耗严重。焦虑感开始渗透，管教时常伴随无力感。您的疲惫已成为孩子压力的来源之一。",
            "【心理力竭】家长处于崩溃边缘，自责与焦虑交织。当前状态下，您的任何教育输出可能都会转化为负向压力。"
        ]
    },
    "关系维度 (19-28题)": {
        "range": range(18, 28),
        "texts": [
            "【亲密信任】沟通渠道畅通，尊重边界，孩子对父母有极高的情感信任，家是孩子最安全的港湾。",
            "【防御增强】沟通仅维持在功能层面（吃喝学）。深度情感链接开始阻塞，孩子开始在心理上对家关门。",
            "【情感断联】孩子出现明显的逃离倾向。沟通伴随强烈的防御或冷战，亲子关系已进入“权力斗争”或“消极避世”阶段。"
        ]
    },
    "动力维度 (29-37题)": {
        "range": range(28, 37),
        "texts": [
            "【生机勃勃】生命力旺盛，具备天然的抗挫力，对事物保持长久的探索热情与自我价值感。",
            "【动力下行】开始畏难、退缩。生命力出现“空心化”苗头，以往的爱好开始减退，对未来缺乏期待。",
            "【动力枯竭】出现明显的消极厌世或极度冷感。自我价值感降至冰点，这种“习得性无助”是脑部奖赏系统低迷的信号。"
        ]
    },
    "学业维度 (38-47题)": {
        "range": range(37, 48),
        "texts": [
            "【脑力高效】脑认知功能处于高效区，指令转化快，具备良好的任务启动速度与专注坚持力。",
            "【功能疲劳】磨蹭、跳行、易分神。这不是态度问题，而是生理性疲劳导致执行功能受损，大脑在频繁“罢工”。",
            "【功能宕机】大脑保护性关闭。无法执行多步骤指令，学业压力已转化为生理抗拒。此时强逼学习会进一步损伤脑神经。"
        ]
    },
    "社会化维度 (48-58题)": {
        "range": range(48, 58),
        "texts": [
            "【社交自如】规则意识清晰，能平衡电子产品与现实生活，具备良好的同伴交往能力与抗诱惑力。",
            "【社交退缩】开始过度依赖屏幕寻找慰藉，对校园规则产生抵触。社交半径缩窄，现实价值感正在被虚拟世界吞噬。",
            "【社会功能受损】出现闭门不出、社交回避或极端的电子产品对抗。已丧失基本的社会参与动力，需警惕社会功能丧失。"
        ]
    }
}

# --- 4. 逻辑控制 ---
if 'st' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 5. 流程渲染 ---
if st.session_state.step == 'home':
    st.markdown("<div class='brand-box'><div class='t1'>家庭教育</div><div class='t2'>十维深度探查表</div><div class='t3'>( 脑科学专业版 )</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='warm-box'>一场跨越心与脑的对话，请放空杂念，给孩子和自己一次被“看见”的机会。</div>", unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'; st.rerun()

elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    
    if cur < 78:
        st.markdown(f"<div class='q-container'><div class='q-text'>{cur+1}. {QUESTIONS_78[cur]}</div></div>", unsafe_allow_html=True)
        opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
        c1, c2 = st.columns(2)
        for i, (txt, val) in enumerate(opts):
            with (c1 if i % 2 == 0 else c2):
                if st.button(txt, key=f"q_{cur}_{i}", use_container_width=True):
                    st.session_state.ans[cur] = val
                    st.session_state.cur += 1
                    st.rerun()
    else:
        q_txt, opts, mode = BG_QS[cur-78]
        st.markdown(f"<div class='q-container'><div class='q-text'>{cur+1}. {q_txt}</div></div>", unsafe_allow_html=True)
        u_val = st.multiselect("多选 (必选)", opts) if mode == "multi" else st.radio("单选 (必选)", opts, index=None)
        if st.button("生成最终报告" if cur == 84 else "下一题", use_container_width=True, disabled=not u_val):
            st.session_state.ans[cur] = u_val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.cur += 1
            st.rerun()
            
    if cur > 0:
        if st.button("⬅️ 返回上一题", type="secondary"):
            st.session_state.cur -= 1; st.rerun()

elif st.session_state.step == 'report':
    # 顶部截屏提醒
    st.markdown("<div class='screenshot-tip'>📸 提示：编号是匹配您测评结果的唯一凭证，请务必截屏保存本页。</div>", unsafe_allow_html=True)
    
    st.markdown("### 📊 深度诊断探查报告")
    
    # 情绪红灯报警 [cite: 66-67]
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='alert-banner'>⚠️ 【最高级别红色警报】监测到孩子存在明显的生存危机或极度情绪创伤（如厌世念头、自伤行为）。此时严禁任何形式的学业施压，必须立刻寻求专业干预，确保生命安全！</div>", unsafe_allow_html=True)
    
    # ADHD/脑特性报警 [cite: 72-77]
    adhd_avg = sum(st.session_state.ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_avg > 1.8:
        st.markdown("<div class='alert-banner' style='background:#FF8F00;'>⚠️ 【脑特性提醒】孩子表现出典型的高多动/冲动或注意力分散特质。建议通过脑科学感统律动而非单纯说教来改善。</div>", unsafe_allow_html=True)

    # 生理基础报警 [cite: 78-83]
    bio_avg = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_avg > 1.5:
        st.markdown("<div class='alert-banner' style='background:#1565C0;'>⚠️ 【底层生理预警】监测到明显的肠脑轴失调或慢性过敏迹象（如黑眼圈、口臭、睡眠异常）。建议先调理身体基础。</div>", unsafe_allow_html=True)

    # 1-6 维度解析
    for dim, info in DIAG_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        level = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        card_cls = "res-card res-high" if level == 2 else "res-card"
        st.markdown(f"<div class='{card_cls}'><b>{dim}：评分显示为【{['稳固/优秀','内耗/预警','危险/力竭'][level]}】</b><br>{info['texts'][level]}</div>", unsafe_allow_html=True)

    # 微信转化
    st.markdown(f"""
        <div class='wx-section'>
            <p style='color:#1B5E20; font-size:18px; font-weight:600;'>
                这份报告揭示了孩子的求救，也看见了您的委屈。<br>其实，您不需要独自扛着。
            </p>
            <div class='promo-list'>
                1. 十个维度个性化改善方案<br>
                2. 30 分钟 1V1 深度解析<br>
                3. 特惠 198 元 (原价 598 元)
            </div>
            <p style='margin-top:15px; font-weight:bold;'>添加微信时请务必备注生成的数字：</p>
            <div class='report-id'>{st.session_state.rid}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.link_button("👉 点击添加老师，预约解析课", "https://work.weixin.qq.com/ca/...", use_container_width=True)
    
    # 底部重复截屏提醒
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。")
