import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_extrema_experiment():
    st.subheader("🏔️ 多元函数极值交互实验")
    st.caption("拖动滑块改变视角，观察曲面上的山峰（极大值）、山谷（极小值）和鞍点。")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 选择函数")
        func_choice = st.selectbox("", [
            "f(x,y) = x² + y²（极小值）",
            "f(x,y) = -x² - y²（极大值）",
            "f(x,y) = x² - y²（鞍点）",
            "f(x,y) = x³ - 3xy²（猴鞍面）"
        ])
        
        elev = st.slider("上下视角", 0, 90, 30)
        azim = st.slider("旋转角度", 0, 360, 45)
        
        if func_choice == "f(x,y) = x² + y²（极小值）":
            st.success("📌 原点 (0, 0) 是极小值点，像一个碗底。")
        elif func_choice == "f(x,y) = -x² - y²（极大值）":
            st.success("📌 原点 (0, 0) 是极大值点，像一个倒扣的碗。")
        elif func_choice == "f(x,y) = x² - y²（鞍点）":
            st.warning("📌 原点 (0, 0) 是鞍点，一个方向是山谷，另一个方向是山峰。")
        else:
            st.info("📌 原点附近有三个谷和三个峰交错，形如猴鞍。")
    
    with col2:
        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)
        
        if func_choice == "f(x,y) = x² + y²（极小值）":
            Z = X**2 + Y**2
        elif func_choice == "f(x,y) = -x² - y²（极大值）":
            Z = -X**2 - Y**2
        elif func_choice == "f(x,y) = x² - y²（鞍点）":
            Z = X**2 - Y**2
        else:
            Z = X**3 - 3*X*Y**2
        
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8, linewidth=0)
        ax.scatter([0], [0], [0], color='black', s=100, marker='o', label='驻点 (0,0)')
        ax.view_init(elev=elev, azim=azim)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title(func_choice)
        ax.legend()
        fig.colorbar(surf, shrink=0.5)
        st.pyplot(fig)
    
    st.caption("💡 旋转视角观察：极小值点像一个碗底，极大值点像倒扣的碗，鞍点像马鞍——一个方向是谷、另一个方向是峰。")