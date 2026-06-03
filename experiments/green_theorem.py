import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_green_experiment():
    st.subheader("🔄 格林公式交互实验")
    st.caption("格林公式：闭曲线上的环流量 = 内部旋度的二重积分。")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 选择向量场")
        field_choice = st.selectbox("", [
            "F = (-y, x) —— 旋度 = 2",
            "F = (x, y) —— 旋度 = 0（无旋场）",
            "F = (-y/2, x/2) —— 旋度 = 1",
            "F = (y², x²) —— 旋度 = 2x - 2y"
        ])
        
        st.markdown("### 积分区域")
        region_choice = st.selectbox("", [
            "单位圆：x² + y² ≤ 1",
            "正方形：|x| ≤ 1, |y| ≤ 1"
        ])
        
        if "旋度 = 0" in field_choice:
            st.success("🟢 旋度处处为零，闭路积分 = 0")
        elif "旋度 = 1" in field_choice:
            st.info("🔵 旋度恒为 1，闭路积分 = 区域面积")
        elif "旋度 = 2" in field_choice:
            st.info("🔵 旋度恒为 2，闭路积分 = 2 × 面积")
        else:
            st.warning("🟡 旋度随位置变化")
    
    with col2:
        # 向量场定义
        if "F = (-y, x)" in field_choice:
            P = lambda x, y: -y
            Q = lambda x, y: x
        elif "F = (x, y)" in field_choice:
            P = lambda x, y: x
            Q = lambda x, y: y
        elif "F = (-y/2, x/2)" in field_choice:
            P = lambda x, y: -y/2
            Q = lambda x, y: x/2
        else:
            P = lambda x, y: y**2
            Q = lambda x, y: x**2
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 左图：向量场 + 边界曲线
        x = np.linspace(-1.5, 1.5, 20)
        y = np.linspace(-1.5, 1.5, 20)
        X, Y = np.meshgrid(x, y)
        U = P(X, Y)
        V = Q(X, Y)
        
        ax1.quiver(X, Y, U, V, color='blue', alpha=0.5, scale=20)
        
        # 画边界曲线
        if "圆" in region_choice:
            t = np.linspace(0, 2*np.pi, 200)
            ax1.plot(np.cos(t), np.sin(t), 'r-', linewidth=2, label='边界曲线 L')
            ax1.set_title("向量场 F 与闭曲线 L")
        else:
            square_x = [-1, 1, 1, -1, -1]
            square_y = [-1, -1, 1, 1, -1]
            ax1.plot(square_x, square_y, 'r-', linewidth=2, label='边界曲线 L')
            ax1.set_title("向量场 F 与闭曲线 L")
        
        ax1.axhline(y=0, color='gray', linewidth=0.5)
        ax1.axvline(x=0, color='gray', linewidth=0.5)
        ax1.set_xlim(-1.5, 1.5)
        ax1.set_ylim(-1.5, 1.5)
        ax1.set_aspect('equal')
        ax1.legend()
        
        # 右图：旋度热力图
        if "F = (-y, x)" in field_choice:
            curl = np.ones_like(X) * 2
            curl_label = "旋度 = 2（常数）"
        elif "F = (x, y)" in field_choice:
            curl = np.zeros_like(X)
            curl_label = "旋度 = 0（无旋场）"
        elif "F = (-y/2, x/2)" in field_choice:
            curl = np.ones_like(X)
            curl_label = "旋度 = 1（常数）"
        else:
            curl = 2*X - 2*Y
            curl_label = "旋度 = 2x - 2y"
        
        im = ax2.contourf(X, Y, curl, levels=20, cmap='coolwarm', alpha=0.8)
        plt.colorbar(im, ax=ax2, label='旋度值')
        
        if "圆" in region_choice:
            ax2.plot(np.cos(t), np.sin(t), 'k-', linewidth=2)
        else:
            ax2.plot(square_x, square_y, 'k-', linewidth=2)
        
        ax2.set_title(f"区域 D 上的旋度分布\n{curl_label}")
        ax2.set_aspect('equal')
        
        st.pyplot(fig)
    
    st.caption("💡 格林公式：∮_L Pdx+Qdy = ∬_D (∂Q/∂x - ∂P/∂y) dxdy。左图是向量场和边界，右图是旋度热力图。")