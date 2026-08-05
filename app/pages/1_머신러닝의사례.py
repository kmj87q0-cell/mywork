import streamlit as st
import streamlit.components.v1 as components
import os
from pathlib import Path

# 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝의 활용 사례",
    page_icon="💡",
    layout="wide"
)

st.title("💡 머신러닝 문제해결 사례")
st.write("직접 개발한 머신러닝 문제해결 사례 보고서/결과물(smartfarm.html)입니다.")

st.markdown("---")

# 1. smartfarm.html 파일 경로 설정
# (기본적으로 app.py가 있는 프로젝트 최상위 폴더에 위치하도록 설정합니다)
BASE_DIR = Path(__file__).resolve().parent.parent
html_file_path = BASE_DIR / "htmls" / "smartfarm.html"

# 2. HTML 파일 읽기 및 iframe 렌더링
if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1024x768 규격 및 상하좌우 스크롤바 허용(scrolling=True)
    components.html(
        html_content,
        width=1024,
        height=768,
        scrolling=True
    )
else:
    st.error(f"❌ '{html_file_path}' 파일을 찾을 수 없습니다.")
    st.warning("프로젝트 최상위 폴더(`app.py`와 같은 위치)에 `preview.html` 파일을 배치해 주세요.")