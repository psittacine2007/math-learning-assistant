import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_double_integral_experiment():
    st.subheader("📦 二重积分体积演示")
    st.caption("二重积分的几何意义：以区域 D 为底、曲面 z=f(x,y) 为顶的曲顶柱体的体积。")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 选择顶面函数")
        func_choice = st.selectbox("", [
            "f(x,y) = 1（平顶柱体）",
            "f(x,y) = x² + y²（旋转抛物面）",
            "f(x,y) = 2 - x - y（斜平面）",
            "f(x,y) = sin(x)cos(y)（波动曲面）"
        ])
        
        st.markdown("### 积分区域")
        region = st.selectbox("", [
            "矩形：[-1,1] × [-1,1]",
            "圆形：x² + y² ≤ 1"
        ])
        
        grid_size = st.slider("网格密度", 10, 50, 20)
        
        if func_choice == "f(x,y) = 1（平顶柱体）":
            expected = 4 if "矩形" in region else np.pi
            st.info(f"理论体积 ≈ {expected:.3f}（底面积 × 高1）")
    
    with col2:
        x = np.linspace(-1, 1, grid_size)
        y = np.linspace(-1, 1, grid_size)
        X, Y = np.meshgrid(x, y)
        
        if func_choice == "f(x,y) = 1（平顶柱体）":
            Z = np.ones_like(X)
        elif func_choice == "f(x,y) = x² + y²（旋转抛物面）":
            Z = X**2 + Y**2
        elif func_choice == "f(x,y) = 2 - x - y（斜平面）":
            Z = 2 - X - Y
        else:
            Z = np.sin(X) * np.cos(Y)
        
        if "圆形" in region:
            mask = X**2 + Y**2 <= 1
            Z[~mask] = np.nan
        
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, linewidth=0)
        ax.view_init(elev=30, azim=45)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title(f'曲顶柱体：{func_choice}')
        fig.colorbar(surf, shrink=0.5)
        st.pyplot(fig)
    
    st.caption("💡 曲面下的体积就是二重积分的值。调整视角和网格密度，直观感受体积的几何意义。")