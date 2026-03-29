# --- 5. 页面流程 ---

# A. 首页 (卡片与按钮整体绝对居中)
if st.session_state.step == 'home':
    st.markdown("""
        <div class='home-mask'>
            <div class='title-l1'>HelloADHDer 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是你的老朋友。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不仅是一份考卷，更是给孩子和你自己一次被“看见”的机会。
            </div>
    """, unsafe_allow_html=True)
    
    # 将按钮放入 mask 内部 div，确保它们作为一个整体在屏幕中心
    st.markdown("<div class='home-btn-fix'>", unsafe_allow_html=True)
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
    cols = st.columns(2)
    for i, (txt, val) in enumerate(opts):
        with (cols[0] if i % 2 == 0 else cols[1]):
            if st.button(txt, key=f"q_{cur}_{i}", use_container_width=True):
                st.session_state.ans[cur] = val
                if cur == 84: 
                    st.session_state.step = 'report'
                else: 
                    st.session_state.cur += 1
                st.rerun()
    
    if cur > 0:
        st.write("")
        if st.button("⬅ 回到上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    scores = []
    labels = list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # 预警警报
    if any(st.session_state.ans.get(i, 0) == 3 for i in range(58, 66)):
        st.markdown("<div class='warn-banner bg-red'>⚠️ 【红色警报】检测到生存危机。请立刻停止施压！</div>", unsafe_allow_html=True)
    if (sum(st.session_state.ans.get(i, 0) for i in range(66, 72))/6) >= 1.5:
        st.markdown("<div class='warn-banner bg-orange'>⚠️ 【脑特性预警】孩子表现出注意力黑洞特质。</div>", unsafe_allow_html=True)

    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div class='benefit'>1. 十个维度个性化改善方案</div>
            <div class='benefit'>2. 30 分钟 1V1 深度解析</div>
            <div class='rid-box'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold;">👉 点击添加老师，预约 1V1 解析</a>
        </div>
    """, unsafe_allow_html=True)
    # --- 5. 页面流程 ---

# A. 首页 (修正嵌套逻辑，确保按钮在卡片内)
if st.session_state.step == 'home':
    # 开启卡片容器
    st.markdown("""
        <div class='home-mask'>
            <div class='title-l1'>HelloADHDer 脑科学专业版</div>
            <div class='title-l2'>家庭教育</div>
            <div class='title-l3'>十维深度探查表</div>
            <div class='intro-text'>
                这是一场跨越心与脑的对话。<br>
                你好，我是你的老朋友。<br><br>
                接下来的测评，请放下焦虑，客观回顾近一个月的家庭状态。<br>
                这不仅是一份考卷，更是给孩子和你自己一次被“看见”的机会。
            </div>
    """, unsafe_allow_html=True)
    
    # 在卡片 Div 闭合前渲染按钮
    if st.button("🚀 开始深度测评", use_container_width=True):
        st.session_state.step = 'quiz'
        st.rerun()
    
    # 闭合卡片容器
    st.markdown("</div>", unsafe_allow_html=True)

# B. 答题页
elif st.session_state.step == 'quiz':
    cur = st.session_state.cur
    st.progress((cur + 1) / 85)
    st.markdown(f"<div class='q-text'>{cur+1}. {QUESTIONS[cur]}</div>", unsafe_allow_html=True)
    
    opts = [("0 (从不)", 0), ("1 (偶尔)", 1), ("2 (经常)", 2), ("3 (总是)", 3)]
    cols = st.columns(2)
    for i, (txt, val) in enumerate(opts):
        with (cols[0] if i % 2 == 0 else cols[1]):
            if st.button(txt, key=f"q_{cur}_{i}", use_container_width=True):
                st.session_state.ans[cur] = val
                if cur == 84: 
                    st.session_state.step = 'report'
                else: 
                    st.session_state.cur += 1
                st.rerun()
    
    if cur > 0:
        st.write("")
        if st.button("⬅ 回到上一题", key="back"):
            st.session_state.cur -= 1
            st.rerun()

# C. 结果页
elif st.session_state.step == 'report':
    st.markdown("<div style='color:#C62828; font-weight:bold; background:#FFEBEE; padding:15px; border-radius:12px; text-align:center; margin-bottom:25px; border:1px solid #FFCDD2;'>📸 重要提示：编号是唯一凭证，请【截屏保存】本页结果。</div>", unsafe_allow_html=True)
    
    scores = []
    labels = list(DIM_DATA.keys())
    for dim in labels:
        r = DIM_DATA[dim]['range']
        avg = sum(st.session_state.ans.get(i, 0) for i in r) / len(r)
        scores.append(round(avg * 33.3, 1))
    
    fig = go.Figure(data=go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#1A237E', fillcolor='rgba(26, 35, 126, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # 维度预警解析及转化卡片逻辑同上，不再赘述，保持原样即可
    for dim, info in DIM_DATA.items():
        avg = sum(st.session_state.ans.get(i, 0) for i in info['range']) / len(info['range'])
        lv = 2 if avg >= 1.86 else (1 if avg >= 0.86 else 0)
        st.markdown(f"<div class='res-card'><b>{dim}</b><br>{info['levels'][lv]}</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='wx-card'>
            <p style='color:#455A64; font-size:18px; text-align:left;'>这份报告揭示了孩子的求救，也看见了您的委屈。</p>
            <div class='rid-box'>{st.session_state.rid}</div>
            <a href="https://work.weixin.qq.com/ca/cawcde91ed29d8de9f" target="_blank" style="text-decoration:none; display:block; background:#1A237E; color:white; padding:20px; border-radius:15px; font-size:20px; font-weight:bold;">👉 点击添加老师，预约 1V1 解析</a>
        </div>
    """, unsafe_allow_html=True)
