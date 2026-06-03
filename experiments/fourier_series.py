import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_fourier_experiment():
    st.subheader("🎵 傅里叶级数逼近实验")
    st.caption("任何周期函数都可以分解为一系列正弦波和余弦波的叠加。拖动滑块增加项数，观察逼近效果。")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 选择目标函数")
        func_choice = st.selectbox("", [
            "方波（有跳跃间断）",
            "锯齿波（有尖点）",
            "三角波（连续但不可导）",
            "半波整流（光滑）"
        ])
        
        n_terms = st.slider("傅里叶级数项数 N", 1, 50, 5)
        
        st.markdown("---")
        st.markdown("### 傅里叶系数")
        
        if "方波" in func_choice:
            st.latex(r"f(x) = \frac{4}{\pi}\sum_{k=1,3,5,\dots}^{\infty}\frac{\sin(kx)}{k}")
            st.info("📌 只有奇数项正弦波，系数按 1/k 衰减")
        elif "锯齿波" in func_choice:
            st.latex(r"f(x) = 2\sum_{k=1}^{\infty}\frac{(-1)^{k+1}\sin(kx)}{k}")
            st.info("📌 所有正弦波，系数按 1/k 衰减")
        elif "三角波" in func_choice:
            st.latex(r"f(x) = \frac{\pi}{2} - \frac{4}{\pi}\sum_{k=1,3,5,\dots}^{\infty}\frac{\cos(kx)}{k^2}")
            st.info("📌 只有奇数项余弦波，系数按 1/k² 快速衰减")
        else:
            st.latex(r"f(x) = \frac{1}{\pi} + \frac{\sin x}{2} - \frac{2}{\pi}\sum_{k=2,4,6,\dots}^{\infty}\frac{\cos(kx)}{k^2-1}")
            st.info("📌 包含常数项 + 基频正弦 + 偶次余弦波")
    
    with col2:
        x = np.linspace(-np.pi, np.pi, 1000)
        
        if "方波" in func_choice:
            target = np.where(np.sin(x) >= 0, 1, -1)
            title = f"方波逼近（N={n_terms}）"
            # 计算傅里叶级数
            y_approx = np.zeros_like(x)
            for k in range(1, n_terms + 1, 2):  # 只有奇数项
                y_approx += (4 / (np.pi * k)) * np.sin(k * x)
        elif "锯齿波" in func_choice:
            target = x / np.pi
            title = f"锯齿波逼近（N={n_terms}）"
            y_approx = np.zeros_like(x)
            for k in range(1, n_terms + 1):
                y_approx += 2 * (-1)**(k+1) * np.sin(k * x) / k
        elif "三角波" in func_choice:
            target = np.abs(x)
            title = f"三角波逼近（N={n_terms}）"
            y_approx = np.ones_like(x) * np.pi/2
            for k in range(1, n_terms + 1, 2):
                y_approx -= (4 / (np.pi * k**2)) * np.cos(k * x)
        else:
            target = np.where(np.sin(x) >= 0, np.sin(x), 0)
            title = f"半波整流逼近（N={n_terms}）"
            y_approx = np.ones_like(x) / np.pi + np.sin(x) / 2
            for k in range(2, n_terms + 1, 2):
                y_approx -= (2 / (np.pi * (k**2 - 1))) * np.cos(k * x)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, target, 'k-', linewidth=2, alpha=0.6, label='目标函数')
        ax.plot(x, y_approx, 'r-', linewidth=1.5, label=f'傅里叶逼近（N={n_terms}）')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-np.pi, np.pi)
        st.pyplot(fig)
        
        # 误差分析
        mse = np.mean((target - y_approx)**2)
        st.metric("均方误差 (MSE)", f"{mse:.4f}")
    
    st.caption("💡 吉布斯现象：对于有跳跃间断的函数（如方波），即使增加很多项，间断点附近仍有约9%的过冲。")