import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

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
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心题库录入 (1-85 题全量) ---
# 此处已预留位置，请将之前完整的 QUESTIONS_78 和 BG_QS 列表粘贴于此
if 'QUESTIONS_78' not in locals():
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
                你好，我是你的老朋友。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'; st.rerun()

# B. 答题页：Key 值唯一化防止报错
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    
    if cur < 78:
        st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS_78[cur]}</div>", unsafe_allow_html=True)
        opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
        c1, c2 = st.columns(2)
        for i, (txt, val) in enumerate(opts):
            with (c1 if i % 2 == 0 else c2):
                # 使用全局唯一 Key：题目索引 + 选项索引
                if st.button(txt, key=f"btn_q_{cur}_{i}", use_container_width=True):
                    st.session_state.ans[cur] = val
                    st.session_state.cur += 1
                    st.rerun()
    # 背景题逻辑 (略，请参照之前版本)

# C. 结果页：雷达图 + 原版三大报警话术
elif st.session_state.step == 'report':
    # 顶部截屏提醒
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。</div>", unsafe_allow_html=True)
    
    # [Plotly 雷达图代码：颜色改为深蓝 #1A237E]
    
    # --- 三大维度原版话术还原 ---
    
    # 1. 情绪红灯 (59-66题)
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("""<div class='warning-banner bg-red'>
            ⚠️ 【最高级别红色警报】<br>
            监测到孩子目前存在明显的生存危机或极度情绪创伤（如厌世念头、自伤、极度冷漠）。<br>
            此时任何关于学习的督促都是在“火上浇油”。请务必立刻停止施压，寻求专业心理干预，确保生命安全是当前家庭的第一要务！
        </div>""", unsafe_allow_html=True)

    # 2. ADHD 脑特性 (67-72题)
    adhd_score = sum(st.session_state.ans.get(i, 0) for i in range(66, 72)) / 6
    if adhd_score >= 1.5:
        st.markdown("""<div class='warning-banner bg-orange'>
            ⚠️ 【脑特性深度预警】<br>
            孩子表现出典型的高多动、冲动或注意力黑洞特质。这并非“态度不端正”，而是前额叶皮质执行功能发育的暂时性滞后。<br>
            单纯的说教和惩罚只会破坏自尊，建议采用脑科学感统律动结合的行为管理方案进行“弯道超车”。
        </div>""", unsafe_allow_html=True)

    # 3. 底层生理基础 (73-78题)
    bio_score = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if bio_score >= 1.5:
        st.markdown("""<div class='warning-banner bg-blue'>
            ⚠️ 【底层生理地基预警】<br>
            监测到孩子伴有明显的肠脑轴失调或慢性生理压力迹象（如长期过敏、睡眠呼吸障碍、眼圈发青、情绪易炸）。<br>
            当身体处于慢性炎症或缺氧状态时，大脑会自动切换到“生存模式”而非“学习模式”。建议先进行生理节律的系统调理。
        </div>""", unsafe_allow_html=True)

    # --- 转化区 ---
    st.markdown(f"""
        <div style='background:#E8EAF6; padding:35px; border-radius:24px; text-align:center; border:1px solid #C5CAE9; margin-top:40px;'>
            <p style='color:#1A237E; font-size:18px; font-weight:600;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div class='report-id'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:22px; font-weight:bold; box-shadow: 0 6px 15px rgba(26,35,126,0.2);">👉 点击添加老师，预约 1V1 解析</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("提示：编号是匹配您测评结果的唯一凭证，请截屏保存本页。")
