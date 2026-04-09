import streamlit as st
import random
import plotly.graph_objects as go
import requests    
import json        
from datetime import datetime
import pytz  

# --- 1. 飞书多维表格 API 模块 (安全优化版) ---

# 从 Streamlit 的"保险柜"(Secrets) 中直接读取，不再把明文写在代码里
APP_ID = st.secrets["APP_ID"]
APP_SECRET = st.secrets["APP_SECRET"]
APP_TOKEN = st.secrets["APP_TOKEN"]
TABLE_ID = st.secrets["TABLE_ID"]

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
    """将数据写入飞书多维表格 (纯净版：只在后台报错)"""
    # 1. 后台记录日志（用户在网页上看不见这些）
    print(f"🚀 [飞书同步] 准备写入记录，用户编号: {data_dict.get('编号', '未知')}")
    
    token = get_tenant_access_token()
    if not token: 
        print("❌ [错误] 无法获取 Tenant Access Token")
        return False
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {"fields": data_dict}
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # 2. 检查返回结果
        if res.status_code == 200 and res_json.get("code") == 0:
            print("✅ [成功] 数据已成功写入飞书多维表格")
            return True
            
        else:
            print(f"🔴 [同步失败] HTTP状态: {res.status_code}, 飞书Code: {res_json.get('code')}, 原因: {res_json.get('msg')}")
            return False 
            
    except Exception as e:
        print(f"🔥 [严重异常] 网络故障: {str(e)}")
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

/* 3. 关键修改：只在鼠标/手指按住（激活）的瞬间变橙色 */
div.stButton > button:active {
    background-color: #FF7043 !important; 
    color: white !important;
    box-shadow: 0 0 0 0.2rem rgba(255, 112, 67, 0.5) !important;
}

/* 4. 焦点状态：恢复为深蓝色（避免点完后一直橙色） */
div.stButton > button:focus {
    background-color: #1A237E !important; 
    color: white !important;
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

# --- 3. 全量题库 (1-85题) ---
QUESTIONS = [
    "孩子3岁前，主要抚养人频繁更换或长期中断。", "孩子早期曾连续2周以上见不到核心抚养人。", 
    "长辈深度参与管教，经常推翻您的决定。", "父母教育标准不一，经常\"一宽一严\"。", 
    "孩子幼年受委屈时极度粘人，无法离开抚养人。", "家里近两年经历搬家、转学或财务大变动。", 
    "您处理人际关系（如婆媳、夫妻矛盾）心力交瘁。", "您的家人虽同住但各忙各的，缺乏交心时刻。", 
    "您面对孩子问题，感到深深的无力感。", "您觉得若不是为了孩子，生活会更精彩自由。", 
    "您发火吼叫后会陷入\"后悔自责—过度补偿\"循环。", "您觉得孩子某些性格与您讨厌的特质一模一样。", 
    "您极度在意老师或他人对孩子的负面评价。", "您将孩子表现与个人价值感挂钩，他不出色您感到挫败。", 
    "您管教孩子时心跳加快、胸闷、手抖或大脑空白。", "您觉得带孩子是孤军奋战，配偶无实质支持。", 
    "您睡眠质量差，入睡困难或报复性熬夜。", "您内心焦虑、烦躁，很难获得平静。", 
    "您和孩子除了聊学习吃睡，很难进行开心闲聊。", "孩子在校受委屈或丢脸会选择隐瞒，不告知您。", 
    "孩子对您进房间或动用其物品有明显反感。", "孩子经常反锁屋门，抗拒您询问或靠近。", 
    "孩子情绪爆发时，您本能想靠讲道理或强行压制。", "孩子犯错后第一反应是撒谎、推诿或冷战。", 
    "您会翻看手机或日记来了解其真实想法。", "孩子不敢在您面前表达真实不满、愤怒或意见。", 
    "孩子抱怨在家里没自由，或想要早点离家。", "孩子对您的沟通有明显防御性，您一开口他就烦。", 
    "孩子面对挑战，还没做就觉得肯定不行，想退缩。", "游戏输了或遇难题，孩子会立刻情绪崩塌或放弃。", 
    "孩子过度在意评价，因别人一句话就郁郁寡欢。", "孩子对学习以外的事物也兴致索然，没爱好。", 
    "孩子经常说没意思、没劲，感到空虚。", "孩子对自己要求极高且不容许失败，稍不如意就否定自己。", 
    "您觉得孩子的生命力在萎缩，越来越像一个\"空心人\"。", "孩子即使做感兴趣的事，也难以保持长久热情。", 
    "孩子近期对以前喜欢的活动表现出明显冷感。", "孩子磨蹭拖延，通过各种准备动作逃避开始作业。", 
    "孩子写作业时神游发呆 or 手脚小动作不停。", "孩子写字姿势扭曲、力道极重，容易疲劳。", 
    "孩子经常\"转头就忘\"，频繁丢失课本或文具。", "孩子对指令\"左耳进右耳出\"，您吼几遍才有反应。", 
    "孩子阅读或抄写频繁跳行、漏字或笔画写反。", "孩子面对复杂任务，完全不知道从哪下手。", 
    "孩子启动效率极低，反应速度明显慢于同龄人。", "孩子坐姿东倒西歪，写作业时头低得非常近。", 
    "孩子处理多步骤指令时，中途断掉就直接放弃。", "孩子无法控制地咬指甲、咬衣领或笔头。", 
    "电子屏幕占据了孩子除学习外的绝大部分时间。", "收手机时，孩子出现剧烈情绪爆发或肢体对抗。", 
    "孩子为了玩手机经常撒谎，或熬夜偷玩。", "提到上学或考试，孩子有头痛腹痛等生理反应。", 
    "孩子拒绝社交，有明显的社交回避或社恐。", "老师反馈孩子纪律性差、孤僻或难以融入集体。", 
    "孩子在学校没有可以倾诉、互助支持的朋友。", "孩子对校园规则极度不耐受，有明显逆反心。", 
    "孩子在公共场合表现出局促感或不合时宜行为。", "电子产品是爆发家庭冲突的最主要诱因。", 
    "孩子近期长时间不洗头不换衣，不在意个人卫生。", "孩子的食欲极端波动（暴食或长期厌食）。", 
    "孩子表达过消极厌世或\"我消失了更好\"的念头。", "孩子身上有不明划痕，或拔头发、啃指甲见血。", 
    "孩子对未来不抱期待，拒绝讨论任何计划。", "孩子睡眠节律彻底混乱，黑白颠倒。", 
    "孩子对最亲近的人也表现出极度冷漠和隔绝。", "提到学校或老师，孩子会浑身发抖或剧烈抵触。", 
    "孩子玩游戏专注，面对学习坐不住、易走神。", "安静环境下，孩子也无法停止身体扭动或晃动。", 
    "孩子无法耐心等别人说完，经常抢话、插话。", "在排队或等待场合，孩子表现出超越年龄的焦躁。", 
    "孩子短时记忆黑洞，刚交代的事转头就忘。", "孩子在做作业或听讲时，极易被微小动静吸引。", 
    "孩子依赖甜食、面食，极度讨厌蔬菜。", "孩子伴有长期口臭、肚子胀气、便秘或大便不成形。", 
    "孩子有长期过敏体质（鼻炎、腺样体、湿疹等）。", "孩子进食大量糖、面后，莫名亢奋或情绪崩溃。", 
    "孩子睡觉张口呼吸、盗汗、磨牙或频繁翻身。", "孩子睡眠充足，但眼圈常年发青或水肿。", 
    "孩子是否有过确诊？（多选）", "为了解决问题，您之前尝试过哪些方式？（多选）", 
    "您之前尝试的方法没有彻底生效的原因是？（多选）", "您目前最迫切想解决的前三个痛点是？（多选）", 
    "如诊断根源在于\"家庭系统及认知\"，您是否有勇气参与改变？（单选）", 
    "填完后，您是否愿预约一次专业\"全面分析解读\"？（单选）", 
    "如果需投入时间扭转局面，您是否有兴趣了解？（单选）"
]

# --- 1.2 拦截与参数处理逻辑 (解决乱码与双链接实现) ---
query_params = st.query_params

# 情况 A：从飞书点击"答题链接" (?page=detail)
if query_params.get("page") == "detail":
    target_id = query_params.get("rid", "未知")
    st.title(f"📋 原始答题详情回顾")
    st.info(f"用户编号: {target_id}")
    
    raw_data = query_params.get("data", "")
    if raw_data:
        ans_list = raw_data.split(",")
        for i, val in enumerate(ans_list):
            if i < 78:
                q_text = QUESTIONS[i] if i < len(QUESTIONS) else f"第 {i+1} 题"
                st.write(f"**{q_text}**")
                score_map = {0: "从不", 1: "偶尔", 2: "经常", 3: "总是"}
                try:
                    score_val = int(val)
                    st.write(f"回答：{score_map.get(score_val, val)} ({val}分)")
                except:
                    st.write(f"回答：{val}")
            else:
                # 背景信息题
                q_text = QUESTIONS[i] if i < len(QUESTIONS) else f"附加信息 {i+1}"
                st.write(f"**{q_text}**")
                st.write(f"回答：{val}")
            st.divider()

# 情况 B：点开的是【报告链接】 (?data=...)
elif "data" in query_params:
    # 只有当 session_state 中没有 ans 或者 ans 为空时才解析
    if 'ans' not in st.session_state or not st.session_state.ans:
        st.session_state.ans = {}
        
    # 还原数据用于渲染精美报告
    raw_data = query_params["data"]
    ans_list = raw_data.split(",")
    for i, val in enumerate(ans_list):
        if val.isdigit():
            st.session_state.ans[i] = int(val)
        else:
            st.session_state.ans[i] = val
            
    # 设置报告状态
    st.session_state.rid = query_params.get("rid", "未知")
    st.session_state.step = 'report'
    st.rerun()

# --- 拦截逻辑结束 ---

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


# --- 4. 维度话术数据库 (严格匹配文档文案) ---
DIM_DATA = {
    "家庭系统": {
        "range": range(0, 8), 
        "levels": [
            "【稳固】您的家庭地基非常扎实，孩子早期依恋关系很好。这意味着孩子内心的安全感底色是亮的，只要解决表层的功能问题，他好起来会比别人快得多。",
            "【内耗】您的家庭基础整体是稳定的，但内部存在一些\"微损耗\"（如教育标准不一）。孩子现在像是在顺风和逆风交替的环境下航行，虽然没翻船，但走得很累。",
            "【动荡】家里的\"气压\"太不稳定了。孩子现在就像在地震带上盖房子，他把所有的能量都用来\"维稳\"了，根本没有余力去搞学习。"
        ]
    },
    "家长状态": {
        "range": range(8, 18), 
        "levels": [
            "【高能】您的心理建设做得很好。您是孩子最稳的后盾。现在的困局不是您无能，而是您手里缺一把精准的\"手术刀\"。",
            "【疲劳】您正处于\"育儿倦怠\"的边缘。您依然在坚持，但这种坚持带有一种强迫性的自我牺牲感。现在的您就像亮起黄灯的仪表盘，提醒您该停下来修整认知模式了。",
            "【力竭】您现在的油箱已经干了。您在用透支自己的方式陪跑，这种焦灼感会通过镜像神经元直接传染给孩子，咱们得先帮您把油加满。"
        ]
    },
    "亲子关系": {
        "range": range(18, 28), 
        "levels": [
            "【顺畅】最宝贵的是，孩子还愿意跟您说真心话。只要情感管道通着，任何技术手段都能 100% 发挥作用。",
            "【疏离】你们之间没有大冲突，但缺乏\"深链接\"。沟通仅维持在琐事的\"事务性交流\"上。孩子正在慢慢关上心门，如果您不主动更换频率，他会习惯性心理隔离。",
            "【淤塞】你们之间现在是\"信号屏蔽\"状态。您说的每一句\"为他好\"，在他听来都是攻击。不先疏通情感，所有的教育都是无效功。"
        ]
    },
    "动力状态": {
        "range": range(28, 37), 
        "levels": [
            "【自驱】孩子骨子里是有胜负欲和生命力的。他现在的颓废只是\"暂时的死机\"，只要重装系统，他自己就能跑起来。",
            "【摇摆】孩子的生命力处于\"待机状态\"。他有想好的愿望，但缺乏持续的推力。这种\"推一下动一下\"的状态，最容易在压力剧增时彻底熄火。",
            "【空心】孩子已经进入了\"节能模式\"，对外界失去了探索欲。这是典型的生命力萎缩，我们要通过底层激活，让他重新\"活\"过来。"
        ]
    },
    "学业管理": {
        "range": range(37, 48), 
        "levels": [
            "【高效】孩子的大脑硬件配置其实很高，执行功能没问题。现在的成绩波动，纯粹是情绪或态度的小感冒，很好修补。",
            "【补偿】孩子目前的学业表现是一种\"高代偿\"的维持。他在用双倍意志力弥补脑启动效率不足。一旦难度超过极限，会迅速厌学崩盘。",
            "【损耗】这不是态度问题，是\"大脑CPU过载\"。他写一个字消耗的能量是别人的三倍。咱们得用脑科学的方法帮他降载。"
        ]
    },
    "社会化适应": {
        "range": range(48, 58), 
        "levels": [
            "【合群】孩子的社会化属性很好。这种对集体的归属感，是我们后期把他从手机世界拉回现实的最强抓手。",
            "【依赖】电子世界对他吸引力正在盖过现实。如果现在不干预，他会越来越倾向于在虚拟世界寻找安全感，现实社交能力将持续退化。",
            "【退缩】他在现实世界里找不到成就感，只能去虚拟世界吸氧。学校对他来说不是学习的地方，而是\"刑场\"，我们要重建他的现实自信。"
        ]
    }
}

def prepare_report_data():
    ans = st.session_state.ans
    rid = st.session_state.rid
    
    # --- 1. 时间修正逻辑 ---
    tz = pytz.timezone('Asia/Shanghai')
    beijing_time = datetime.now(tz)

    # 定义格式化函数（处理列表转字符串）
    def fmt(v):  return  "、".join(v) if  isinstance(v, list) else  str(v)
    
    # --- 2. 构造两个纯链接 --- 
    # 【注意】：请确保此域名是你 Streamlit 部署后的最新实际网址
    base_url = "https://family-edu-test-sqjqmdetjfhtbvpsh44xng.streamlit.app"
    raw_data_str = ",".join(str(ans.get(i, "")) for i in range(85))
    
    # 将原本的 detail_link 改为 report_link，作为客户看到的报告页
    report_link = f"{base_url}/?rid={rid}&data={raw_data_str}"

    # 将原本多余的 detail_url 改名为 detail_link，作为后台详情页
    detail_link = f"{base_url}/?page=detail&rid={rid}&data={raw_data_str}"

    # 3. 维度均分计算 (严格对应 1-78 题)
    sys_avg = round(sum(int(ans.get(i, 0) or 0) for i in range(0, 8)) / 8, 2)
    par_avg = round(sum(int(ans.get(i, 0) or 0) for i in range(8, 18)) / 10, 2)
    rel_avg = round(sum(int(ans.get(i, 0) or 0) for i in range(18, 28)) / 10, 2)
    pow_avg = round(sum(int(ans.get(i, 0) or 0) for i in range(28, 37)) / 9, 2)
    stu_avg = round(sum(int(ans.get(i, 0) or 0) for i in range(37, 48)) / 11, 2)
    soc_avg = round(sum(int(ans.get(i, 0) or 0) for i in range(48, 58)) / 10, 2)

    # --- 4. 预警逻辑重构 (针对红线题 61, 62 优化) ---
    
    # 【情绪状态预警】 (对应 59-66 题，索引 58-65)
    emo_range = range(58, 66)
    emo_score = sum(int(ans.get(i, 0) or 0) for i in emo_range)
    emo_max = len(emo_range) * 3  # 总分 24
    
    # --- 核心红线拦截 ---
    # 第 61 题索引为 60，第 62 题索引为 61
    negative_worldview = int(ans.get(60, 0) or 0) >= 2  # 消极厌世
    self_harm_intent = int(ans.get(61, 0) or 0) >= 2    # 自伤倾向
    
    # 触发条件：红线触发 OR 任意一题3分 OR 总分超过60%
    if negative_worldview or self_harm_intent:
        emo_risk = "🚨 极高风险 (敏感指标)"
    elif any(int(ans.get(i, 0) or 0) == 3 for i in emo_range) or (emo_score / emo_max > 0.6):
        emo_risk = "🚩 情绪预警"
    else:
        emo_risk = "正常"

    # 【注意状态预警】 (对应 67-72 题，索引 66-71)
    att_range = range(66, 72)
    att_score = sum(int(ans.get(i, 0) or 0) for i in att_range)
    att_max = len(att_range) * 3  # 总分 18
    
    # 触发条件：任意一题3分 OR 总分超过60%
    if any(int(ans.get(i, 0) or 0) == 3 for i in att_range) or (att_score / att_max > 0.6):
        adhd_risk = "🟠 注意受损"
    else:
        adhd_risk = "正常"

    # 【身体状态预警】 (对应 73-78 题，索引 72-77)
    # 触发条件：均分 > 1.5
    body_range = range(72, 78)
    body_scores = [int(ans.get(i, 0) or 0) for i in body_range]
    body_avg = sum(body_scores) / len(body_scores) if body_scores else 0
    
    body_risk = "🔵 生理负荷" if body_avg > 1.5 else "正常"

   # 5. 构造飞书表格字段 (Key 必须与图片表头完全一字不差)
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
        "报告链接": report_link,    # 👈 对应飞书"报告链接"列
        "答题链接": detail_link     # 👈 对应飞书"答题链接"列
        
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
                接下来的测评，请放下焦虑，客观回顾近三个月的家庭状态。<br>
                这不是一份考卷，而是给孩子和你自己一次被"看见"的机会。
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

    if age_picked == st.session_state.age:
        st.caption("💡 当前显示默认年龄，请拖动滑块确认孩子周岁")

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
                
                if cur == 84:  # 第 85 题提交 
                    # 这里增加转圈等待提示 
                    with st.spinner('正在为您生成解析报告，请稍候...'):
                        try:
                            # 1. 准备数据
                            report_payload = prepare_report_data()
                            # 2. 执行强制同步，获取返回结果
                            success = send_to_feishu_bitable(report_payload)
                            
                            if success:
                                # 只有同步成功，才切换状态并跳转
                                st.session_state.step = 'report'
                                st.rerun()
                            else:
                                # 同步失败，停在原地并报错
                                st.error("数据保存失败，请再次点击提交按钮。")
                        except Exception as e:
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
    # 防御性检查：如果 RID 丢失，重新生成一个（虽然理论上不会发生）
    if 'rid' not in st.session_state or not st.session_state.rid:
        st.session_state.rid = str(random.randint(100000, 999999))
        # 可选：记录一条日志
        print("警告：进入报告页时 RID 丢失，已自动生成临时编号。")
    
    # --- 1. 紧凑修复版：集成印章、水印感与动态质感 ---
    st.markdown(f"""<div style="position:relative; background:linear-gradient(135deg, #FFFFFF 0%, #F8F9FB 100%); border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.08); border:1px solid #ECEFF1; margin-top:-60px; margin-bottom:20px; overflow:visible; width:100%;"><div style="height:6px; background:linear-gradient(90deg, #1A237E, #FF7043); width:100%; border-radius:12px 12px 0 0;"></div><div style="position: absolute; top: 15px; right: 15px; width: 85px; height: 85px; border: 3px double rgba(255, 82, 82, 0.6); border-radius: 50%; display: flex; align-items: center; justify-content: center; transform: rotate(-15deg); z-index: 99; pointer-events: none;"><div style="width: 70px; height: 70px; border: 1px solid rgba(255, 82, 82, 0.3); border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;"><span style="color: rgba(255, 82, 82, 0.7); font-size: 11px; font-weight: 900; line-height:1;">曹校长</span><span style="color: rgba(255, 82, 82, 0.7); font-size: 16px; font-weight: 900; line-height:1.2;">已认证</span></div></div><div style="padding:30px 0 15px 0; width:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;"><div style="color:#90A4AE; font-size:10px; letter-spacing:3px; line-height:1; margin-bottom:12px; width:100%;">REPORT ANALYSIS</div><div style="color:#1A237E; font-size:32px; font-weight:900; line-height:1; margin:0 auto; width:100%; display:block; text-align:center;">多维报告解析</div><div style="color:#546E7A; font-size:14px; font-weight:500; line-height:1; margin-top:12px; width:100%;">家庭教育十维深度探查</div></div><div style="background:#FFFDE7; border-top:1px dashed #FFD54F; border-bottom:1px dashed #FFD54F; margin:0 10px 15px 10px; border-radius:8px; height:85px; display:flex; align-items:center; justify-content:center;"><table style="width:100%; border-collapse:collapse; table-layout:fixed; border:none; margin:0;"><tr style="border:none; vertical-align:middle;"><td style="padding-left:15px; text-align:left; vertical-align:middle; border:none;"><div style="line-height:1.4;"><p style="color:#E65100; font-size:16px; font-weight:900; margin:0;">📸 截图保存此页</p><p style="color:#F57C00; font-size:13px; font-weight:800; margin:2px 0 0 0;">1V1 咨询核心凭证</p></div></td><td style="padding-right:15px; text-align:right; border-left:1px dashed #FFD54F; width:42%; vertical-align:middle; border:none;"><div style="line-height:1.2;"><p style="color:#90A4AE; font-size:11px; font-weight:800; margin:0;">报告编号</p><p style="color:#1A237E; font-family:monospace; font-size:24px; font-weight:900; margin:2px 0 0 0;">{st.session_state.rid}</p></div></td></tr></table></div></div>""", unsafe_allow_html=True)
    
    # 1. 风险预警模块（暖橙色卡片提示）
    st.markdown("<p style='color:#E65100; font-weight:bold; margin-bottom:10px;'>核心风险筛查：</p>", unsafe_allow_html=True)
    
    # 7. 情绪状态预警 (59-66题)
    emo_scores = [st.session_state.ans.get(i, 0) for i in range(58, 66)]
    if any(s == 3 for s in emo_scores) or (sum(emo_scores) >= 24 * 0.6) or any(st.session_state.ans.get(i, 0) >= 2 for i in [64, 65]): # 假设65/66为消极倾向题
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【情绪状态预警】当前孩子情绪安全水位极低，沉默是他在呼救。首要任务不是抓学习，而是\"稳情绪\"，必须立刻切入心理安全干预。</div>", unsafe_allow_html=True)
    
    # 8. 注意状态预警 (67-72题)
    adhd_scores = [st.session_state.ans.get(i, 0) for i in range(66, 72)]
    if any(s == 3 for s in adhd_scores) or (sum(adhd_scores) >= 18 * 0.6):
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【注意状态预警】疑似 ADHD 特质。孩子大脑天生自带\"降噪功能缺陷\"，不要再骂他粗心了，他需要专业的脑功能整合训练。</div>", unsafe_allow_html=True)

    # 9. 身体状态预警 (73-78题)
    body_avg = sum(st.session_state.ans.get(i, 0) for i in range(72, 78)) / 6
    if body_avg > 1.5:
        st.markdown("<div class='warn-banner bg-blue'>⚠️ 【身体状态预警】当前表现受生理代谢（如营养、过敏）影响。生理基础不稳，心智无法成长，建议从营养与节律层面修复。</div>", unsafe_allow_html=True)

    # --- 2. 雷达图绘制 (视觉专业化升级版) ---
    scores, labels = [], list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        # 转化为100分制展示，分值越高代表风险越高
        scores.append(round(avg * 33.3, 1)) 

    # 增加闭环点（让雷达图线条连起来，不留缺口）
    radar_scores = scores + [scores[0]]
    radar_labels = labels + [labels[0]]

    fig = go.Figure(data=go.Scatterpolar(
        r=radar_scores, 
        theta=radar_labels, 
        fill='toself', 
        # 线条颜色改为更有质感的深蓝，填充色改为半透明橙，对比强烈
        line=dict(color='#1A237E', width=3), 
        fillcolor='rgba(255, 112, 67, 0.2)',
        marker=dict(size=8, color='#FF7043')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 100],
                tickfont=dict(size=10, color="#90A4AE"),
                gridcolor="#ECEFF1", # 浅灰色网格，更有高级感
                angle=90 # 刻度线方向
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color="#1A237E", family="PingFang SC"),
                gridcolor="#ECEFF1"
            ),
            bgcolor="rgba(255,255,255,0)" # 背景透明
        ),
        showlegend=False, 
        height=350, 
        margin=dict(t=40, b=40, l=50, r=50)
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("<p style='font-size:12px; color:#90A4AE; text-align:center;'>注：覆盖越大，代表该维度的"负荷"或"风险"越大。</p>", unsafe_allow_html=True)

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

    # --- 4. 情感升华：校长的结语 (新增：建立心理链接) ---
    st.markdown("""
        <div style='text-align:center; margin: 40px 0 30px 0; padding: 0 10px;'>
            <div style='width: 30px; height: 3px; background: #FF7043; margin: 0 auto 20px; border-radius:2px;'></div>
            <p style='color:#1A237E; font-size:18px; font-weight:600; line-height:1.8; font-style:italic;'>
                "这份报告揭示了孩子的求救，<br>
                也看见了您的委屈。"
            </p>
            <p style='color:#546E7A; font-size:15px; margin-top:12px; line-height:1.6;'>
                每一个在深夜焦虑的父母，其实都在孤军奋战。<br>
                改变不一定靠"用力吼叫"，而是靠<b>"精准调频"</b>。
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. 微信转化区域 (最稳固拼接版) ---

    # 确保变量名是 qr_b64，引号一定要闭合
    qr_b64 = """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""".replace('\n', '').strip()

    # 第一部分：顶部到按钮和提示语
    html_part1 = """
    <div style="border:2px solid #E8EAF6; background:#FFFFFF; padding:20px; border-radius:20px; box-shadow:0 12px 40px rgba(26,35,126,0.12); text-align:center; margin:10px 0;">
    <div style="background:#FFF5F2; display:inline-block; padding:4px 15px; border-radius:20px; color:#FF7043; font-size:13px; font-weight:bold; margin-bottom:15px;">
        🎯 深度干预建议 · 预约通道
    </div>
    <p style="color:#1A237E; font-size:20px; font-weight:900; line-height:1.4; margin-bottom:15px;">
        既然已经找到了"病灶"，<br>
        <span style="color:#FF7043;">让我们一起对症下药。</span>
    </p>
    <div style="text-align:left; margin:15px 0; background:#F8F9FA; padding:15px; border-radius:15px; border:1px solid #EEE;">
        <p style="margin:0 0 10px 0; font-weight:bold; color:#1A237E; font-size:18px;">添加微信预约曹校长：</p>
        <p style="margin:6px 0; color:#455A64; font-size:16px;"><b style="color:#C62828;">✓</b> 10个维度<b style="color:#FF7043;"> 个性化 </b>改善方案</p>
        <p style="margin:6px 0; color:#455A64; font-size:16px;"><b style="color:#C62828;">✓</b> 30分钟<b style="color:#FF7043;"> 1V1 </b>深度解析报告</p>
        <p style="margin:6px 0; color:#455A64; font-size:16px;"><b style="color:#C62828;font-weight:bold;">✓</b> <b style="color:#FF7043;">特惠 198 元</b> <span style="text-decoration:line-through; font-size:16px; color:#90A4AE;">(原价 598)</span>
    </div>
    <div style="margin-bottom:20px;">
        <p style="color:#546E7A; font-size:12px; margin-bottom:8px;">您的专属报告编号：</p>
        <div style="background:#FFF9C4; border:2px dashed #FBC02D; font-size:30px; font-weight:900; color:#E65100; padding:10px 20px; border-radius:12px; display:inline-block;">
    """

    # 第二部分：编号、按钮、小贴士
    # 这里手动拼入 rid
    rid_val = str(st.session_state.rid)
    html_part2 = """
        </div>
    </div>
    <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:16px; border-radius:15px; font-size:18px; font-weight:bold; -webkit-tap-highlight-color: transparent;">
        👉 点击预约 · 开启家庭重塑
    </a>
    <p style="color:#90A4AE; font-size:11px; margin-top:12px; line-height:1.5;">
        * 曹校长亲自解读，名额稀缺，添加后请发送编号<br>
        * 若点击按钮无反应，请长按二维码识别或截屏扫码
    </p>
    """
    # --- 在这里开始插入你的"曹校后台专用"代码 ---
    st.write("") 
    st.divider() # 画一条分割线，区分用户内容和管理内容
    
    with st.expander("🔍 曹校后台专用：查看原始答题明细", expanded=False):
        # 遍历 85 道题
        for i in range(85):
            # 获取题目文本，如果没有（比如80题以后）则显示"背景/意愿"
            q_text = QUESTIONS[i] if i < len(QUESTIONS) else f"附加信息题 {i+1}"
            u_ans = st.session_state.ans.get(i, "未填")
            
            # 显示题号和题目
            st.markdown(f"**{i+1}. {q_text}**")
            
            # 针对前78题的分值做个简单翻译
            if i < 78:
                score_desc = {0: "从不", 1: "偶尔", 2: "经常", 3: "总是"}
                display_text = f"{score_desc.get(u_ans, u_ans)} ({u_ans}分)"
                # 如果是2分或3分，用醒目的红色显示 
                if isinstance(u_ans, int) and u_ans >= 2:
                    st.error(f"👉 选项：{display_text}")
                else:
                    st.info(f"👉 选项：{display_text}")
            else:
                # 79-85题是文本描述
                st.success(f"👉 回答：{u_ans}")
            
            st.write("---") # 题目之间的细分割线
    # --- 插入结束 ---
    
    # 第三部分：二维码图片
    img_html = '<img src="data:image/png;base64,' + qr_b64 + '" style="width:160px; height:160px; display:block; margin:15px auto 10px auto; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">'

    # 第四部分：页脚文字和闭合
    html_part3 = """
    <p style="color:#FF7043; font-size:13px; font-weight:bold; margin-bottom:5px;">↑ 长按上方二维码识别 ↑</p>
    </div>
    """

    # 最终渲染：用加号拼接，绝对不报语法错
    st.markdown(html_part1 + rid_val + html_part2 + img_html + html_part3, unsafe_allow_html=True)

    # --- 6. 底部重置按钮 ---
    st.write("") 
    if st.button("🔄 重新开始测评", use_container_width=True):
        st.session_state.clear()
        st.rerun()
