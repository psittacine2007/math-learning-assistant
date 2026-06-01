import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_series_experiment():
    st.subheader("📈 级数部分和收敛动画")
    st.caption("观察级数的部分和如何随项数增加而变化。收敛级数会趋近一个定值，发散级数则不断增长或振荡。")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 选择级数")
        series_choice = st.selectbox("", [
            "几何级数：∑ (1/2)ⁿ（收敛于1）",
            "调和级数：∑ 1/n（发散）",
            "交错调和级数：∑ (-1)ⁿ⁻¹/n（收敛于ln2）",
            "p-级数：∑ 1/n²（收敛于π²/6）"
        ])

        n_max = st.slider("最大项数 n", 1, 200, 50)

        # 精确判断，避免混淆
        if series_choice.startswith("几何级数"):
            st.success("收敛于 1")
        elif series_choice.startswith("交错调和级数"):
            st.success("收敛于 ln2 ≈ 0.693")
        elif series_choice.startswith("调和级数"):
            st.warning("发散！尽管通项趋于0，但部分和缓慢增长至无穷")
        elif series_choice.startswith("p-级数"):
            st.success("收敛于 π²/6 ≈ 1.645")

    with col2:
        n = np.arange(1, n_max + 1)

        if series_choice.startswith("几何级数"):
            terms = (1/2)**n
            label = "几何级数：∑ (1/2)ⁿ"
            limit = 1
        elif series_choice.startswith("交错调和级数"):
            terms = (-1)**(n-1) / n
            label = "交错调和级数：∑ (-1)ⁿ⁻¹/n"
            limit = np.log(2)
        elif series_choice.startswith("调和级数"):
            terms = 1/n
            label = "调和级数：∑ 1/n"
            limit = None
        elif series_choice.startswith("p-级数"):
            terms = 1/n**2
            label = "p-级数：∑ 1/n²"
            limit = np.pi**2 / 6
        else:
            # 默认情况
            terms = 1/n
            label = "未知级数"
            limit = None

        partial_sums = np.cumsum(terms)

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(n, partial_sums, 'b-', linewidth=1.5, label='部分和 Sₙ')
        if limit is not None:
            ax.axhline(y=limit, color='red', linestyle='--', linewidth=1.5, label=f'极限值 = {limit:.3f}')
        ax.set_xlabel('项数 n')
        ax.set_ylabel('部分和 Sₙ')
        ax.set_title(label)
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    st.caption("💡 收敛级数的部分和逐渐趋近红色虚线；发散级数的部分和则持续增长。")