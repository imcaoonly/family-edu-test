import streamlit as st
import random
import plotly.graph_objects as go
import requests    
import json        
from datetime import datetime  

# --- 1. 飞书多维表格 API 模块  ---

APP_ID = "cli_a941cc514b639bcd"          # 你的 App ID
APP_SECRET = "7tjJzFqaSY0fyh2GDNCjPgD12NWYnw4b"  # 你的 App Secret
APP_TOKEN = "UKsvb9YQEajaYTsEjHmcq1CEnqh"   # 多维表格的 Token
TABLE_ID = "tblp77Ua52JtkEaX"            # 数据表的 ID

def get_tenant_access_token():
    """获取飞书 API 访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.json().get("tenant_access_token")
    except:
        return None

def send_to_feishu_bitable(data_dict):
    """将数据写入飞书多维表格 (后台日志增强版)"""
    # 1. 记录开始动作 (在日志里留个脚印，证明程序运行到这了)
    print(f"🚀 [飞书同步] 准备写入记录，用户编号: {data_dict.get('编号', '未知')}")
    
    token = get_tenant_access_token()
    if not token: 
        print("❌ [错误] 无法获取 Tenant Access Token，请检查 App ID 和 Secret")
        return False
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {"fields": data_dict}
    
    try:
        # 设置超时，防止无限等待
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # 2. 检查返回状态码
        if res.status_code == 200:
            print("✅ [成功] 数据已成功写入飞书多维表格")
            return True
        else:
            # --- 关键改动：这里会将飞书返回的具体报错 JSON 打印到日志 ---
            print(f"🔴 [同步失败] 状态码: {res.status_code}")
            print(f"🔴 [详细原因] {res.text}")
            return False
            
    except Exception as e:
        # 3. 记录物理网络异常 (如服务器断网、DNS解析失败)
        print(f"🔥 [严重异常] 网络或代码崩溃: {str(e)}")
        return False

# --- 1. UI 深度定制：首页高度优化版 ---
st.set_page_config(page_title="家庭教育十维深度探查", layout="centered")

st.markdown("""
    <style>
    /* 基础隐藏 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    
    /* 全局背景 */
    .stApp { background: #F8F9FA; color: #455A64; font-family: "PingFang SC", sans-serif; }
    
    /* 首页专用遮盖容器：优化高度与溢出 */
    .home-mask {
        padding: 25px 20px; 
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(26, 35, 126, 0.05);
        border: 1px solid rgba(255,255,255,0.6);
        backdrop-filter: blur(10px);
        margin-top: 10px;
        /* --- 核心修复：去掉 max-height 和 overflow:hidden --- */
        margin-bottom: 20px; /* 增加底部间距，防止贴边 */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* 三行标题：压缩间距 */
    .title-l1 { font-size: 14px; color: #90A4AE; font-weight: 500; margin-bottom: 4px; }
    .title-l2 { font-size: 32px; font-weight: 800; color: #1A237E; line-height: 1.1; margin-bottom: 2px; }
    .title-l3 { font-size: 24px; font-weight: 700; color: #FF7043; margin-bottom: 15px; }
    
    /* 引导语：缩小字号与行高 */
    .intro-text {
        font-size: 16px; color: #546E7A; line-height: 1.6; margin-bottom: 20px;
        border-left: 4px solid #FF7043; padding-left: 15px;
    }
    
/* 1. 基础按钮样式：默认深蓝色 */
    div.stButton > button {
        border-radius: 12px; 
        height: 55px; 
        font-size: 18px !important; 
        font-weight: 700;
        background-color: #1A237E; 
        color: white; 
        border: none;
        transition: all 0.2s;
    }

    /* 2. 悬停状态：颜色稍微变深 */
    div.stButton > button:hover {
        background-color: #0D47A1;
        color: white;
    }

    /* 3. 关键修改：点击后及获得焦点时的状态 */
    /* 这里的 #FF7043 是你品牌色中的橙色，按下后会变成橙色且不再跳回蓝色 */
    div.stButton > button:focus, 
    div.stButton > button:active {
        background-color: #FF7043 !important; 
        color: white !important;
        box-shadow: 0 0 0 0.2rem rgba(255, 112, 67, 0.5) !important;
        outline: none !important;
    }
    
    /* 结果页与其他样式 */
    .q-text { font-size: 20px; font-weight: 600; color: #263238; margin: 25px 0; }
    .warn-banner { padding: 18px; border-radius: 14px; margin-bottom: 15px; color: white; font-weight: 600; }
    .bg-red { background: #C62828; } .bg-orange { background: #E65100; } .bg-blue { background: #0D47A1; }
    .res-card { padding: 18px; border-radius: 12px; background: white; border-left: 6px solid #1A237E; margin-bottom: 12px; }
    .wx-card { background: #FFFFFF; padding: 25px; border-radius: 20px; border: 1px solid #E8EAF6; box-shadow: 0 8px 30px rgba(26,35,126,0.1); text-align: center; }
    .rid-box { font-size: 36px; font-weight: 900; color: #C62828; border: 2px dashed #C62828; padding: 5px 20px; margin: 15px 0; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 状态管理 ---
if 'step' not in st.session_state:
   # 抓取 URL 参数 (?from=xhs 或 ?from=dy)
    query_params = st.query_params
    url_source = query_params.get("from", "直接打开")
    
    # 建立映射表
    source_map = {"xhs": "小红书", "dy": "抖音"}
    final_source = source_map.get(url_source, url_source)
    
    st.session_state.update({
        'step': 'home', 
        'cur': 0, 
        'ans': {},
        'age': 7,  
        'source': final_source,
        'rid': str(random.randint(100000, 999999))
    })
    # --- 3. 全量题库 (1-85题) ---
QUESTIONS = [
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
    "经常“转头就忘”，频繁丢失课本或文具。", "指令“左耳进右耳出”，吼几遍才有反应。", 
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
    "依赖甜食、面食，极度讨厌蔬菜。", "伴有长期口臭、肚子胀气、便秘或大便不成形。", 
    "长期过敏体质（鼻炎、腺样体、湿疹等）。", "进食大量糖、面后，莫名亢奋或情绪崩溃。", 
    "睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "睡眠充足但眼圈常年发青或水肿。", 
    "是否有过确诊？", "为了解决问题，您之前尝试过哪些方式？", 
    "之前尝试的方法没有彻底生效的原因是？", "目前最迫切想解决的前三个痛点是？", 
    "如诊断根源在于“家庭系统及认知”，您是否有勇气参与改变？", 
    "填完后，是否愿预约一次专业“全面分析解读”？", 
    "如果需投入时间扭转局面，您是否有兴趣了解？"
]

# --- 4. 维度话术数据库 (严格匹配文档文案) ---
DIM_DATA = {
    "家庭系统": {
        "range": range(0, 8), 
        "levels": [
            "【稳固】您的家庭地基非常扎实，孩子早期依恋关系很好。这意味着孩子内心的安全感底色是亮的，只要解决表层的功能问题，他好起来会比别人快得多。",
            "【内耗】您的家庭基础整体是稳定的，但内部存在一些“微损耗”（如教育标准不一）。孩子现在像是在顺风和逆风交替的环境下航行，虽然没翻船，但走得很累。",
            "【动荡】家里的“气压”太不稳定了。孩子现在就像在地震带上盖房子，他把所有的能量都用来“维稳”了，根本没有余力去搞学习。"
        ]
    },
    "家长状态": {
        "range": range(8, 18), 
        "levels": [
            "【高能】您的心理建设做得很好。您是孩子最稳的后盾。现在的困局不是您无能，而是您手里缺一把精准的“手术刀”。",
            "【疲劳】您正处于“育儿倦怠”的边缘。您依然在坚持，但这种坚持带有一种强迫性的自我牺牲感。现在的您就像亮起黄灯的仪表盘，提醒您该停下来修整认知模式了。",
            "【力竭】您现在的油箱已经干了。您在用透支自己的方式陪跑，这种焦灼感会通过镜像神经元直接传染给孩子，咱们得先帮您把油加满。"
        ]
    },
    "亲子关系": {
        "range": range(18, 28), 
        "levels": [
            "【顺畅】最宝贵的是，孩子还愿意跟您说真心话。只要情感管道通着，任何技术手段都能 100% 发挥作用。",
            "【疏离】你们之间没有大冲突，但缺乏“深链接”。沟通仅维持在琐事的“事务性交流”上。孩子正在慢慢关上心门，如果您不主动更换频率，他会习惯性心理隔离。",
            "【淤塞】你们之间现在是“信号屏蔽”状态。您说的每一句“为他好”，在他听来都是攻击。不先疏通情感，所有的教育都是无效功。"
        ]
    },
    "动力状态": {
        "range": range(28, 37), 
        "levels": [
            "【自驱】孩子骨子里是有胜负欲和生命力的。他现在的颓废只是“暂时的死机”，只要重装系统，他自己就能跑起来。",
            "【摇摆】孩子的生命力处于“待机状态”。他有想好的愿望，但缺乏持续的推力。这种“推一下动一下”的状态，最容易在压力剧增时彻底熄火。",
            "【空心】孩子已经进入了“节能模式”，对外界失去了探索欲。这是典型的生命力萎缩，我们要通过底层激活，让他重新“活”过来。"
        ]
    },
    "学业管理": {
        "range": range(37, 48), 
        "levels": [
            "【高效】孩子的大脑硬件配置其实很高，执行功能没问题。现在的成绩波动，纯粹是情绪或态度的小感冒，很好修补。",
            "【补偿】孩子目前的学业表现是一种“高代偿”的维持。他在用双倍意志力弥补脑启动效率不足。一旦难度超过极限，会迅速厌学崩盘。",
            "【损耗】这不是态度问题，是“大脑CPU过载”。他写一个字消耗的能量是别人的三倍。咱们得用脑科学的方法帮他降载。"
        ]
    },
    "社会化适应": {
        "range": range(48, 58), 
        "levels": [
            "【合群】孩子的社会化属性很好。这种对集体的归属感，是我们后期把他从手机世界拉回现实的最强抓手。",
            "【依赖】电子世界对他吸引力正在盖过现实。如果现在不干预，他会越来越倾向于在虚拟世界寻找安全感，现实社交能力将持续退化。",
            "【退缩】他在现实世界里找不到成就感，只能去虚拟世界吸氧。学校对他来说不是学习的地方，而是“刑场”，我们要重建他的现实自信。"
        ]
    }
}

def prepare_report_data():
    ans = st.session_state.ans

    # --- 时间修正逻辑：获取北京时间 (UTC+8) ---
    from datetime import timedelta
    # 获取 UTC 时间，然后手动加上 8 小时
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    
  # 辅助：多选列表转文字（统一转为文本，飞书写入最稳）
    def fmt(v): return "、".join(v) if isinstance(v, list) else str(v)

    # 1. 维度均分计算 (严格对应 1-78 题)
    sys_avg = round(sum(ans.get(i,0) for i in range(0, 8)) / 8, 2)
    par_avg = round(sum(ans.get(i,0) for i in range(8, 18)) / 10, 2)
    rel_avg = round(sum(ans.get(i,0) for i in range(18, 28)) / 10, 2)
    pow_avg = round(sum(ans.get(i,0) for i in range(28, 37)) / 9, 2)
    stu_avg = round(sum(ans.get(i,0) for i in range(37, 48)) / 11, 2)
    soc_avg = round(sum(ans.get(i,0) for i in range(48, 58)) / 10, 2)

    # --- 2. 预警逻辑重构 (针对红线题 61, 62 优化) ---
    
    # 【情绪状态预警】 (对应 59-66 题，索引 58-65)
    emo_range = range(58, 66)
    emo_score = sum(ans.get(i, 0) for i in emo_range)
    emo_max = len(emo_range) * 3  # 总分 24
    
    # --- 核心红线拦截 ---
    # 第 61 题索引为 60，第 62 题索引为 61
    negative_worldview = ans.get(60, 0) >= 2  # 消极厌世
    self_harm_intent = ans.get(61, 0) >= 2    # 自伤倾向
    
    # 触发条件：红线触发 OR 任意一题3分 OR 总分超过60%
    if negative_worldview or self_harm_intent:
        emo_risk = "🚨 极高风险 (敏感指标)"
    elif any(ans.get(i, 0) == 3 for i in emo_range) or (emo_score / emo_max > 0.6):
        emo_risk = "🚩 情绪预警"
    else:
        emo_risk = "正常"

    # 【注意状态预警】 (对应 67-72 题，索引 66-71)
    att_range = range(66, 72)
    att_score = sum(ans.get(i, 0) for i in att_range)
    att_max = len(att_range) * 3  # 总分 18
    
    # 触发条件：任意一题3分 OR 总分超过60%
    if any(ans.get(i, 0) == 3 for i in att_range) or (att_score / att_max > 0.6):
        adhd_risk = "🟠 注意受损"
    else:
        adhd_risk = "正常"

    # 【身体状态预警】 (对应 73-78 题，索引 72-77)
    # 触发条件：均分 > 1.5
    body_range = range(72, 78)
    body_scores = [ans.get(i, 0) for i in body_range]
    body_avg = sum(body_scores) / len(body_scores) if body_scores else 0
    
    body_risk = "🔵 生理负荷" if body_avg > 1.5 else "正常"

   # 3. 构造飞书表格字段 (Key 必须与图片表头完全一字不差)
    return {
        "提交日期": beijing_time.strftime("%Y-%m-%d"),
        "提交时间": beijing_time.strftime("%H:%M:%S"),
        "编号": st.session_state.rid,
        "来源渠道": st.session_state.source,
        "年龄": f"{st.session_state.age}岁",
        "确诊情况": fmt(ans.get(78)),
        "试过方法": fmt(ans.get(79)),
        "不生效原因": fmt(ans.get(80)),
        "痛点": fmt(ans.get(81)),
        "改变勇气": fmt(ans.get(82)),
        "预约意愿": fmt(ans.get(83)),
        "了解意愿": fmt(ans.get(84)),
        "各维度均分": f"系统:{sys_avg}, 家长:{par_avg}, 关系:{rel_avg}, 动力:{pow_avg}, 学业:{stu_avg}, 社会:{soc_avg}",
        "情绪预警": emo_risk,
        "注意预警": adhd_risk,
        "身体预警": body_risk,
        "原始凭证": ",".join(str(ans.get(i, "")) for i in range(85))
    }

# --- 5. 页面流程逻辑 ---

# A. 首页：优化后的紧凑版
if st.session_state.step == 'home':
    st.markdown("""
 <div class='home-mask'>
            <div class='title-l1'>曹校长 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是曹校长。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被“看见”的机会。
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'info'
        st.rerun()
# B. 背景信息登记页 (新增部分)
elif st.session_state.step == 'info':
    st.markdown("<h3 style='text-align:center; color:#1A237E; font-weight:900;'>基本资料登记</h3>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<p style='font-size:18px; font-weight:600; color:#263238;'>请选择孩子的周岁年龄：</p>", unsafe_allow_html=True)
    
    # 1. 使用一个独立的 key（例如 "slider_val"）来承接滑块的即时动作
    # 2. 将滑块的返回值直接赋给变量 age_picked
    age_picked = st.slider(
        label="", 
        min_value=1, 
        max_value=25, 
        value=st.session_state.age, 
        key="slider_val", 
        help="请滑动选择孩子目前的周岁年龄"
    )
    
    # 实时显示选中的年龄，确保用户能看到变化
    st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:bold; color:#FF7043; margin:20px 0;'>{age_picked} 周岁</div>", unsafe_allow_html=True)
    
    st.info("💡 提示：年龄信息将帮助系统自动匹配相应发育阶段的脑科学解析模型。")
    
    st.write("")
    
    # 3. 关键点：在点击确认按钮时，强制执行覆盖操作
    if st.button("确认并开始答题 🚀", use_container_width=True):
        st.session_state.age = age_picked  # 这一行是物理覆盖，确保 7 被替换掉
        st.session_state.step = 'quiz'
        st.rerun()

# C. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur

    # 1. 定义动态文案字典 (建议放在这，或者放在代码最顶部的配置区)
    LOGIC_MAP = {
        0:  "🔍 正在开始家庭根基扫描...", 
        8:  "⚡ 正在评估家长能量状态...", 
        18: "🔗 正在剖析亲子链接密度...", 
        28: "🚀 正在触达底层动力核心...", 
        37: "📚 正在测算学习功能损耗...", 
        48: "🤝 正在评估社会化适应能力...", 
        58: "🌊 正在监测情绪安全水平...", 
        66: "🧠 正在解析大脑注意模型...", 
        72: "🍎 正在追溯生理代谢底层...", 
        78: "🎯 正在匹配深入解析方向..."
    }

    # 2. 匹配当前文案
    current_status = "📝 正在录入测评数据..."
    for start_idx in sorted(LOGIC_MAP.keys(), reverse=True):
        if cur >= start_idx:
            current_status = LOGIC_MAP[start_idx]
            break

    # 3. 渲染美化后的动态进度条区域
    col_status, col_pct = st.columns([3, 1])
    with col_status:
        st.markdown(f"""
            <div style='font-size: 14px; color: #1A237E; font-weight: 600; margin-bottom: -5px;'>
                {current_status}
            </div>
        """, unsafe_allow_html=True)
    with col_pct:
        st.markdown(f"""
            <div style='font-size: 12px; color: #90A4AE; text-align: right; margin-bottom: -5px;'>
                已分析 {round((cur + 1) / 85 * 100)}%
            </div>
        """, unsafe_allow_html=True)

    st.progress((cur + 1) / 85)

    # 4. 显示题目文本 (保持你原有的 q-text 样式)
    q_text = QUESTIONS[cur]
    st.markdown(f"<div class='q-text'>{cur+1}. {q_text}</div>", unsafe_allow_html=True)

    # --- 以下保持你原有的按钮逻辑不变 ---
    if cur < 78:
        opts = [("0 (从不)", 0), ("2 (经常)", 2), ("1 (偶尔)", 1), ("3 (总是)", 3)]
        cols = st.columns(2)
        for i, (txt, val) in enumerate(opts):
            with (cols[0] if i % 2 == 0 else cols[1]):
                if st.button(txt, key=f"q_{cur}_{i}", use_container_width=True):
                    st.session_state.ans[cur] = val
                    if cur not in st.session_state.ans:
                        st.error("⚠️ 上一题未记录，请点击“上一题”重新作答。")
                    else:
                        st.session_state.cur += 1
                        st.rerun()

   # --- 逻辑分水岭：79-85题 为背景/意愿题 ---
    else:
        # 使用动态 Key 确保每一题的状态是独立的
        input_key = f"input_step_{cur}"
        
        if cur == 78: # 79题
            user_input = st.multiselect("可多选", ["ADHD", "抑郁/焦虑", "其他", "暂无"], key=input_key)
        elif cur == 79: # 80题
            user_input = st.multiselect("可多选", ["心理咨询", "药物治疗", "增加严管", "上父母课", "其他"], key=input_key)
        elif cur == 80: # 81题
            user_input = st.multiselect("可多选", ["不落地", "不系统", "没法坚持", "孩子不配合", "缺乏专业陪跑"], key=input_key)
        elif cur == 81: # 82题
            user_input = st.multiselect("请勾选（建议不超过3个）", ["关系", "厌学", "专注力差", "情绪较大", "手机"], key=input_key)
        elif cur == 82: # 83题
            user_input = st.radio("请选择", ["有", "有，但需指导", "比较纠结", "只想改孩子"], key=input_key)
        elif cur == 83: # 84题
            user_input = st.radio("请选择", ["是", "否"], key=input_key)
        elif cur == 84: # 85题
            user_input = st.radio("请选择", ["是", "否"], key=input_key)

        btn_label = "生成报告 📊" if cur == 84 else "确认，下一题 ➡️"
        
        st.write("")
        
        # 修复触发逻辑：确保点击时能保存当前答案
        if st.button(btn_label, use_container_width=True):
            if not user_input:
                st.warning("⚠️ 请选择后再继续。")
            else:
                # 显式保存到 session_state
                st.session_state.ans[cur] = user_input
                
                if cur == 84: # 第 85 题提交 
                    # 这里增加转圈等待提示 
                    with st.spinner('正在为您生成解析报告，请稍候...'):
                        try:
                            report_payload = prepare_report_data()
                            send_to_feishu_bitable(report_payload)
                        except:
                            st.warning("💡数据同步略有延迟，请截屏保存结果。")
                        
                        st.session_state.step = 'report'
                        st.rerun()
                else:
                    # 正常跳转到下一题
                    st.session_state.cur += 1
                    st.rerun()

            
    # 底部导航
    if cur > 0:
        st.write("")
        if st.button("⬅ 上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# D. 结果报告页逻辑
elif st.session_state.step == 'report':
    # --- 标题部分 ---
    st.markdown("<h2 style='text-align:center; color:#000000; font-weight:900; margin-bottom:8px;'>多维报告解析</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:12px; border-radius:10px; text-align:center; margin-bottom:20px; font-size:14px;'>📸 请【截屏保存】本页结果，作为咨询凭证。</div>", unsafe_allow_html=True)
    
    # 1. 风险预警模块（暖橙色卡片提示）
    st.markdown("<p style='color:#E65100; font-weight:bold; margin-bottom:10px;'>核心风险筛查：</p>", unsafe_allow_html=True)
    
    # 7. 情绪状态预警 (59-66题)
    emo_scores = [st.session_state.ans.get(i, 0) for i in range(58, 66)]
    if any(s == 3 for s in emo_scores) or (sum(emo_scores) >= 24 * 0.6) or any(st.session_state.ans.get(i, 0) >= 2 for i in [64, 65]): # 假设65/66为消极倾向题
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【情绪状态预警】当前孩子情绪安全水位极低，沉默是他在呼救。首要任务不是抓学习，而是“稳情绪”，必须立刻切入心理安全干预。</div>", unsafe_allow_html=True)
    
    # 8. 注意状态预警 (67-72题)
    adhd_scores = [st.session_state.ans.get(i, 0) for i in range(66, 72)]
    if any(s == 3 for s in adhd_scores) or (sum(adhd_scores) >= 18 * 0.6):
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【注意状态预警】疑似 ADHD 特质。孩子大脑天生自带“降噪功能缺陷”，不要再骂他粗心了，他需要专业的脑功能整合训练。</div>", unsafe_allow_html=True)

    # 9. 身体状态预警 (73-78题)
    body_avg = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if body_avg > 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【身体状态预警】当前表现受生理代谢（如营养、过敏）影响。生理基础不稳，心智无法成长，建议从营养与节律层面修复。</div>", unsafe_allow_html=True)

    # 2. 雷达图绘制
    scores, labels = [], list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1)) # 转化为100分制展示
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(t=20, b=20, l=40, r=40))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<p style='font-size:12px; color:#90A4AE; text-align:center;'>注：分值越高，代表该维度的“负荷”或“风险”越大。</p>", unsafe_allow_html=True)

    # 3. 六大维度深度解析卡片 (匹配 0.8/1.8/3.0 分层逻辑)
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        # 匹配分值：0-0.8 优秀(绿/蓝), 0.9-1.8 预警(黄), 1.9-3.0 危险(红)
        if avg <= 0.8:
            color, idx = "#2E7D32", 0 # 稳固
        elif avg <= 1.8:
            color, idx = "#F9A825", 1 # 中位
        else:
            color, idx = "#C62828", 2 # 高分危险
            
        st.markdown(f"""
            <div style='padding:18px; border-radius:12px; background:white; border-left:6px solid {color}; margin-bottom:12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                <b style='color:{color};'>{dim}</b><br>
                <span style='color:#455A64; font-size:15px;'>{info['levels'][idx]}</span>
            </div>
        """, unsafe_allow_html=True)

    # 微信转化区域
    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#1A237E; font-size:18px; font-weight:bold;'>
                这份报告揭示了孩子的求救，<br>
                也看见了您的委屈。<br>
                <span style='color:#FF7043;'>其实，您不需要独自扛着。</span>
            </p>
            <div style='text-align:left; margin-top:15px;'>
            <p style='margin:10px 0 5px 0; font-weight:bold; color:#455A64;'>添加微信您可以获得：</p>
                <p style='margin:5px 0;'>✅ 10个维度<span style='color:#FF7043; font-weight:bold;'>个性化</span> 改善方案</p>
                <p style='margin:5px 0;'>✅ 30分钟 <span style='color:#FF7043; font-weight:bold;'>1V1</span> 深度解析</p>
                <p style='margin:5px 0;'>✅ <span style='color:#FF7043; font-weight:bold;'>特惠 198 元</span>（原价 598 元）</p>
            </div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <p style='color:#546E7A; font-size:13px;'>添加微信请备注上方数字编号</p>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:15px; border-radius:12px; font-size:18px; font-weight:bold; margin-top:10px;">👉 点击添加预约曹校深度解析</a>
        </div>
    """, unsafe_allow_html=True)
    # --- 就在这里添加！注意缩进要和上面的 st.markdown 对齐 ---
    st.write("") 
    if st.button("🔄 新开始测评", use_container_width=True):
        st.session_state.clear() # 清空所有答案和状态
        st.rerun() # 强制回到首页重新开始
