import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# 从 settings 导入配置
from settings import CHAPTERS, SYSTEM_PROMPT

# 导入交互实验模块
from experiments.gradient import show_gradient_experiment
from experiments.extrema import show_extrema_experiment
from experiments.double_integral import show_double_integral_experiment
from experiments.series_convergence import show_series_experiment
from experiments.damped_vibration import show_damped_vibration_experiment

# ====== 配置 API ======
load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
MODEL = "deepseek-v4-flash"

# ====== 会话状态初始化 ======
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ====== 侧边栏：章节导航与模式切换 ======
st.sidebar.title("📚 高数下册知识地图")
st.sidebar.caption('💡 提示：选择章节后点击按钮，AI 将按照“先类比、再几何、后公式”的原则为你讲解。')

# 模式切换
mode = st.sidebar.radio("选择模式", ["概念讲解", "练习模式", "交互实验"])

# 选择章
selected_chapter = st.sidebar.selectbox("选择章", list(CHAPTERS.keys()))

# 选择节
if selected_chapter:
    selected_section = st.sidebar.selectbox(
        "选择节",
        list(CHAPTERS[selected_chapter].keys())
    )

# ====== 交互实验模式 ======
if mode == "交互实验":
    experiment = st.sidebar.selectbox("选择实验", [
        "方向导数和梯度",
        "多元函数极值",
        "二重积分体积演示",
        "级数部分和收敛",
        "阻尼振动"
    ])

    if experiment == "方向导数和梯度":
        show_gradient_experiment()
    elif experiment == "多元函数极值":
        show_extrema_experiment()
    elif experiment == "二重积分体积演示":
        show_double_integral_experiment()
    elif experiment == "级数部分和收敛":
        show_series_experiment()
    elif experiment == "阻尼振动":
        show_damped_vibration_experiment()

# ====== 概念讲解模式 ======
elif mode == "概念讲解":
    if st.sidebar.button("🚀 开始图像化学习", type="primary"):
        prompt_text = CHAPTERS[selected_chapter][selected_section]
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        st.rerun()

    # 主界面
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

# ====== 练习模式 ======
else:  # mode == "练习模式"
    if st.sidebar.button("📝 生成一道练习题", type="primary"):
        exercise_prompt = (
            f"请根据{selected_section}的内容，生成一道练习题。"
            "要求：1）包含一个常见错误选项；"
            "2）用户回答后，你必须先明确标出错误类型，格式为：【错误类型：计算错误/理解错误/方法错误】；"
            "3）然后用“颜色标记错误步骤”的文字方式给出针对性反馈；"
            "4）诊断完成后，出一道同类型的新题检验用户是否真正掌握。"
            "直接出题，不用讲解概念。"
        )
        st.session_state.messages.append({"role": "user", "content": exercise_prompt})
        st.rerun()

    # 主界面
    st.title("📝 高数下册练习模式")
    st.caption("AI 出题 → 你作答 → AI 诊断错误类型 → 针对性反馈 → 再练习")

    # 显示历史消息
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # 用户自由输入
    if prompt := st.chat_input("输入你的答案，或输入“来一道新题”..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("正在诊断..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

st.sidebar.divider()
st.sidebar.caption("💡 概念讲解：先图后公式 | 练习模式：AI诊断错误类型 | 交互实验：动手感受数学")