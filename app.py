import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
MODEL = "deepseek-v4-flash"

# ====== 高数下册章节目录 ======
CHAPTERS = {
    "第8章 多元函数微分学及其应用": {
        "8.1 多元函数的基本概念": "请用图像化方式讲解多元函数的基本概念，包括点集知识、多元函数的定义、极限和连续性。先给生活类比，再给几何直观，最后给定义。",
        "8.2 偏导数": "请讲解偏导数的概念和几何意义，用登山或曲面的类比来说明。",
        "8.3 全微分": "请用类比方式讲解全微分的定义和可微的条件。",
        "8.4 多元复合函数的求导法则": "请讲解链法则的直观理解，用图像化方式说明复合函数求导的过程。",
        "8.5 隐函数的求导法则": "请用几何直观讲解隐函数求导，一个方程和方程组的情况。",
        "8.6 方向导数和梯度": "请重点讲解方向导数和梯度的几何意义，用登山类比说明梯度方向是最陡上升方向。",
        "8.7 多元函数微分学的几何应用": "请讲解空间曲线的切线和法平面、曲面的切平面与法线的几何意义。",
        "8.8 多元函数的极值及其求法": "请用图像化方式讲解多元函数极值、条件极值和拉格朗日乘数法。",
    },
    "第9章 重积分": {
        "9.1 二重积分的概念与性质": "请用曲顶柱体体积的类比讲解二重积分的概念和性质。",
        "9.2 二重积分的计算": "请讲解直角坐标和极坐标下二重积分的计算方法，重点说明如何选择积分次序。",
        "9.3 三重积分": "请用类比方式讲解三重积分的概念和计算方法（直角坐标、柱坐标、球坐标）。",
        "9.4 重积分的应用": "请讲解重积分在曲面面积、重心、转动惯量中的应用。",
    },
    "第10章 曲线积分和曲面积分": {
        "10.1 第一型曲线积分": "请用图像化方式讲解第一型曲线积分的概念和计算方法。",
        "10.2 第二型曲线积分": "请讲解第二型曲线积分的概念，用变力沿曲线做功的类比。",
        "10.3 格林公式": "请重点讲解格林公式的几何直观，把曲线积分和二重积分联系起来。",
        "10.4 第一型曲面积分": "请用类比讲解第一型曲面积分的概念和计算。",
        "10.5 第二型曲面积分": "请讲解第二型曲面积分的概念和计算。",
        "10.6 高斯公式、通量与散度": "请用流体类比讲解高斯公式、通量和散度的物理意义。",
        "10.7 斯托克斯公式、环流量与旋度": "请讲解斯托克斯公式的几何和物理意义。",
    },
    "第11章 无穷级数": {
        "11.1 数项级数的概念和性质": "请用图像化方式讲解无穷级数的概念和收敛性质。",
        "11.2 正项级数": "请讲解正项级数的收敛判别法，用图形辅助理解。",
        "11.3 一般项级数": "请讲解交错级数、绝对收敛和条件收敛的区别。",
        "11.4 幂级数": "请讲解幂级数的概念和收敛半径的直观理解。",
        "11.5 函数的幂级数展开式": "请讲解泰勒级数和初等函数的展开，用多项式逼近的图形说明。",
        "11.6 傅里叶级数": "请用信号分解的类比讲解傅里叶级数的概念。",
    },
    "第12章 微分方程": {
        "12.1 微分方程的概念": "请讲解微分方程的基本概念，用实际例子引入。",
        "12.2 一阶微分方程": "请分类讲解可分离变量、齐次型、一阶线性微分方程的解法。",
    },
    "第13章 差分方程": {
        "13.1 差分与差分方程的概念": "请讲解差分和差分方程的基本概念。",
    },
}

# ====== 个性化系统指令 ======
SYSTEM_PROMPT = """
你是一位专门适配“图像化 + 理解驱动”型学习者的高等数学导师。
课程：高等数学（下册），涵盖多元函数微分学、重积分、曲线曲面积分、无穷级数等。
教学原则：
1. 讲解任何概念时，必须先用一个生活中的视觉化类比或几何直观描述引入，再给出严格的数学定义。
2. 用文本描述数学对象的几何形象，尽可能让用户“在脑海中看到画面”。
3. 在练习模式下，生成需要先理解图形才能作答的题目；批改时用“颜色标记错误步骤”的方式解释。
4. 所有数学公式和符号必须使用LaTeX格式，并将它们正确地包裹在$$符号中，以便正确渲染。
5. 【重要】关键数学符号必须书写准确，例如极限符号必须写为 \lim，不能写成中文“令”或错别字“林”；偏导数符号必须写为 \partial，等等。
请严格遵守以上原则，语言生动形象，条理清晰。
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ====== 侧边栏：章节导航 ======
st.sidebar.title("📚 高数下册知识地图")
st.sidebar.caption('💡 提示：选择章节后点击按钮，AI 将按照“先类比、再几何、后公式”的原则为你讲解。')

# 选择章
selected_chapter = st.sidebar.selectbox("选择章", list(CHAPTERS.keys()))

# 选择节
if selected_chapter:
    selected_section = st.sidebar.selectbox(
        "选择节",
        list(CHAPTERS[selected_chapter].keys())
    )

# 开始学习按钮
if st.sidebar.button("🚀 开始图像化学习", type="primary"):
    prompt_text = CHAPTERS[selected_chapter][selected_section]
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    st.rerun()

# ====== 主界面 ======
st.title("🎨 高数下册图像化学习助手")
st.caption("专门适配图像化理解型学习者 —— 先图后公式，类比先行")

# 显示历史消息
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 用户自由输入
if prompt := st.chat_input("你也可以直接输入问题，比如：什么是方向导数？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("正在生成视觉化讲解..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})