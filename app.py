import streamlit as st
import random

# --- 1. 全局样式定制 (解决移动端点击感 & 视觉对齐) ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* 品牌区 */
    .brand-box { text-align: center; margin-bottom: 30px; }
    .t1 { font-size: 34px; font-weight: 800; color: #1B5E20; }
    .t2 { font-size: 28px; font-weight: 700; color: #2E7D32; }
    
    /* 题目左对齐 & 深灰蓝 */
    .q-container { text-align: left !important; margin: 25px 0; }
    .q-text { font-size: 20px; font-weight: 600; color: #455A64; line-height: 1.6; }
    
    /* 提高按钮点击灵敏度 */
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 55px; font-size: 18px !important;
        border: 1px solid #E0E0E0; background-color: #FAFAFA; transition: all 0.2s;
    }
    div.stButton > button:active { transform: scale(0.98); background-color: #E8F5E9; }

    /* 报告页结果卡片 */
    .res-card { padding: 20px; border-radius: 15px; background: #FFF; border-left: 8px solid #E0E0E0; margin-bottom: 15px; text-align: left; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .res-danger { border-left-color: #D32F2F !important; background-color: #FFF5F5; }
    
    /* 红色警报区 */
    .alert-box { background: #D32F2F; color: white; padding: 15px; border-radius: 12px; font-weight: bold; margin-bottom: 20px; }
    
    /* 转化区专属编号 */
    .id-box { font-size: 36px; font-weight: 900; color: #D32F2F; background: #FFF; padding: 10px 25px; border-radius: 12px; border: 3px dashed #D32F2F; display: inline-block; margin: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心题库录入 (1-85题) ---
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
    ("有过确诊？", ["ADHD", "抑郁/焦虑", "其他", "暂无"], "multi"),
    ("尝试过的方式？", ["咨询", "药物", "严管", "父母课", "其他"], "multi"),
    ("未生效的原因？", ["不落地", "不系统", "难坚持", "不配合", "缺陪跑"], "multi"),
    ("迫切的痛点？", ["关系", "厌学", "专注力", "情绪", "手机"], "multi"),
    ("是否有勇气改变？", ["有", "需指导", "纠结", "只想改孩子"], "single"),
    ("是否愿预约解读？", ["是", "否"], "single"),
    ("是否愿了解方案？", ["是", "否"], "single")
]

# --- 3. 补全三级诊断话术 (全量录入) ---
DIAG_DATA = {
    "系统维度": {"range": range(0, 8), "texts": ["【稳固】地基牢固，依恋安全。", "【内耗】地基有裂缝，承压接近临界。", "【动荡】地基动摇，缺乏基本安全感。"]},
    "家长维度": {"range": range(8, 18), "texts": ["【充沛】能量强，自控力优。", "【预警】能量内耗，焦虑渗透。", "【力竭】心理崩溃边缘，引导力丧失。"]},
    "关系维度": {"range": range(18, 28), "texts": ["【信任】沟通畅通，边界清晰。", "【防御】情感阻塞，仅维持功能沟通。", "【断联】逃离倾向明显，处于冷战对抗。"]},
    "动力维度": {"range": range(28, 37), "texts": ["【旺盛】生机勃勃，抗挫力强。", "【下行】开始畏难，出现空心化苗头。", "【枯竭】极度冷感，自我价值感降至冰点。"]},
    "学业维度": {"range": range(37, 48), "texts": ["【高效】脑功能处于高效区。", "【疲劳】生理性磨蹭，执行功能受损。", "【宕机】大脑保护性关闭，抗拒任务。"]},
    "社会化": {"range": range(48, 58), "texts": ["【自如】社交正常，规则意识强。", "【退缩】依赖屏幕，社交半径缩窄。", "【受损】社会功能丧失，回避现实生活。"]}
}

# --- 4. 流程逻辑 ---
if 'step' not in st.session_state:
    st.session_state.update({'step': 'home', 'cur': 0, 'ans': {}, 'rid': str(random.randint(100000, 999999))})

# --- 5. 界面呈现 ---
if st.session_state.step == 'home':
    st.markdown("<div class='brand-box'><div class='t1'>家庭教育</div><div class='t2'>十维深度探查表</div></div>", unsafe_allow_html=True)
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
                # 核心修复：为每个按钮分配唯一 Key，解决点击失效
                if st.button(txt, key=f"btn_{cur}_{i}", use_container_width=True):
                    st.session_state.ans[cur] = val
                    st.session_state.cur += 1
                    st.rerun()
    else:
        q_txt, opts, mode = BG_QS[cur-78]
        st.markdown(f"<div class='q-container'><div class='q-text'>{cur+1}. {q_txt}</div></div>", unsafe_allow_html=True)
        u_val = st.multiselect("多选", opts, key=f"ms_{cur}") if mode == "multi" else st.radio("单选", opts, index=None, key=f"rd_{cur}")
        if st.button("生成最终报告" if cur == 84 else "下一题", key=f"next_{cur}", use_container_width=True, disabled=not u_val):
            st.session_state.ans[cur] = u_val
            if cur == 84: st.session_state.step = 'report'
            else: st.session_state.cur += 1
            st.rerun()

elif st.session_state.step == 'report':
    # 顶部截屏提醒
    st.markdown("""<div style='background:#FFEBEE; border:2px solid #D32F2F; padding:15px; border-radius:12px; text-align:center; margin-bottom:20px;'>
        <p style='color:#D32F2F; font-size:18px; font-weight:bold; margin:0;'>📸 请务必【截屏保存】本页结果！</p></div>""", unsafe_allow_html=True)
    
    # 1-9 维度解析 (报警与话术)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='alert-box'>⚠️ 红色警报：监测到生存危机倾向，请立即停止施压并寻求专业干预！</div>", unsafe_allow_html=True)
    
    for dim, info in DIAG_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        level = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card {'res-danger' if level==2 else ''}'><b>{dim}：{['稳固','预警','危险'][level]}</b><br>{info['texts'][level]}</div>", unsafe_allow_html=True)

    # 微信转化区 (原生 HTML 解决点击无效)
    st.markdown(f"""
        <div style='background:#E8F5E9; padding:30px; border-radius:20px; text-align:center; border:1px solid #C8E6C9;'>
            <p style='color:#1B5E20; font-size:18px; font-weight:600;'>一份报告揭示了孩子的求救，您不需要独自扛着。</p>
            <div style='text-align:left; display:inline-block; font-size:17px; line-height:2; color:#1B5E20;'>
                1. 十个维度改善方案 | 2. 30分钟1V1解析 | 3. 特惠198元
            </div><br>
            <p style='margin-top:15px; font-weight:bold;'>添加微信请备注编号：</p>
            <div class='id-box'>{st.session_state.rid}</div>
            
            <a href="https://work.weixin.qq.com/ca/你的真实链接" target="_blank" style="text-decoration:none;">
                <div style="background:#2E7D32; color:white; padding:18px; border-radius:12px; font-size:20px; font-weight:bold; margin-top:10px;">👉 点击添加老师微信</div>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。")
