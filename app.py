import streamlit as st
import pandas as pd
import os
import subprocess
import sys

# Plotly 자동 설치 및 로드
try:
    import plotly.express as px
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.express as px

# ------------------------ [보안] 비밀번호 확인 ------------------------
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.set_page_config(page_title="SPURS BOARD Login", page_icon="⚽")
        st.title("⚽ COYS! SPURS BOARD")
        st.subheader("스쿼드 명단에 접근하려면 전술 코드를 입력하세요.")
        
        user_pwd = st.text_input("TACTICAL CODE (Password)", type="password")
        if st.button("Access Granted"):
            if user_pwd == "1006": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚨 전술 코드가 일치하지 않습니다.")
        return False
    return True

# ------------------------ 메인 앱 ------------------------
if check_password():
    DB_FILE = "my_total_library.csv"
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["등록일", "책이름", "저자", "출판사", "장르", "메모"])
        df.to_csv(DB_FILE, index=False)

    # 데이터 로드
    library_df = pd.read_csv(DB_FILE)
    total_books = len(library_df)

    st.set_page_config(page_title="Tottenham Hotspur Library", page_icon="⚽", layout="wide")

    # ------------------------ 디자인 CSS (원래 디자인 100% 유지) ------------------------
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    .main { background-color: #f8f9fa; font-family: 'Noto Sans KR', sans-serif; }
    [data-testid="stSidebar"] { background-color: #132257 !important; }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {
        color: white !important; font-weight: 700 !important; font-size: 1.1rem !important;
    }
    .tower-card {
        background: linear-gradient(135deg, #132257 0%, #001c58 100%);
        color: white; padding: 40px; border-radius: 25px;
        text-align: center; box-shadow: 0 15px 30px rgba(19, 34, 87, 0.4); margin-bottom: 30px;
    }
    .tower-card h1 { color: #ffffff; font-size: 110px; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .book-card {
        background: white; padding: 20px; border-radius: 15px; border-left: 10px solid #132257;
        margin-bottom: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # ------------------------ 사이드바 ------------------------
    spurs_logo = "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"
    st.sidebar.image(spurs_logo, width=150)
    st.sidebar.markdown("<h1 style='text-align:center; color:white; font-size:25px;'>SPURS BOARD</h1>", unsafe_allow_html=True)
    st.sidebar.divider()

    menu = st.sidebar.selectbox("📋 전술 메뉴 선택", ["홈/통계", "새 책 등록하기", "내 서재 목록", "서재 관리"])
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style='background-color:rgba(255,255,255,0.1); padding:15px; border-radius:10px; border:1px dashed rgba(255,255,255,0.3);'>
        <p style='margin:0; font-size:14px; color:#ddd;'>TEAM SLOGAN</p>
        <p style='margin:0; font-size:18px; color:white; font-weight:900;'>TO DARE IS TO DO</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------ [메뉴 1] 홈/통계 ------------------------
    if menu == "홈/통계":
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.title("⚽ COYS! 나의 독서 기록")
            book_icons = "📚" * (total_books // 10 + 1)
            st.markdown(f"""
                <div class="tower-card">
                    <p style="letter-spacing: 5px; font-weight:900;">GOALS SCORED</p>
                    <h1>{total_books}</h1>
                    <p style="font-size: 50px; margin:20px 0;">{book_icons}</p>
                </div>
            """, unsafe_allow_html=True)
        with col_t2:
            st.image(spurs_logo, use_container_width=True)

        st.divider()
        st.subheader("📊 포지션별(장르별) 득점 통계")
        if total_books > 0:
            # 그래프 데이터 집계 로직 복구
            genre_counts = library_df['장르'].value_counts().reset_index()
            genre_counts.columns = ['장르', '권수'] # 컬럼명 명확히 지정
            
            fig = px.pie(genre_counts, values='권수', names='장르', hole=0.5,
                         color_discrete_sequence=['#132257', '#DAA520', '#E21A23', '#20B2AA', '#FF8C00', '#4169E1'])
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("책을 등록하면 전술 분석 그래프가 나타납니다!")

    # ------------------------ [메뉴 2] 새 책 등록 ------------------------
    elif menu == "새 책 등록하기":
        st.title("📝 신규 도서 영입")
        with st.form(key='book_form', clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                new_title = st.text_input("📋 책 제목")
                new_author = st.text_input("✍️ 저자")
            with c2:
                new_pub = st.text_input("🏢 출판사")
                new_genre = st.selectbox("🎯 장르", ["소설", "만화", "자기계발", "과학/기술", "인문/사회", "기타"])
            new_memo = st.text_area("🗒️ 스카우팅 리포트 (메모)")
            
            submit_button = st.form_submit_button(label='서재에 스쿼드 등록')
            
            if submit_button:
                if new_title and new_author:
                    new_row = {
                        "등록일": pd.Timestamp.now().strftime("%Y-%m-%d"), 
                        "책이름": new_title, "저자": new_author, 
                        "출판사": new_pub, "장르": new_genre, "메모": new_memo
                    }
                    # 데이터 저장
                    new_df = pd.DataFrame([new_row])
                    library_df = pd.concat([library_df, new_df], ignore_index=True)
                    library_df.to_csv(DB_FILE, index=False)
                    
                    # ✅ 풍선 효과 (성공 메시지 먼저 띄우고 풍선!)
                    st.success(f"⚽ {new_title} 영입 완료!")
                    st.balloons()
                    # 풍선을 보여주기 위해 바로 rerun하지 않고 메시지만 유지
                else:
                    st.error("🚨 제목과 저자는 필수 입력 사항입니다.")

    # ------------------------ [메뉴 3] 내 서재 목록 ------------------------
    elif menu == "내 서재 목록":
        st.title("📋 전체 스쿼드 명단")
        genre_colors = {"소설": "#132257", "자기계발": "#DAA520", "만화": "#E21A23", "과학/기술": "#20B2AA", "인문/사회": "#FF8C00", "기타": "#4169E1"}
        if total_books > 0:
            cols = st.columns(3)
            # 최신순으로 정렬해서 보여주기
            for i, (idx, row) in enumerate(library_df.iloc[::-1].iterrows()):
                card_color = genre_colors.get(row['장르'], "#132257")
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="book-card" style="border-left: 10px solid {card_color};">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <h3 style='margin:0; color:#132257;'>{row['책이름']}</h3>
                                <span style="background-color:{card_color}; color:white; padding:2px 8px; border-radius:5px; font-size:10px; font-weight:bold;">{row['장르']}</span>
                            </div>
                            <p style="margin-top:10px;"><b>저자:</b> {row['저자']}</p>
                            <p style='background:#f0f2f6; padding:10px; border-radius:5px; font-style:italic; min-height:60px;'>"{row['메모']}"</p>
                            <p style="text-align:right; font-size:11px; color:#aaa; margin-top:10px;">SIGNED: {row['등록일']}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("등록된 책이 없습니다.")

    # ------------------------ [메뉴 4] 서재 관리 ------------------------
    elif menu == "서재 관리":
        st.title("⚙️ 스쿼드 방출 관리")
        if total_books > 0:
            target = st.selectbox("방출할 책 선택", library_df['책이름'].tolist())
            if st.button("🚨 이 책 방출하기"):
                library_df = library_df[library_df['책이름'] != target]
                library_df.to_csv(DB_FILE, index=False)
                st.warning(f"✅ {target} 방출 완료.")
                st.rerun()