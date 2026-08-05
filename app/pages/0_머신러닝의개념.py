# streamlit webapp의 pages 경로 밑에 서브 페이지로 다음을 생성해주세요.
#머신러닝의 개념에 대해 학습할 콘텐츠 생성
#간단하게 머신러닝의 개념을 실습할 수 있는 시뮬레이터 포함(mock data를 생성해서 (분류 데이터) 직접 실습하도록 함)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.datasets import make_blobs, make_moons
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝의 개념",
    page_icon="🤖",
    layout="wide"
)

# 메인 타이틀
st.title("🤖 머신러닝(Machine Learning)의 개념")
st.write("머신러닝의 기본 원리를 이해하고, 직접 데이터를 생성하고 모델을 학습시켜보는 시뮬레이션 공간입니다.")

# 탭 구성: 개념 학습 / 실습 시뮬레이터
tab1, tab2 = st.tabs(["📚 머신러닝 개념 학습", "🧪 인터랙티브 분류 시뮬레이터"])

# ==========================================
# TAB 1: 머신러닝 개념 학습
# ==========================================
with tab1:
    st.subheader("1. 전통적 프로그래밍 vs 머신러닝")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💻 전통적인 프로그래밍")
        st.info("**[ 데이터 ] + [ 명시적 규칙 ] ➡️ [ 결과 ]**")
        st.write("사람이 직접 조건문(if-else) 등의 규칙을 프로그래밍하여 결과값을 도출합니다.")
        
    with col2:
        st.markdown("### 🧠 머신러닝")
        st.success("**[ 데이터 ] + [ 정답(결과) ] ➡️ [ 규칙(모델) ]**")
        st.write("컴퓨터가 수많은 데이터를 바탕으로 스스로 패턴과 규칙을 학습하여 정답을 예측합니다.")

    st.markdown("---")
    st.subheader("2. 머신러닝의 주요 유형")
    
    type_col1, type_col2, type_col3 = st.columns(3)
    with type_col1:
        st.markdown("#### 🎯 지도학습 (Supervised Learning)")
        st.write("- **정답(라벨)이 있는 데이터**를 학습")
        st.write("- **분류(Classification)**: 스팸 메일 여부, 암 양성/음성")
        st.write("- **회귀(Regression)**: 집값 예측, 내일 기온 예측")
        
    with type_col2:
        st.markdown("#### 🔍 비지도학습 (Unsupervised Learning)")
        st.write("- **정답(라벨)이 없는 데이터**를 학습")
        st.write("- 데이터 간의 숨겨진 구조나 패턴을 발견")
        st.write("- **군집화(Clustering)**: 고객 세분화, 유사 뉴스 그룹핑")
        
    with type_col3:
        st.markdown("#### 🎮 강화학습 (Reinforcement Learning)")
        st.write("- **보상(Reward)**을 극대화하는 방향으로 학습")
        st.write("- 에이전트가 환경과 상호작용하며 최적의 행동을 터득")
        st.write("- 알파고, 자율주행, 게임 AI 등")

# ==========================================
# TAB 2: 인터랙티브 분류 시뮬레이터
# ==========================================
with tab2:
    st.subheader("🧪 머신러닝 (분류) 모델 시뮬레이터")
    st.write("가상(Mock) 데이터를 생성하고 분류 알도리즘이 데이터의 경계를 어떻게 학습하는지 직접 확인해보세요.")

    # 1. 사이드바 / 컨트롤러 설정
    st.sidebar.header("⚙️ 시뮬레이터 설정")
    
    data_type = st.sidebar.selectbox("데이터 형태 선택", ["구분하기 쉬운 데이터 (Blobs)", "복잡한 데이터 (Moons)"])
    n_samples = st.sidebar.slider("데이터 개수", min_value=50, max_value=500, value=200, step=50)
    noise_level = st.sidebar.slider("데이터 노이즈(혼잡도)", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    
    algorithm = st.sidebar.selectbox("머신러닝 알고리즘 선택", ["의사결정나무 (Decision Tree)", "로지스틱 회귀 (Logistic Regression)", "K-최근접 이웃 (KNN)"])

    # 2. Mock Data 생성
    if data_type == "구분하기 쉬운 데이터 (Blobs)":
        X, y = make_blobs(n_samples=n_samples, centers=2, cluster_std=1.0 + noise_level * 3, random_state=42)
    else:
        X, y = make_moons(n_samples=n_samples, noise=noise_level, random_state=42)

    df = pd.DataFrame(X, columns=["특성 1 (X1)", "특성 2 (X2)"])
    df["클래스 (Target)"] = y.astype(str)

    # Train / Test 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 3. 알고리즘 생성 및 학습
    if algorithm == "의사결정나무 (Decision Tree)":
        max_depth = st.sidebar.slider("나무 깊이 (Max Depth)", 1, 10, 3)
        model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    elif algorithm == "로지스틱 회귀 (Logistic Regression)":
        model = LogisticRegression()
    else:
        n_neighbors = st.sidebar.slider("이웃 수 (K)", 1, 15, 5)
        model = KNeighborsClassifier(n_neighbors=n_neighbors)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # 4. 시각화 영역 (데이터 분포 + 결정 경계)
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 📊 결정 경계(Decision Boundary) 시각화")
        
        # 결정 경계 그리드 생성
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
        
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # Plotly 차트 생성
        fig = go.Figure()

        # 배경 (결정 경계 영역)
        fig.add_trace(go.Contour(
            x=np.linspace(x_min, x_max, 100),
            y=np.linspace(y_min, y_max, 100),
            z=Z,
            showscale=False,
            opacity=0.3,
            colorscale=['#FFAAAA', '#AAAAFF']
        ))

        # 데이터 포인트
        for cls_val, color, name in zip([0, 1], ['red', 'blue'], ['클래스 0', '클래스 1']):
            mask = y == cls_val
            fig.add_trace(go.Scatter(
                x=X[mask, 0],
                y=X[mask, 1],
                mode='markers',
                name=name,
                marker=dict(color=color, size=8, line=dict(width=1, color='darkgray'))
            ))

        fig.update_layout(
            title=f"모델 예측 영역 ({algorithm})",
            xaxis_title="특성 1 (X1)",
            yaxis_title="특성 2 (X2)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### 🎯 모델 평가")
        st.metric(label="테스트 데이터 정확도 (Accuracy)", value=f"{acc * 100:.1f}%")
        
        st.markdown("---")
        st.markdown("### 🔮 실시간 예측 테스트")
        st.write("새로운 데이터 값을 입력하여 모델이 어떤 클래스로 예측하는지 테스트해보세요.")
        
        val_x1 = st.number_input("특성 1 값 (X1)", value=float(X[:, 0].mean()))
        val_x2 = st.number_input("특성 2 값 (X2)", value=float(X[:, 1].mean()))
        
        input_data = np.array([[val_x1, val_x2]])
        pred_single = model.predict(input_data)[0]
        
        if pred_single == 0:
            st.error(f"예측 결과: **클래스 0 (🔴)**")
        else:
            st.info(f"예측 결과: **클래스 1 (🔵)**")

    # 5. 생성된 데이터 표 형태 확인
    with st.expander("📄 생성된 Mock 데이터 보기 (상위 10개)"):
        st.dataframe(df.head(10), use_container_width=True)
