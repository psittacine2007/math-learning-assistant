import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_damped_vibration_experiment():
    st.subheader("🪶 阻尼振动实验")
    st.caption("二阶常系数线性微分方程 mx'' + μx' + kx = 0 的解。调整阻尼系数观察振动形态的变化。")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 参数设置")
        m = st.slider("质量 m", 0.1, 5.0, 1.0, 0.1)
        k = st.slider("刚度 k", 0.1, 10.0, 4.0, 0.1)
        mu = st.slider("阻尼系数 μ", 0.0, 10.0, 0.5, 0.1)
        
        n = mu / (2 * m)  # 阻尼比相关参数
        omega0 = np.sqrt(k / m)  # 固有频率
        
        st.markdown("---")
        st.markdown("### 系统分析")
        st.latex(r"\omega_0 = \sqrt{k/m} = " + f"{omega0:.3f}")
        st.latex(r"n = \mu/(2m) = " + f"{n:.3f}")
        
        if n == 0:
            st.success("🔵 无阻尼：简谐振动，永不衰减")
        elif n < omega0:
            st.info("🟢 小阻尼：衰减振荡")
            omega_d = np.sqrt(omega0**2 - n**2)
            st.latex(r"\omega_d = " + f"{omega_d:.3f}")
        elif abs(n - omega0) < 0.01:
            st.warning("🟡 临界阻尼：刚好不振荡，最快回到平衡位置")
        else:
            st.error("🔴 大阻尼：缓慢衰减，无振荡")
    
    with col2:
        t = np.linspace(0, 20, 500)
        x0, v0 = 1.0, 0.0  # 初始位移和速度
        
        if n == 0:
            x = x0 * np.cos(omega0 * t) + v0/omega0 * np.sin(omega0 * t)
            title = "无阻尼简谐振动"
        elif n < omega0:
            omega_d = np.sqrt(omega0**2 - n**2)
            x = np.exp(-n * t) * (x0 * np.cos(omega_d * t) + (v0 + n*x0)/omega_d * np.sin(omega_d * t))
            title = f"小阻尼衰减振荡 (n={n:.2f}, ωd={omega_d:.2f})"
        elif abs(n - omega0) < 0.01:
            x = (x0 + (v0 + n*x0) * t) * np.exp(-n * t)
            title = "临界阻尼"
        else:
            r1 = -n + np.sqrt(n**2 - omega0**2)
            r2 = -n - np.sqrt(n**2 - omega0**2)
            C1 = (v0 - r2*x0) / (r1 - r2)
            C2 = x0 - C1
            x = C1 * np.exp(r1 * t) + C2 * np.exp(r2 * t)
            title = f"大阻尼 (n={n:.2f} > ω0={omega0:.2f})"
        
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(t, x, 'b-', linewidth=1.5)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.set_xlabel('时间 t')
        ax.set_ylabel('位移 x(t)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    st.caption("💡 调节阻尼系数 μ 观察：无阻尼时永不衰减，小阻尼时振荡衰减，临界阻尼和大阻尼时无振荡。")