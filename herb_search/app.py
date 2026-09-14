import pandas as pd
import streamlit as st
from pathlib import Path


# ==========================================
# 페이지 설정
# ==========================================

st.set_page_config(
    page_title="국내 생약 검색 시스템",
    page_icon="🌿",
    layout="wide"
)


# ==========================================
# Excel 데이터 불러오기
# ==========================================

@st.cache_data
def load_data():

    base_dir = Path(__file__).resolve().parent

    file_path = base_dir / "herb_data.xlsx"

    df = pd.read_excel(file_path)

    return df


df = load_data()


# ==========================================
# 검색 함수
# ==========================================

def search_column(data, column, query):

    result = data[
        data[column]
        .fillna("")
        .astype(str)
        .str.contains(
            query,
            case=False,
            na=False
        )
    ]

    return result


# ==========================================
# 웹 화면
# ==========================================

st.title("🌿 국내 생약 검색 시스템")

st.write(
    "국내 생산 생약 데이터베이스에서 "
    "생약명, 성분, 약효, 질병 및 분포지역을 검색합니다."
)

st.divider()


# ==========================================
# 검색 유형 선택
# ==========================================

search_options = {

    "생약명": "국명",

    "영문명": "TCM_name_en (영문명)",

    "학명": "Herb_latin_name (학명)",

    "성분": "성분",

    "약효": "Function (약효)",

    "질병": "Indication (질병)",

    "분포지역": "분포지역"
}


search_type = st.selectbox(
    "검색 유형을 선택하세요",
    list(search_options.keys())
)


# ==========================================
# 검색어 입력
# ==========================================

query = st.text_input(
    "검색어를 입력하세요",
    placeholder="예: eleutheroside"
)


# ==========================================
# 검색 실행
# ==========================================

if st.button("검색", type="primary"):

    if query.strip() == "":

        st.warning("검색어를 입력해주세요.")

    else:

        column = search_options[search_type]

        result = search_column(
            df,
            column,
            query
        )

        if result.empty:

            st.warning("검색 결과가 없습니다.")

        else:

            st.success(
                f"검색 결과: {len(result)}건"
            )

            columns_to_show = [

                "국명",

                "TCM_name_en (영문명)",

                "Herb_latin_name (학명)",

                "Function (약효)",

                "Indication (질병)",

                "분포지역",

                "성분"
            ]

            st.dataframe(
                result[columns_to_show],
                use_container_width=True,
                hide_index=True
            )