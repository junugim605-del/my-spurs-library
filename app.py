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

from supabase import create_client, Client

# Supabase 연결 설정 (비밀 금고 secrets.toml에서 정보를 가져옴)
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)
import hashlib

# 비밀번호 암호화 전술
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
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
# 팀별 커스텀 세팅 (자료 모으는 대로 여기만 업데이트하면 끝!)
TEAM_CONFIG = {
    "Tottenham": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
        "main_color": "#132257",
        "accent_color": "#ffffff",
        "slogan": "TO DARE IS TO DO",
        "sub_slogan": "NORTH LONDON IS WHITE"
    },
    "Liverpool": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
        "main_color": "#C8102E",
        "accent_color": "#f6eb61",
        "slogan": "YOU'LL NEVER WALK ALONE",
        "sub_slogan": "THIS IS ANFIELD"
    },
    "Arsenal": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
        "main_color": "#EF0107",
        "accent_color": "#ffffff",
        "slogan": "VICTORIA CONCORDIA CRESCIT",
        "sub_slogan": "NORTH LONDON IS RED"
    },
    "Man City": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
        "main_color": "#6CABDD",
        "accent_color": "#ffffff",
        "slogan": "CITY TILL I DIE",
        "sub_slogan": "BLUE MOON RISING"
    },
    "Man United": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
        "main_color": "#DA291C",
        "accent_color": "#FBE122",
        "slogan": "GLORY GLORY MAN UNITED",
        "sub_slogan": "THE RED DEVILS"
    },
    "Chelsea": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
        "main_color": "#034694",
        "accent_color": "#ffffff",
        "slogan": "KEEP THE BLUE FLAG FLYING HIGH",
        "sub_slogan": "PRIDE OF LONDON"
    },
    "Aston Villa": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282024%29.svg",
        "main_color": "#670E36",
        "accent_color": "#95BFE5",
        "slogan": "PREPARED",
        "sub_slogan": "VILLANS"
    },
    "Newcastle": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
        "main_color": "#241F20",
        "accent_color": "#ffffff",
        "slogan": "HOWAY THE LADS",
        "sub_slogan": "THE MAGPIES"
    },
    "Brighton": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        "main_color": "#0057B8",
        "accent_color": "#ffffff",
        "slogan": "SEAGULLS",
        "sub_slogan": "SUSSEX BY THE SEA"
    },
    "West Ham": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        "main_color": "#7A263A",
        "accent_color": "#1BB1E7",
        "slogan": "I'M FOREVER BLOWING BUBBLES",
        "sub_slogan": "THE HAMMERS"
    },
    "Wolves": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        "main_color": "#FDB913",
        "accent_color": "#231F20",
        "slogan": "OUT OF DARKNESS COMETH LIGHT",
        "sub_slogan": "WOLVES"
    },
    "Fulham": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/3/3f/Fulham_FC_%28shield%29.svg",
        "main_color": "#ffffff",
        "accent_color": "#000000",
        "slogan": "FFC",
        "sub_slogan": "THE COTTAGERS"
    },
    "Bournemouth": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg",
        "main_color": "#DA291C",
        "accent_color": "#000000",
        "slogan": "TOGETHER, ANYTHING IS POSSIBLE",
        "sub_slogan": "THE CHERRIES"
    },
    "Crystal Palace": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg",
        "main_color": "#1B458F",
        "accent_color": "#C4122E",
        "slogan": "SOUTH LONDON & PROUD",
        "sub_slogan": "THE EAGLES"
    },
    "Brentford": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        "main_color": "#E30613",
        "accent_color": "#ffffff",
        "slogan": "BEE TOGETHER",
        "sub_slogan": "THE BEES"
    },
    "Everton": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        "main_color": "#003399",
        "accent_color": "#ffffff",
        "slogan": "NIL SATIS NISI OPTIMUM",
        "sub_slogan": "THE TOFFEES"
    },
    "Leicester": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        "main_color": "#003090",
        "accent_color": "#FDBE11",
        "slogan": "FOXES NEVER QUIT",
        "sub_slogan": "FEARLESS"
    },
    "Ipswich": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg",
        "main_color": "#0033FF",
        "accent_color": "#ffffff",
        "slogan": "THE TRACTOR BOYS",
        "sub_slogan": "ITFC"
    },
    "Southampton": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/c/c9/Southampton_FC.svg",
        "main_color": "#D71920",
        "accent_color": "#ffffff",
        "slogan": "MARCHING IN",
        "sub_slogan": "THE SAINTS"
    },
    "Nott'm Forest": {
        "logo": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg",
        "main_color": "#DD0000",
        "accent_color": "#ffffff",
        "slogan": "YOU REDS",
        "sub_slogan": "FOREST"
    }
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
# ===================== 비밀번호 (DB 로그인 전술) =====================
def check_password():
    if st.session_state.get("auth"):
        return True

    st.title("⚽ CLUB MEMBERSHIP")
# 기존 st.title("⚽ CLUB MEMBERSHIP") 바로 아래에 붙여넣으세요!
    tab1, tab2, tab3 = st.tabs(["🔒 로그인", "📝 회원가입", "🔍 아이디/비번 찾기"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            epl_logo = "https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg"
            st.image(epl_logo, width=150)
        with col2:
            input_id = st.text_input("USER ID (아이디)", key="login_id")
            input_pw = st.text_input("PASSWORD (비밀번호)", type="password", key="login_pw")
            login_btn = st.button("LOGIN")

    with tab2:
        st.subheader("📝 신규 구단주 입단 신청")
        with st.form("signup_form"):
            new_id = st.text_input("사용할 아이디")
            new_pw = st.text_input("비밀번호", type="password")
            new_email = st.text_input("이메일 (아이디 찾기용)")
            new_hint = st.text_input("질문: 가장 좋아하는 선수 이름은? (비번 찾기용)")
            new_team = st.selectbox("응원 구단 선택", list(TEAM_CONFIG.keys()))
            
            if st.form_submit_button("입단 계약서 서명"):
                # 중복 아이디 체크
                check = supabase.table("users").select("username").eq("username", new_id).execute()
                if check.data:
                    st.error("이미 리그에 등록된 아이디입니다.")
                else:
                    # 비밀번호 해시(암호화)해서 저장!
                    supabase.table("users").insert({
                        "username": new_id, 
                        "password": hash_password(new_pw), # 이 함수는 맨 위에 만드셔야 해요!
                        "email": new_email,
                        "hint_answer": new_hint,
                        "team_name": new_team
                    }).execute()
                    st.success("입단 완료! 로그인 탭으로 이동해서 로그인해주세요.")

    with tab3:
        st.subheader("🔍 계정 정보 찾기")
        find_mode = st.radio("찾기 모드", ["아이디 찾기", "비밀번호 확인"])
        if find_mode == "아이디 찾기":
            f_email = st.text_input("가입 시 등록한 이메일 입력")
            if st.button("아이디 찾기"):
                res = supabase.table("users").select("username").eq("email", f_email).execute()
                if res.data:
                    st.info(f"찾으시는 아이디는 [{res.data[0]['username']}] 입니다.")
                else:
                    st.error("등록된 정보가 없습니다.")
        else:
            f_id = st.text_input("아이디 입력")
            f_hint = st.text_input("답변: 좋아하는 선수 이름은?")
            if st.button("정보 일치 확인"):
                # 비번은 암호화되어 있어서 본인도 못 보게 하는 게 보안의 정석입니다. 일치 여부만 확인!
                res = supabase.table("users").select("*").eq("username", f_id).eq("hint_answer", f_hint).execute()
                if res.data:
                    st.success("정보가 일치합니다! 로그인을 진행해주세요.")
                else:
                    st.error("정보가 일치하지 않습니다.")

    # --- 여기서부터 다시 기존 if login_btn: 로직이 시작됩니다 ---
    if login_btn:
        try:
            # Supabase에서 유저 정보 확인
            response = supabase.table("users").select("*")\
                .eq("username", input_id)\
                .eq("password", hash_password(input_pw))\
                .execute()

# (기존 코드 74라인 부근 수정)
            if response.data:
                st.session_state.auth = True
                st.session_state.user_id = response.data[0]['username']
                # ⭐ 이 줄을 꼭 추가해야 팀 정보가 저장됩니다!
                st.session_state.user_team = response.data[0].get('team_name', 'Tottenham') 
                st.success(f"✅ {st.session_state.user_id} 구단주님, 환영합니다!")
                st.rerun()
            else:
                st.error("🚫 아이디 또는 비밀번호가 틀렸습니다!")
        except Exception as e:
            st.error(f"⚠️ 로그인 서버 확인 필요: {e}")
            
    return False
    return True
# ===================== 메인 =====================
if check_password():
    # DB 작업 하기 바로 직전에 이 쿼리를 먼저 날려줘야 RLS를 통과합니다!
    supabase.rpc("set_config", {"setting": "app.current_username", "value": st.session_state.user_id}).execute()
    # 1. 팀 정보 가져오기 (이건 그대로 유지!)
    user_team = st.session_state.get("user_team", "Tottenham")
    config = TEAM_CONFIG.get(user_team, TEAM_CONFIG["Tottenham"])
    current_logo = config["logo"]

    # 2. 여기서부터 디자인 코드를 통째로 교체! (업그레이드 버전)
    st.markdown(f"""
    <style>
    /* 메인 배경 (팀 컬러 살짝 반영) */
    .stApp {{
        background: linear-gradient(180deg, #f8f9fa 0%, {config['main_color']}10 100%);
    }}

    /* 사이드바 (팀 컬러 그라데이션) */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {config['main_color']}, #000000) !important;
    }}

    /* 섹션 타이틀 (팀 컬러 반영) */
    .section-title {{
        padding:12px 24px;
        background: {config['main_color']} !important;
        color: {config['accent_color']} !important;
        border-radius:30px;
        font-weight:900;
        font-size:28px;
        display:inline-block;
        margin-bottom:20px;
    }}

    /* 버튼 색상 강제 변경 */
    div.stButton > button:first-child {{
        background-color: {config['main_color']} !important;
        color: {config['accent_color']} !important;
        border-radius: 20px;
        border: none;
    }}

    /* 타워 카드 (전광판) */
    .tower-card {{
        background: linear-gradient(135deg, {config['main_color']}, #000000);
        color: {config['accent_color']};
        padding:50px;
        border-radius:30px;
        text-align:center;
    }}

    /* 모바일 최적화 (반응형) */
    @media (max-width: 768px) {{
        .section-title {{ font-size:20px; padding:8px 16px; }}
        .tower-card {{ padding:25px; border-radius:20px; }}
        [data-testid="column"] {{ width:100% !important; flex:1 1 100% !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # 3. 이후 DB 로드 로직 시작...
    try:
        response = supabase.table("books").select("*").eq("username", st.session_state.user_id).execute()
        # ... (이하 기존 코드 그대로)
        
        if response.data:
            # 가져온 데이터를 판다스 데이터프레임으로 변환
            library_df = pd.DataFrame(response.data)
            
            # DB의 영어 컬럼명을 앱에서 사용하는 한글 이름으로 변환 (매핑 작업)
            library_df = library_df.rename(columns={
                "title": "책이름", 
                "author": "저자", 
                "publisher": "출판사",
                "genre": "장르", 
                "season": "시즌", 
                "memo": "메모", 
                "registered_at": "등록일"
            })
        else:
            # DB가 텅 비어있을 때 (첫 실행 시)
            library_df = pd.DataFrame(columns=["등록일","책이름","저자","출판사","장르","시즌","메모"])
            
    except Exception as e:
        st.error(f"DB 연결 중 부상 발생(에러): {e}")
        library_df = pd.DataFrame(columns=["등록일","책이름","저자","출판사","장르","시즌","메모"])

    # 시즌 컬럼 문자열 강제 (기존 로직 유지)
    library_df["시즌"] = library_df["시즌"].astype(str)
    total_books = len(library_df)
# ---------- 사이드바 (팀별 로고 & 제목 자동 변경) ----------
    # (기존 spurs_logo 선언문은 지우고 이걸 넣으세요)
    st.sidebar.image(current_logo, width=150) 

    st.sidebar.markdown(
        f"<h2 style='color:{config['accent_color']}; text-align:center;'>{user_team.upper()} BOARD</h2>",
        unsafe_allow_html=True
    )

    menu = st.sidebar.selectbox(
        "MENU",
        ["🏟️ 홈", "📝 신규 영입", "📋 스쿼드", "⚙️ 방출 관리"]
    )

# 슬로건도 팀별로 다르게 하고 싶다면 나중에 수정 가능!
    st.sidebar.markdown(f"""
    <div class="sidebar-slogan">
        <div class="main" style="color:{config['accent_color']};">{config.get('slogan', 'TO DARE IS TO DO')}</div>
        <div class="sub" style="color:{config['accent_color']}cc;">{config.get('sub_slogan', user_team.upper() + ' LIBRARY')}</div>
    </div>
    """, unsafe_allow_html=True)
# 사이드바 하단에 로그아웃 버튼 배치
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 전술 후퇴 (로그아웃)"):
        st.session_state.auth = False
        st.session_state.user_id = None
        st.rerun()
    # ===================== 홈 (메인 화면 박스 색상 수정) =====================
    if menu == "🏟️ 홈":
        st.markdown(f"<h1 style='color:{config['main_color']};'>MATCH DAY</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,1])

        with col1:
            # ⭐ 여기 background 색상을 config['main_color']로 바꿨습니다!
            st.markdown(f"""
            <div style="background:{config['main_color']};color:{config['accent_color']};padding:40px;
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
            # ⭐ 여기도 spurs_logo 대신 current_logo로!
            st.image(current_logo, use_container_width=True)

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
            # DB에 넣을 데이터 정리 (영어 컬럼명 주의!)
# 수정 후 (username을 꼭 넣어주세요!)
            new_book = {
                "registered_at": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "title": title,
                "author": author,
                "publisher": pub,
                "genre": genre,
                "season": str(season),
                "username": st.session_state.user_id,  # ⭐ 이 줄 추가! 누가 영입했는지 기록
                "memo": memo
            }
            # Supabase DB로 전송!
            try:
                supabase.table("books").insert(new_book).execute()
                st.success(f"⚽ {title} 영입 완료!")
                st.balloons()
                st.rerun()  # <--- 'ㅇ' 지우고 깔끔하게!
            except Exception as e:
                st.error(f"영입 실패: {e}")

            # 이 밑에 있던 library_df = pd.read_csv... 줄은 삭제됐어야 함!
             # ⭐ CSV 다시 불러오기 + 시즌 컬럼 문자열로 강제
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


# ===================== 방출 관리 (Supabase 전용) =====================
    elif menu == "⚙️ 방출 관리":
        st.subheader("🗑️ 방출 대상 선수 명단")
        
        # 만약 명단이 비어있다면?
        if library_df.empty:
            st.info("방출할 선수가 없습니다. 먼저 영입해 주세요!")
        else:
            for idx, r in library_df.iterrows():
                col1, col2 = st.columns([3, 1])

                with col1:
                    # 장르별 색상은 그대로 유지!
                    genre_color = GENRE_COLORS.get(r['장르'], "#ccc")
                    st.markdown(f"""
                        <div style="border-left:8px solid {genre_color};
                                    background:white;padding:15px;border-radius:12px;margin-bottom:10px;box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                            <b style="font-size:1.1em;">{r['책이름']}</b> · <span style="color:gray;">{r['장르']}</span>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    # 원터치 방출 버튼 (id값을 직접 사용해서 DB 타겟팅!)
                    # ⚠️ r['id']가 실제 Supabase의 id 컬럼 값이어야 합니다.
                    if st.button("방출", key=f"del_{r['id']}"):
                        try:
                            # 🔍 Supabase 서버에 방출 명령 전달
                            supabase.table("books").delete().eq("id", r['id']).execute()
                            
                            st.toast(f"🚪 {r['책이름']} 방출 완료!", icon="⚽")
                            st.rerun()  # 즉시 명단 업데이트
                        except Exception as e:
                            st.error(f"방출 실패: {e}")