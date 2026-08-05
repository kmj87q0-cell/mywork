import streamlit as st
import sqlite3
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="머신러닝 형성평가", page_icon="📝", layout="wide")

# --------------------------------------------------
# DB 테이블 확인 함수
# --------------------------------------------------
def init_db():
    conn = sqlite3.connect('myproject.db')
    c = conn.cursor()
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

init_db()

st.title("📝 머신러닝 개념 형성평가")

# --------------------------------------------------
# 로그인 확인
# --------------------------------------------------
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("🔒 형성평가 응시 및 기록 저장을 위해 먼저 메인 페이지(app.py) 사이드바에서 **로그인** 해주세요.")
    st.stop()

current_user = st.session_state["user"]
st.info(f"👤 현재 응시자: **{current_user}**님 (여러 번 응시가 가능하며, 결과는 자동 저장됩니다.)")

# --------------------------------------------------
# 10개 문항 데이터 (5지선다형)
# --------------------------------------------------
questions = [
    {
        "id": 1,
        "question": "1. 전통적인 프로그래밍과 머신러닝의 차이점에 대한 설명으로 옳지 않은 것은?",
        "options": [
            "① 전통적 프로그래밍은 규칙과 데이터를 입력하여 결과를 얻는다.",
            "② 머신러닝은 데이터와 정답(결과)을 입력하여 스스로 규칙을 학습한다.",
            "③ 머신러닝은 사람이 직접 모든 조건식(if-else)을 작성할 필요가 없다.",
            "④ 전통적 프로그래밍은 규칙이 바뀔 때마다 사람이 직접 코드를 수정해야 한다.",
            "⑤ 머신러닝은 데이터만 주어지면 항상 100% 완벽한 규칙을 생성하므로 오차가 전혀 없다."
        ],
        "answer_num": 5,
        "hint": "머신러닝 모델이 예측한 결과에는 통계적/확률적 오차가 항상 존재할 수 있습니다.",
        "explanation": "머신러닝 모델은 데이터의 패턴을 학습하는 확률적 모델이므로 항상 100% 완벽할 수는 없으며, 오차가 존재할 수 있습니다."
    },
    {
        "id": 2,
        "question": "2. 지도학습(Supervised Learning)에 대한 설명으로 가장 올바른 것은?",
        "options": [
            "① 정답(라벨)이 없는 데이터만을 사용하여 숨겨진 패턴을 찾는 학습 방식이다.",
            "② 입력 데이터(X)와 함께 정답 라벨(y)이 주어진 상태에서 모델을 학습시킨다.",
            "③ 에이전트가 환경과 상호작용하며 보상(Reward)을 극대화하는 방향으로 학습한다.",
            "④ 대표적인 알고리즘으로 K-평균(K-Means) 군집화가 있다.",
            "⑤ 주로 데이터의 차원을 축소하거나 시각화할 때 사용된다."
        ],
        "answer_num": 2,
        "hint": "선생님이 문제와 함께 '정답'을 지도해주듯 학습하는 방식입니다.",
        "explanation": "지도학습은 입력 데이터와 정답(라벨)을 함께 제공하여 모델이 둘 사이의 관계나 규칙을 배우도록 합니다."
    },
    {
        "id": 3,
        "question": "3. 다음 중 머신러닝의 '분류(Classification)' 문제에 해당하는 예시는?",
        "options": [
            "① 내일의 서울 지역 최고 기온(℃) 예측",
            "② 수신된 이메일이 '스팸 메일'인지 '정상 메일'인지 판별",
            "③ 아파트의 평수와 위치 정보를 기반으로 한 매매 가격 예측",
            "④ 지난달 매출액 데이터를 바탕으로 다음 달 예상 매출액 추정",
            "⑤ 고객의 연령과 소득에 따른 예상 대출 한도 금액 계산"
        ],
        "answer_num": 2,
        "hint": "분류는 범주(Class) 중 하나를 정하는 것이고, 회귀는 연속적인 수치를 예측합니다.",
        "explanation": "이메일을 스팸/정상이라는 그룹으로 정하는 것은 분류 문제이며, 나머지는 연속적인 숫자를 예측하는 회귀 문제입니다."
    },
    {
        "id": 4,
        "question": "4. 비지도학습(Unsupervised Learning)의 대표적인 유형인 '군집화(Clustering)'에 대한 설명으로 옳지 않은 것은?",
        "options": [
            "① 정답 라벨 없이 데이터 간의 유사성을 바탕으로 그룹을 나눈다.",
            "② 구매 이력을 기반으로 유사한 성향의 고객 그룹을 세분화할 때 활용된다.",
            "③ 뉴스 기사를 주제별로 자동 분류/그룹화할 때 사용될 수 있다.",
            "④ 학습 시 미리 정해진 정답 클래스와 비교하여 정확도(Accuracy)를 직접 평가한다.",
            "⑤ 데이터 내의 숨겨진 구조나 패턴을 파악하는 데 유용하다."
        ],
        "answer_num": 4,
        "hint": "비지도학습은 학습 시 정답(라벨)이 주어지지 않는 학습 방법입니다.",
        "explanation": "비지도학습은 정답 라벨이 없으므로 정답과 비교하여 '정확도(Accuracy)'를 직접 측정할 수 없습니다."
    },
    {
        "id": 5,
        "question": "5. 머신러닝의 '강화학습(Reinforcement Learning)'에 등장하는 핵심 요소가 아닌 것은?",
        "options": [
            "① 에이전트 (Agent)",
            "② 환경 (Environment)",
            "③ 보상 (Reward)",
            "④ 지도 라벨 (Target Label)",
            "⑤ 행동 (Action)"
        ],
        "answer_num": 4,
        "hint": "강화학습은 정답을 직접 주는 대신 행동에 따른 '보상'으로 학습합니다.",
        "explanation": "지도 라벨(Target Label)은 지도학습의 핵심 요소입니다."
    },
    {
        "id": 6,
        "question": "6. 모델이 학습 데이터(Train Data)에는 지나치게 잘 맞지만, 새로운 테스트 데이터(Test Data)에서는 성능이 떨어지는 현상은?",
        "options": [
            "① 과소적합 (Underfitting)",
            "② 과적합 (Overfitting)",
            "③ 정규화 (Normalization)",
            "④ 교차 검증 (Cross Validation)",
            "⑤ 특성 공학 (Feature Engineering)"
        ],
        "answer_num": 2,
        "hint": "연습문제의 문제와 답만 달달 외워 응용 시험문제를 틀리는 상태와 같습니다.",
        "explanation": "학습 데이터에 과도하게 맞추어져 일반화 성능이 떨어진 상태를 과적합(Overfitting)이라고 합니다."
    },
    {
        "id": 7,
        "question": "7. 머신러닝 모델 구축 시 데이터를 '학습 데이터'와 '테스트 데이터'로 분할하는 주된 이유는?",
        "options": [
            "① 데이터 크기를 줄여 학습 속도를 높이기 위해",
            "② 메모리 용량이 부족해지는 것을 방지하기 위해",
            "③ 보지 않은 새로운 데이터에 대한 일반화 성능을 객관적으로 평가하기 위해",
            "④ 입력 특성(Feature)의 개수를 줄이기 위해",
            "⑤ 학습 데이터가 있으면 정답 라벨을 지울 수 있기 위해"
        ],
        "answer_num": 3,
        "hint": "학습에 사용한 데이터로만 평가하면 실제 실전 성능을 제대로 알 수 없습니다.",
        "explanation": "학습에 사용되지 않은 평가용 데이터(테스트 데이터)를 통해 일반화 능력을 제대로 측정하기 위함입니다."
    },
    {
        "id": 8,
        "question": "8. 지도학습에서 예측하고자 하는 대상이 되는 '정답 변수'를 일컫는 용어는?",
        "options": [
            "① 특성 (Feature)",
            "② 독립변수 (Independent Variable)",
            "③ 타깃 / 라벨 (Target / Label)",
            "④ 하이퍼파라미터 (Hyperparameter)",
            "⑤ 손실 함수 (Loss Function)"
        ],
        "answer_num": 3,
        "hint": "입력값(X)은 특성(Feature), 맞춰야 하는 정답(y)은 무엇이라 부를까요?",
        "explanation": "예측 대상이 되는 정답을 타깃(Target) 또는 라벨(Label)이라고 합니다."
    },
    {
        "id": 9,
        "question": "9. 분류 모델의 평가 지표 중, 전체 예측 건수 중 올바르게 예측한 건수의 비율은?",
        "options": [
            "① 평균 제곱 오차 (MSE)",
            "② 평균 절대 오차 (MAE)",
            "③ 정확도 (Accuracy)",
            "④ 결정 계수 (R-squared)",
            "⑤ 학습률 (Learning Rate)"
        ],
        "answer_num": 3,
        "hint": "100문제 중 90문제를 맞혔다면 이 값은 90%입니다.",
        "explanation": "전체 예측 중 맞힌 비율을 정확도(Accuracy)라고 합니다."
    },
    {
        "id": 10,
        "question": "10. 사용자가 학습 시작 전에 직접 설정해 주는 매개변수(예: 나무의 최대 깊이, K값 등)는?",
        "options": [
            "① 가중치 (Weight)",
            "② 편향 (Bias)",
            "③ 하이퍼파라미터 (Hyperparameter)",
            "④ 예측값 (Prediction)",
            "⑤ 잔차 (Residual)"
        ],
        "answer_num": 3,
        "hint": "모델이 스스로 배우는 가중치/편향과 달리 사람이 직접 지정해 주는 값입니다.",
        "explanation": "개발자가 직접 설정해주는 매개변수를 하이퍼파라미터(Hyperparameter)라고 합니다."
    }
]

# --------------------------------------------------
# 문제 출력 및 응시 폼
# --------------------------------------------------
user_answers = {}

with st.form("quiz_form"):
    st.subheader("📋 형성평가 문항 (10문항)")
    
    for item in questions:
        q_id = item["id"]
        st.markdown(f"**{item['question']}**")
        
        # 선택지 (1~5번)
        selected_option = st.radio(
            label=f"Q{q_id} 선택",
            options=item["options"],
            key=f"q_{q_id}",
            index=0,
            label_visibility="collapsed"
        )
        
        # 선택한 번호(1~5) 추출 및 저장
        opt_idx = item["options"].index(selected_option) + 1
        user_answers[f"m{q_id}"] = opt_idx
        
        # 💡 힌트 열기/닫기
        with st.expander("💡 힌트 보기"):
            st.info(item["hint"])
            
        # ✅ 정답 및 해설 열기/닫기
        with st.expander("✅ 정답 및 해설 보기"):
            st.success(f"**정답:** {item['options'][item['answer_num'] - 1]}")
            st.write(f"**해설:** {item['explanation']}")
            
        st.markdown("---")

    submitted = st.form_submit_button("💯 형성평가 제출 및 DB 저장", use_container_width=True)

# --------------------------------------------------
# 제출 처리 및 DB 저장
# --------------------------------------------------
if submitted:
    score = 0
    for item in questions:
        q_id = item["id"]
        if user_answers[f"m{q_id}"] == item["answer_num"]:
            score += 10  # 문항당 10점 (만점 100점)

    # DB에 저장
    conn = sqlite3.connect('myproject.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO learning_history (
            userid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        current_user,
        user_answers["m1"], user_answers["m2"], user_answers["m3"], user_answers["m4"], user_answers["m5"],
        user_answers["m6"], user_answers["m7"], user_answers["m8"], user_answers["m9"], user_answers["m10"],
        score
    ))
    conn.commit()
    conn.close()

    st.balloons()
    st.success(f"🎉 **{current_user}**님의 제출이 완료되었습니다!")
    st.metric(label="최종 점수", value=f"{score} / 100점")

# --------------------------------------------------
# 📊 나의 형성평가 응시 기록 (DB 조회)
# --------------------------------------------------
st.markdown("---")
st.subheader(f"📊 {current_user} 님의 형성평가 응시 히스토리 (myproject.db)")

conn = sqlite3.connect('myproject.db')
query = """
    SELECT id AS '응시 번호', score AS '점수', created_at AS '응시 일시',
           m1, m2, m3, m4, m5, m6, m7, m8, m9, m10
    FROM learning_history
    WHERE userid = ?
    ORDER BY created_at DESC
"""
history_df = pd.read_sql_query(query, conn, params=(current_user,))
conn.close()

if not history_df.empty:
    st.dataframe(history_df, use_container_width=True)
else:
    st.write("아직 응시한 기록이 없습니다. 위 문제를 풀고 제출해 보세요!")