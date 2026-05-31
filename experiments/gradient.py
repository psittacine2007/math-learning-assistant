import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_gradient_experiment():
    st.subheader("🧪 方向导数与梯度交互实验")
    st.caption("拖动滑块改变方向角度，观察方向导数的变化。梯度方向（红色箭头）是方向导数最大的方向。")
    
    # 设定函数：z = x² + y² 在点 (1, 1) 处
    # 梯度 = (2x, 2y) = (2, 2) 在 (1, 1) 处
    fx, fy = 2, 2  # 梯度分量
    gradient_magnitude = np.sqrt(fx**2 + fy**2)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        angle = st.slider("选择方向角度 θ（度）", 0, 360, 45, 5)
        theta = np.radians(angle)
        direction = np.array([np.cos(theta), np.sin(theta)])
        directional_derivative = fx * direction[0] + fy * direction[1]
        
        st.latex(r"\text{方向导数} = \nabla f \cdot \mathbf{u} = " + f"{directional_derivative:.3f}")
        st.latex(r"\text{梯度模长（最大方向导数）} = " + f"{gradient_magnitude:.3f}")
        
        if abs(directional_derivative - gradient_magnitude) < 0.01:
            st.success("🎯 这就是梯度方向！方向导数达到最大值。")
        elif abs(directional_derivative + gradient_magnitude) < 0.01:
            st.warning("🔻 这是负梯度方向，方向导数达到最小值。")
        elif abs(directional_derivative) < 0.01:
            st.info("➡️ 方向与梯度垂直，方向导数为零（沿等高线方向）。")
    
    with col2:
        fig, ax = plt.subplots(figsize=(5, 5))
        # 画等高线
        x = np.linspace(0, 2, 100)
        y = np.linspace(0, 2, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2
        ax.contour(X, Y, Z, levels=10, cmap='Blues', alpha=0.6)
        
        # 标记点 (1, 1)
        ax.plot(1, 1, 'ko', markersize=6, label='点 (1, 1)')
        
        # 画梯度方向（红色）
        ax.arrow(1, 1, fx*0.15, fy*0.15, head_width=0.05, head_length=0.05, 
                 fc='red', ec='red', linewidth=2, label='梯度 ∇f = (2, 2)')
        
        # 画用户选择的方向（蓝色）
        ax.arrow(1, 1, direction[0]*0.2, direction[1]*0.2, head_width=0.05, head_length=0.05,
                 fc='blue', ec='blue', linewidth=2, label=f'选择方向 θ={angle}°')
        
        ax.set_xlim(0, 2.5)
        ax.set_ylim(0, 2.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('等高线图：f(x, y) = x² + y²')
        ax.legend(loc='upper left')
        ax.set_aspect('equal')
        st.pyplot(fig)
    
    st.caption("💡 观察：当蓝色箭头与红色箭头方向一致时，方向导数最大；垂直时为零；相反时最小。")