import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 레이아웃 및 설정 (전문적인 와이드 모드) ---
st.set_page_config(
    page_title="AI 학교 안전사고 예방 및 대응 시스템",
    page_icon="🏛️",
    layout="wide"
)

# --- 2. CSS 스타일 적용 (전문적인 블루/슬레이트 카드 스타일) ---
st.markdown("""
<style>
    .main {
        background-color: #F8FAFC;
    }
    .report-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
    }
    .report-title {
        color: #1E3A8A;
        margin-top: 0;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 10px;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .section-header {
        color: #2563EB;
        margin-top: 20px;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .shap-box {
        background-color: #F8FAFC;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #2563EB;
        line-height: 1.6;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 타이틀 및 헤더 ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'> 🏛️ AI 기반 학교 안전사고 예방 및 대응 시스템 </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569;'><b>[빅데이터 분석]</b> 학교 안전사고 통계 데이터 및 <b>[머신러닝 모델]</b> LightGBM·CatBoost 앙상블을 활용한 지능형 안전 관리 플랫폼</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 4. 사이드바 (사고 조건 입력부) ---
st.sidebar.markdown("### 🔍 사고 조건 설정")

school_level = st.sidebar.selectbox("🎒 학교급", ["유치원", "초등학교", "중학교", "고등학교", "특수학교"], index=None, placeholder="학교급을 선택하세요")
time_options = ["이론수업", "과학", "실과(기술·가정)", "기타(음악, 미술 등)", "체육", "자유놀이활동시간", "언어활동", "신체활동, 게임", "음악, 미술", "수학, 과학활동", "요리활동", "실외활동(바깥놀이 포함)", "기타 활동시간", "자율활동", "동아리활동", "봉사활동", "진로활동", "체육대회", "경기출전", "현장학습", "수련활동, 수학여행", "학교축제", "기타 특별활동시간", "등교", "하교", "돌봄교실", "방과후과정", "식사시간(간식 포함)", "쉬는시간", "자습시간", "(유치원)특성화활동", "기타 학교체류", "그 밖의 교육활동 시간"]
time = st.sidebar.selectbox("⏰ 사고시간", time_options, index=None, placeholder="사고시간을 선택하세요")

location_options = ["일반(교과)교실", "특별교실(과학실)", "특별교실(과학실 외)", "학습지원공간", "교무실", "행정실/방송실", "기타 관리·행정공간", "강당(체육관)", "운동장", "놀이터", "기타 체육·집회공간", "보건실", "탈의실/샤워실", "화장실", "기타 보건·위생공간", "복도", "계단", "현관", "승강기", "기타 공용공간", "급식실", "기숙사", "기타 교내", "영화관, 공연장", "문화유적지", "전시관, 체험관", "실·내외 체육시설", "어린이 놀이시설", "청소년 수련 시설", "공원, 유원 시설", "기타 문화·체육공간", "교통구역(스쿨존 내)-차도", "교통구역(스쿨존 내)-인도", "교통구역(스쿨존 내)-자전거도로", "교통구역(스쿨존 내)-교통수단 안", "교통구역(스쿨존 내)-기타교통구역", "교통구역(스쿨존 외)-차도", "교통구역(스쿨존 외)-인도", "교통구역(스쿨존 외)-자전거도로", "교통구역(스쿨존 외)-교통수단 안", "교통구역(스쿨존 외)-기타교통구역", "강·바다·하천", "산림·계곡", "기타 자연", "가정", "현장실습/근로지(직업계고)", "숙박시설/식당", "기타 교외"]
location = st.sidebar.selectbox("🏫 사고장소", location_options, index=None, placeholder="사고장소를 선택하세요")

type_options = ["움직이는 물체와의 부딪힘", "고정된 물체와의 부딪힘", "사람과의 부딪힘", "교통사고", "물체 사이에 끼임·눌림", "사람 사이에 끼임·눌림", "넘어짐", "1미터 미만의 높이에서 떨어짐", "1미터 이상의 높이에서 떨어짐", "이동 중 충격을 가함", "스포츠 활동 중 충격을 가함", "물건을 운반하는 중 충격을 가함", "긁힘, 찔림", "베임, 절단", "동물에게 물림(사람 포함)", "곤충·식물 등에 쏘임", "고온의 물체·물질 접촉·흡입·섭취", "일사병, 열사병", "감전", "추위에 장시간 노출", "저온의 물체(드라이아이스 등)·물질 접촉", "화학물질 접촉·흡입·섭취", "익사·익수", "이물질에 의한 질식", "기타 호흡 곤란", "식중독", "이물질 섭취로 인한 질병", "이물질 접촉에 의한 피부염", "그밖의 손상 사고"]
acc_type = st.sidebar.selectbox("💥 사고형태", type_options, index=None, placeholder="사고형태를 선택하세요")

body_part_options = ["두피", "뇌(두개내)", "이마", "눈", "코", "귀", "볼", "턱", "입술 및 구강", "치아", "목구멍", "목", "흉부", "복부", "내장기관", "등", "허리", "어깨", "위팔", "팔꿈치", "아래팔", "손목", "손", "손가락", "골반/엉덩이", "넓적다리(허벅지)", "무릎", "아래다리(종아리)", "발목", "발", "발가락", "기타"]
body_part = st.sidebar.selectbox("🩹 사고부위", body_part_options, index=None, placeholder="사고부위를 선택하세요")

activity_options = ["수업", "자습", "과학실험", "일반실습", "전공실습", "축구", "농구", "배구", "야구", "피구", "족구", "뉴스포츠(구기)", "기타 구기", "배드민턴", "테니스", "탁구", "뉴스포츠(라켓)", "기타 라켓 스포츠", "골프", "볼링", "양궁·사격", "뉴스포츠(타켓형)", "기타 타켓형 스포츠", "인라인/롤러 스케이트", "스케이트 보드", "사이클", "기타 바퀴달린 무동력 스포츠", "달리기", "뜀뛰기", "던지기", "뉴스포츠(던지기)", "장애물", "기타 육상", "태권도", "유도", "합기도", "검도", "펜싱", "레슬링", "씨름", "복싱", "킥복싱", "기타 무도", "수영", "다이빙", "기타 수중 스포츠", "스키·스노우보드", "스케이트", "아이스하키", "기타 설상, 빙상", "리듬·기계체조", "매트운동", "무용(댄스 포함)", "기타 스포츠 활동", "식사", "휴식", "장난, 놀이", "씻기", "수면", "기타 일상활동", "걷기/뛰기, 오르내리기", "(교통수단 등) 운전, 조작, 탑승 중", "싸움", "기타"]
activity = st.sidebar.selectbox("⚽ 사고당시활동", activity_options, index=None, placeholder="사고당시활동을 선택하세요")

run_btn = st.sidebar.button("📊 분석 실행", type="primary")

# --- 5. 메인 화면 출력부 ---
if not school_level or not location or not time or not acc_type or not body_part or not activity:
    st.markdown("<div style='text-align: center; margin-top: 80px; color: #64748B; font-size: 1.1em;'>👈 좌측 사이드바에서 조건을 모두 설정한 후 <b>[분석 실행]</b> 버튼을 클릭해 주세요.</div>", unsafe_allow_html=True)
else:
    if run_btn:
        with st.spinner("AI 모델 분석 수행 중..."):
            
            # [1. 위험등급 예측 로직 연동부]
            try:
                input_data_cls = pd.DataFrame({'학교급': [school_level], '사고장소': [location], '사고시간': [time], '사고형태': [acc_type]})
                for col in ['학교급', '사고장소', '사고시간', '사고형태']:
                    input_data_cls[col] = label_encoders[col].transform(input_data_cls[col].astype(str))
                pred_idx = tuned_lgbm_model.predict(input_data_cls)[0]
                pred_risk_grade = class_name_map[pred_idx]
            except:
                pred_idx = -1
                pred_risk_grade = "분석 불가"

            # [2. 예상 보상금 계산 로직 연동부]
            try:
                input_data_reg = pd.DataFrame({
                    "지역": ["미상"], "학교급": [school_level], "사고자구분": ["미상"], 
                    "사고자학년": ["미상"], "사고자성별": ["미상"], "사고시간": [time], 
                    "사고장소": [location], "사고부위": [body_part], "사고형태": [acc_type], 
                    "사고당시활동": [activity], "데이터연도": [2024]
                })
                for col in categorical_cols:
                    input_data_reg[col] = input_data_reg[col].astype('category')

                lgb_pred = np.expm1(lgb_model.predict(input_data_reg))[0]
                cat_pred = np.expm1(cat_model.predict(input_data_reg))[0]
                expected_comp = max(0, (lgb_pred + cat_pred) / 2)
                comp_str = f"약 {expected_comp:,.0f} 원"
            except:
                comp_str = "산출 불가"

            # [3 & 4. 예방 우선순위 및 빈도 계산]
            combo_key = f"{school_level}-{location}-{time}-{acc_type}"
            try:
                priority_info = prevention_priority[prevention_priority['사고유형'] == combo_key]
                if not priority_info.empty:
                    freq = int(priority_info['X3_Accident_Frequency'].values[0])
                    rank = int(priority_info['순위'].values[0])
                    total_cases = len(prevention_priority)
                    top_percent = (rank / total_cases) * 100
                    priority_str = f"전체 {total_cases}개 유형 중 **{rank}위** (상위 {top_percent:.1f}%)"
                    freq_str = f"{freq}건 발생"
                else:
                    similar_info = prevention_priority[
                        (prevention_priority['사고유형'].str.contains(location)) & 
                        (prevention_priority['사고유형'].str.contains(acc_type))
                    ]
                    if not similar_info.empty:
                        best_similar = similar_info.sort_values(by='X3_Accident_Frequency', ascending=False).iloc[0]
                        freq = int(best_similar['X3_Accident_Frequency'])
                        rank = int(best_similar['순위'])
                        priority_str = f"유사 조건 기준 **{rank}위**"
                        freq_str = f"유사 조건 {freq}건"
                    else:
                        priority_str = "⚠️ **신규 잠재 위험** (선제적 예방 요망)"
                        freq_str = "0건 (과거 5년 이력 없음)"
            except:
                freq_str = "0건"
                priority_str = "분석 오류"

            # [5. SHAP 중요 요인 분석]
            try:
                if pred_idx != -1:
                    instance_shap = explainer.shap_values(input_data_cls)
                    shap_vals = select_class_shap(instance_shap, pred_idx, 1, 4)[0]
                    shap_df = pd.DataFrame({'요인': ['학교급', '사고장소', '사고시간', '사고형태'], '기여도': shap_vals})
                    shap_df['절대기여도'] = shap_df['기여도'].abs()
                    shap_df = shap_df.sort_values('절대기여도', ascending=False)
                    top_factor = shap_df.iloc[0]['요인']
                    
                    shap_desc = f"AI 모델의 SHAP(SHapley Additive exPlanations) 해석 결과, 이번 **'{pred_risk_grade}'** 판정에는 **[{top_factor}]** 요인이 가장 결정적인 기여를 했습니다. 즉, 입력하신 조건 중 {top_factor}의 특성이 해당 사고 위험도를 높인 핵심 원인으로 작용했습니다."
                else:
                    shap_desc = "위험등급 산출이 불가하여 분석을 수행할 수 없습니다."
            except Exception as e:
                shap_desc = "SHAP 분석 로직을 불러올 수 없습니다."

            # [6 & 7. 공식 안전 지침 링크]
            if any(keyword in location or keyword in time or keyword in activity for keyword in ['체육', '운동', '스포츠', '구기', '육상']):
                guideline_link = "🏃‍♂️ [체육활동 안전수칙 가이드 다운로드 (클릭)](https://www.schoolsafe.kr/)"
            elif any(keyword in location or keyword in time or keyword in activity for keyword in ['실험', '과학']):
                guideline_link = "🧪 [과학실험실 안전수칙 가이드 다운로드 (클릭)](https://www.schoolsafe.kr/)"
            else:
                guideline_link = "📚 [학교생활 일반 안전수칙 가이드 다운로드 (클릭)](https://www.schoolsafe.kr/)"

        # --- 6. 전문적인 카드 리포트 화면 렌더링 (수정본) ---
        html_content = f"""
        <div class="report-card">
            <h3 class="report-title"> 📊 [{school_level}] {location} - {time} 사고 분석 종합 리포트 </h3>
            
            <h4 class="section-header"> 📌 1. 핵심 예측 지표 </h4>
            <ul style="line-height: 1.8;">
                <li> 🔴 <b>AI 예측 위험등급 :</b> <code>{pred_risk_grade}</code> </li>
                <li> 💰 <b>예상 보상금 산출액 :</b> <code>{comp_str}</code> </li>
                <li> 📈 <b>과거 사고 빈도 :</b> 과거 5년간 <code>{freq_str}</code> </li>
                <li> 🏆 <b>CRITIC-TOPSIS 예방 우선순위 :</b> {priority_str} </li>
            </ul>

            <h4 class="section-header"> 🔍 2. 머신러닝 모델 해석 (SHAP) </h4>
            <div class="shap-box"> {shap_desc} </div>

            <h4 class="section-header"> 💡 3. 현장 맞춤형 예방 가이드 (Action Item) </h4>
            <ul style="line-height: 1.8;">
                <li> 🛠️ <b>환경 통제 :</b> [{location}] 구역의 위험 요소를 점검하고, 사고 발생 시 <b>[{body_part}]</b> 부위의 충격을 완화할 안전 인프라 보강 </li>
                <li> ⏱️ <b>시간 및 활동 통제 :</b> [{time}] 시간대 <b>[{activity}]</b> 활동 시 안전 지도 인력 최소 2명 이상 집중 배치 </li>
                <li> 📢 <b>행동 통제 :</b> [{acc_type}] 유형 사고 예방을 위한 대상별 시청각 안전 교육 실시 </li>
            </ul>

            <h4 class="section-header"> 🔗 4. 공식 안전 지침 및 매뉴얼 </h4>
            {guideline_link}
            <br><br>
            <p style="color: #64748B; font-size: 0.85em; margin-top: 20px; text-align: right;"> ℹ️ 본 리포트는 학교 안전사고 빅데이터 및 머신러닝 예측 모델을 기반으로 산출되었습니다. </p>
        </div>
        """
        
        # 💡 핵심: unsafe_allow_html=True를 꼭 붙여주어야 HTML 태그가 정상 적용됩니다!
        st.markdown(html_content, unsafe_allow_html=True)
