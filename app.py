import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ===================== 기본 설정 =====================
st.set_page_config(
    page_title="Tottenham Hotspur Library",
    page_icon="⚽",
    layout="wide"
)

DB_FILE = "my_total_library.csv"

# ===================== 장르 & 색상 =====================
GENRES = [
    "소설", "만화", "자기계발", "과학/기술", "인문/사회",
    "수학", "경제", "역사", "철학", "에세이", "기타"
]

GENRE_COLORS = {
    "소설": "#4CAF50", "만화": "#FF9800", "자기계발": "#2196F3",
    "과학/기술": "#9C27B0", "인문/사회": "#3F51B5",
    "수학": "#009688", "경제": "#795548", "역사": "#607D8B",
    "철학": "#673AB7", "에세이": "#E91E63", "기타": "#9E9E9E"
}

SEASONS = ["2025", "2026", "2027"]

def season_top_genre(df, season):
    sdf = df[df["시즌"] == season]
    if sdf.empty:
        return None, 0
    vc = sdf["장르"].value_counts()
    return vc.idxmax(), vc.max()
def season_mvp_book(df, season):
    sdf = df[df["시즌"] == season]
    if sdf.empty:
        return None

    top_genre = sdf["장르"].value_counts().idxmax()
    mvp = sdf[sdf["장르"] == top_genre].iloc[0]

    return mvp
# ===================== 비밀번호 =====================
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False

    if not st.session_state.auth:
        st.title("⚽ COYS! SPURS BOARD")
        pwd = st.text_input("TACTICAL CODE", type="password")
        if st.button("ACCESS"):
            if pwd == "1006":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("전술 코드가 틀렸습니다")
        return False
    return True
st.markdown("""
<style>
/* ===== 메인 배경 ===== */
.main {
    background: linear-gradient(180deg, #f8f9fa 0%, #eef1f7 100%);
}

/* ===== 사이드바 ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10224d, #1b2f6b);
}

/* ===== 섹션 타이틀 ===== */
.section-title {
    padding:12px 24px;
    background:#132257;
    color:white;
    border-radius:30px;
    font-weight:900;
    font-size:28px;
    display:inline-block;
    margin-bottom:20px;
}

/* ===== 타워 카드 ===== */
.tower-card {
    background: linear-gradient(135deg, #132257, #001c58);
    color:white;
    padding:50px;
    border-radius:30px;
    text-align:center;
}

/* ===== 책 카드 ===== */
.book-card {
    background:white;
    padding:18px;
    border-radius:15px;
    margin-bottom:15px;
    border-left:8px solid;
}

/* ===== 사이드바 슬로건 ===== */
.sidebar-slogan {
    text-align:center;
    margin-top:25px;
}
.sidebar-slogan .main {
    font-size:20px;
    font-weight:900;
    color:#9db7ff;
}
.sidebar-slogan .sub {
    font-size:14px;
    letter-spacing:2px;
    color:#dfe6ff;
}

/* ===== 모바일 최적화 ===== */
@media (max-width: 768px) {
    .section-title {
        font-size:20px;
        padding:8px 16px;
    }
    .tower-card {
        padding:25px;
        border-radius:20px;
    }
    .book-card {
        padding:14px;
        font-size:14px;
    }
    [data-testid="column"] {
        width:100% !important;
        flex:1 1 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ===================== 메인 =====================
if check_password():

    # ---------- DB 로드 & 보정 ----------
    if not os.path.exists(DB_FILE):
        pd.DataFrame(columns=[
            "등록일","책이름","저자","출판사","장르","시즌","메모"
        ]).to_csv(DB_FILE, index=False)

# CSV 읽을 때 시즌 컬럼을 문자열로 강제
    library_df = pd.read_csv(DB_FILE, dtype={"시즌": str})

    if "시즌" not in library_df.columns:
        library_df["시즌"] = SEASONS[0]
        library_df.to_csv(DB_FILE, index=False)


    total_books = len(library_df)

    # ---------- 사이드바 ----------
    spurs_logo = "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"
    st.sidebar.image(spurs_logo, width=150)

    st.sidebar.markdown(
        "<h2 style='color:white; text-align:center;'>SPURS BOARD</h2>",
        unsafe_allow_html=True
    )

    menu = st.sidebar.selectbox(
        "MENU",
        ["🏟️ 홈", "📝 신규 영입", "📋 스쿼드", "⚙️ 방출 관리"]
    )

    st.sidebar.markdown("""
    <div class="sidebar-slogan">
        <div class="main">TO DARE IS TO DO</div>
        <div class="sub">NORTH LONDON IS WHITE</div>
    </div>
    """, unsafe_allow_html=True)



    # ===================== 홈 =====================
    if menu == "🏟️ 홈":
        st.markdown("<h1>MATCH DAY</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown(f"""
            <div style="background:#132257;color:white;padding:40px;
                        border-radius:25px;text-align:center;">
                <p>GOALS SCORED</p>
                <h1 style="font-size:70px;">⚽ {total_books}</h1>
            </div>
            """, unsafe_allow_html=True)

            if total_books > 0:
                gc = library_df["장르"].value_counts()
                fig = px.pie(
                    values=gc.values,
                    names=gc.index,
                    color=gc.index,
                    color_discrete_map=GENRE_COLORS,
                    hole=0.5
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.image(spurs_logo, use_container_width=True)

        st.subheader("SEASON STATS")
        scols = st.columns(3)
        for i, s in enumerate(SEASONS):
            g, c = season_top_genre(library_df, s)
            with scols[i]:
                st.metric(f"{s} 시즌", g if g else "없음", f"⚽ {c}")
        st.subheader("🏆 SEASON MVP BOOK")

        mvp_cols = st.columns(3)

        for i, s in enumerate(SEASONS):
            mvp = season_mvp_book(library_df, s)

            with mvp_cols[i]:
                if mvp is None:
                    st.info(f"{s} 시즌 MVP 없음")
                else:
                    st.markdown(f"""
                    <div style="border-left:8px solid {GENRE_COLORS.get(mvp['장르'])};
                            background:white;padding:18px;border-radius:15px;">
                        <b>🏆 {mvp['책이름']}</b><br>
                        <small>{mvp['저자']} · {mvp['장르']}</small><br>
                        <small>시즌 {s}</small>
                    </div>
                    """, unsafe_allow_html=True)

    # ===================== 신규 영입 =====================
    elif menu == "📝 신규 영입":
        with st.form("add", clear_on_submit=True):
            title = st.text_input("책 제목")
            author = st.text_input("저자")
            pub = st.text_input("출판사")
            genre = st.selectbox("장르", GENRES)
            season = st.selectbox("시즌", SEASONS)
            memo = st.text_area("메모")
            ok = st.form_submit_button("영입")


        if ok and title and author:
            new = {
                "등록일": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "책이름": title,
                "저자": author,
                "출판사": pub,
                "장르": genre,
                "시즌": season,
                "메모": memo
            }
            library_df = pd.concat([library_df, pd.DataFrame([new])])
            library_df.to_csv(DB_FILE, index=False)
            st.success(f"⚽ {title} 영입 완료!")
            st.balloons()
             # ⭐ CSV 다시 불러오기 + 시즌 컬럼 문자열로 강제
            library_df = pd.read_csv(DB_FILE, dtype={"시즌": str})
    elif menu == "📋 스쿼드":
        q = st.text_input("🔍 검색")
        df = library_df if q == "" else library_df[library_df["책이름"].str.contains(q)]

        pages = [df.iloc[i:i+12] for i in range(0, len(df), 12)]

        for page in pages:
            cols = st.columns(3)
            for i, (_, r) in enumerate(page.iterrows()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="border-left:8px solid {GENRE_COLORS.get(r['장르'])};
                            background:white;padding:15px;border-radius:12px;">
                    <b>{r['책이름']}</b><br>
                    <small>{r['저자']} · {r['장르']} · {r['시즌']}</small>
                    <p>{r['메모']}</p>
                </div>
                """, unsafe_allow_html=True)


    # ===================== 방출 =====================
    elif menu == "⚙️ 방출 관리":
        for idx, r in library_df.iterrows():
            col1, col2 = st.columns([3,1])

            with col1:
                st.markdown(f"""
                <div style="border-left:8px solid {GENRE_COLORS.get(r['장르'])};
                        background:white;padding:15px;border-radius:12px;">
                <b>{r['책이름']}</b> · {r['장르']}
            </div>
            """, unsafe_allow_html=True)


            if col2.button("방출", key=f"rel{idx}"):
                st.session_state.confirm = idx

            if st.session_state.get("confirm") == idx:
                if col2.button("예", key=f"yes{idx}"):
                    library_df = library_df.drop(idx)
                    library_df.to_csv(DB_FILE, index=False)
                    st.toast(f"🚪 {r['책이름']} 방출 완료", icon="⚽")
                    st.session_state.pop("confirm")
                    st.rerun()
                if col2.button("아니오", key=f"no{idx}"):
                    st.session_state.pop("confirm")