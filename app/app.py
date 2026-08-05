import streamlit as st
import sqlite3
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "myproject.db"
# --------------------------------------------------
# 1. DB 및 테이블 초기화 함수 (myproject.db)
# --------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1) users 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2) learning_history 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            m1 INTEGER, m2 INTEGER, m3 INTEGER, m4 INTEGER, m5 INTEGER,
            m6 INTEGER, m7 INTEGER, m8 INTEGER, m9 INTEGER, m10 INTEGER,
            score INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 비밀번호 암호화 함수 (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# DB 초기화 실행
init_db()

# 페이지 설정
st.set_page_config(layout="wide")

# --------------------------------------------------
# 2. 로그인 및 회원가입 시스템 (사이드바)
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

st.sidebar.title("🔑 회원 관리 시스템")

if st.session_state["user"] is None:
    auth_menu = st.sidebar.radio("선택", ["로그인", "회원가입"])
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if auth_menu == "로그인":
        st.sidebar.subheader("로그인")
        login_id = st.sidebar.text_input("아이디", key="login_id")
        login_pw = st.sidebar.text_input("비밀번호", type="password", key="login_pw")
        
        if st.sidebar.button("로그인", use_container_width=True):
            if login_id and login_pw:
                hashed_pw = hash_password(login_pw)
                c.execute("SELECT userid FROM users WHERE userid = ? AND password = ?", (login_id, hashed_pw))
                user = c.fetchone()
                if user:
                    st.session_state["user"] = user[0]
                    st.sidebar.success(f"🎉 {user[0]}님 반갑습니다!")
                    st.rerun()
                else:
                    st.sidebar.error("아이디 또는 비밀번호가 올바르지 않습니다.")
            else:
                st.sidebar.warning("아이디와 비밀번호를 모두 입력하세요.")
                
    elif auth_menu == "회원가입":
        st.sidebar.subheader("회원가입")
        new_id = st.sidebar.text_input("새 아이디", key="new_id")
        new_pw = st.sidebar.text_input("새 비밀번호", type="password", key="new_pw")
        new_pw_confirm = st.sidebar.text_input("비밀번호 확인", type="password", key="new_pw_confirm")
        
        if st.sidebar.button("회원가입 완료", use_container_width=True):
            if not new_id or not new_pw:
                st.sidebar.warning("모든 필드를 입력해주세요.")
            elif new_pw != new_pw_confirm:
                st.sidebar.error("비밀번호가 일치하지 않습니다.")
            else:
                try:
                    hashed_pw = hash_password(new_pw)
                    c.execute("INSERT INTO users (userid, password) VALUES (?, ?)", (new_id, hashed_pw))
                    conn.commit()
                    st.sidebar.success("회원가입 성공! 로그인 탭으로 이동하여 로그인해주세요.")
                except sqlite3.IntegrityError:
                    st.sidebar.error("이미 존재하는 아이디입니다.")
    conn.close()

else:
    st.sidebar.success(f"👤 로그인 계정: **{st.session_state['user']}**")
    if st.sidebar.button("로그아웃", use_container_width=True):
        st.session_state["user"] = None
        st.rerun()

# --------------------------------------------------
# 3. 기존 메인 웹앱 컨텐츠
# --------------------------------------------------
st.title('This is my first webapp!!')

st.subheader('국어과 AIDT')
col1, col2 = st.columns((4,1))
with col1:
    with st.expander('1차시_ 동영상'):
        st.title('동영상 시청......')
        url = 'https://www.youtube.com/watch?v=U57LVkQVf4o'
        st.video(url)
with col2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        st.write('This is a term....')

coll1, coll2 = st.columns((4,1))
with coll1:
    with st.expander('2차시_ 사진'):
        st.title('사진......')
        imgpath1 = BASE_DIR / "img" / "machinelearning.jpg"
        st.image(str(imgpath1))
with coll2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        imgpath = 'https://i.ytimg.com/vi/MP8R6kBykzE/hqdefault.jpg'
        st.image(imgpath)
        st.write('This is a term....')        

colll1, colll2 = st.columns((4, 1))

with colll1:
    with st.expander('3차시_ 동영상'):
        st.title('머신러닝의 개념')
        
        # --------------------------------------------------
        # 머신러닝의 개념 설명 (개조식)
        # --------------------------------------------------
        st.markdown("""
        ### 📌 머신러닝(Machine Learning)이란?
        - **정의**: 명시적인 프로그래밍 없이 컴퓨터가 데이터로부터 **패턴을 학습**하여 스스로 예측이나 결정을 내리게 하는 인공지능(AI)의 한 분야
        
        ---

        #### 💡 핵심 개념 및 특징
        - **데이터 기반 학습**: 규칙(Rule)을 직접 코딩하는 대신, 대량의 입출력 데이터를 전달하여 모델 스스로 규칙을 발견
        - **일반화(Generalization)**: 학습에 사용되지 않은 새로운 데이터(Unseen Data)에 대해서도 정확한 예측을 수행하는 것이 목표
        - **기존 프로그래밍과의 차이**:
          - `기존 방식`: 데이터 + 규칙 ➔ **결과**
          - `머신러닝`: 데이터 + 결과 ➔ **규칙(모델)**

        ---

        #### ⚙️ 머신러닝의 일반적인 과정
        1. **데이터 수집 및 전처리**: 데이터 정제 및 특성(Feature) 추출
        2. **모델 선택 및 학습**: 알맞은 알고리즘을 선택하여 패턴 학습
        3. **평가 및 최적화**: 성능 지표를 통한 검증 및 하이퍼파라미터 튜닝
        4. **예측 및 배포**: 실전 데이터에 모델 적용
        """)

with colll2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        
        # --------------------------------------------------
        # 머신러닝 하위 개념 (요약 팁)
        # --------------------------------------------------
        st.markdown("""
        💡 **머신러닝 3대 학습 유형**

        **1. 지도학습 (Supervised)**
        - 정답(Label)이 있는 데이터 학습
        - *예: 분류(Classification), 회귀(Regression)*

        **2. 비지도학습 (Unsupervised)**
        - 정답이 없는 데이터의 구조/패턴 탐색
        - *예: 군집화(Clustering), 차원축소*

        **3. 강화학습 (Reinforcement)**
        - 보상(Reward)을 최적화하는 행동 학습
        - *예: 게임 AI, 자율주행*
        """)