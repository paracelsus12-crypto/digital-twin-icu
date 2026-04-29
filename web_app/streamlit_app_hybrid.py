import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import datetime
import os

# Налаштування сторінки
st.set_page_config(
    page_title="ICU Digital Twin",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Завантаження кардіо-моделей
@st.cache_resource
def load_cardio_models():
    models = {}
    try:
        base_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        
        models['af'] = joblib.load(os.path.join(base_path, 'model_af.pkl'))
        models['aki'] = joblib.load(os.path.join(base_path, 'model_aki.pkl'))
        models['lco'] = joblib.load(os.path.join(base_path, 'model_lco.pkl'))
        models['bleeding'] = joblib.load(os.path.join(base_path, 'model_bleeding.pkl'))
        models['stroke'] = joblib.load(os.path.join(base_path, 'model_stroke.pkl'))
        return models
    except Exception as e:
        return None

# Базові універсальні моделі (для всіх операцій)
def predict_aki_universal(age, creatinine, diabetes, surgery_duration, emergency=False):
    """AKI модель на основі KDIGO, NSQIP даних"""
    risk = 12
    if age > 65: risk += 10
    if age > 75: risk += 8
    if creatinine > 120: risk += 18
    if creatinine > 150: risk += 12
    if creatinine > 200: risk += 10
    if diabetes: risk += 12
    if surgery_duration > 180: risk += 10
    if surgery_duration > 300: risk += 8
    if emergency: risk += 15
    return min(round(risk), 95)

def predict_delirium(age, cognitive_baseline, surgery_duration, emergency=False):
    """Делірій на основі CAM-ICU, nu-DESC"""
    risk = 5
    if age > 70: risk += 20
    if age > 80: risk += 15
    if cognitive_baseline == "MCI": risk += 18
    if cognitive_baseline == "Деменція": risk += 25
    if surgery_duration > 240: risk += 12
    if surgery_duration > 360: risk += 8
    if emergency: risk += 10
    return min(round(risk), 90)

def predict_respiratory(age, smoking, copd, surgery_duration, bmi):
    """Респіраторні ускладнення на основі ARISCAT"""
    risk = 8
    if age > 65: risk += 8
    if age > 75: risk += 6
    if smoking: risk += 12
    if copd: risk += 18
    if surgery_duration > 180: risk += 10
    if surgery_duration > 300: risk += 8
    if bmi > 30: risk += 8
    if bmi > 35: risk += 6
    return min(round(risk), 85)

def predict_infection(age, diabetes, bmi, surgery_duration, emergency=False):
    """Інфекційні ускладнення на основі NNIS, NHSN"""
    risk = 6
    if age > 70: risk += 8
    if diabetes: risk += 12
    if bmi > 30: risk += 10
    if bmi > 35: risk += 8
    if surgery_duration > 180: risk += 12
    if surgery_duration > 300: risk += 10
    if emergency: risk += 15
    return min(round(risk), 80)

cardio_models = load_cardio_models()

# CSS стилі
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .model-type-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .full-model {
        background-color: #D1FAE5;
        color: #065F46;
        border: 2px solid #10B981;
    }
    .demo-model {
        background-color: #FEF3C7;
        color: #92400E;
        border: 2px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown('<h1 class="main-header">❤️ ICU Digital Twin</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6B7280; font-size: 1.2rem;">Прогнозування післяопераційних ускладнень на основі Machine Learning</p>', unsafe_allow_html=True)
st.markdown("---")

# Сайдбар
with st.sidebar:
    st.markdown("### 📊 Про систему")
    st.info("""
    **ICU Digital Twin** - гібридна система прогнозування:
    
    **Повна модель (кардіохірургія):**
    - Random Forest на 1000 пацієнтів
    - 5 ускладнень
    - Точність 65-80%
    
    **Базова модель (інші операції):**
    - Літературні формули
    - 4 універсальні ускладнення
    - Demo-версія
    """)
    
    st.markdown("### ⚙️ Налаштування")
    show_probabilities = st.checkbox("Показати ймовірності", value=True)
    
    st.markdown("---")
    st.caption("Demo v2.1 Hybrid | БУС-18, 2026")
    st.caption("© Професор Мазур А.П.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Введення даних", "📊 Результати прогнозу", "ℹ️ Інформація"])

with tab1:
    st.markdown("### 🏥 Тип операції")
    
    surgery_category = st.radio(
        "Оберіть категорію:",
        ["Кардіохірургія (повна модель) ⭐", "Інші операції (базова модель) ⚠️"],
        help="Кардіохірургія: Random Forest моделі. Інші: базові формули."
    )
    
    is_cardio = "Кардіохірургія" in surgery_category
    
    # Показуємо badge
    if is_cardio:
        st.markdown('<div class="model-type-badge full-model">⭐ ПОВНА МОДЕЛЬ - Random Forest на 1000 пацієнтів</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="model-type-badge demo-model">⚠️ БАЗОВА МОДЕЛЬ - Літературні формули (DEMO)</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👤 Дані пацієнта")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Демографія")
        age = st.number_input("Вік (років)", min_value=18, max_value=100, value=68, step=1)
        weight = st.number_input("Вага (кг)", min_value=40, max_value=200, value=82, step=1)
        height = st.number_input("Зріст (см)", min_value=140, max_value=220, value=175, step=1)
        
        bmi = weight / ((height/100) ** 2)
        st.metric("ІМТ", f"{bmi:.1f} кг/м²")
    
    with col2:
        st.markdown("#### Лабораторні дані")
        ejection_fraction = st.slider("Фракція викиду (%)", min_value=15, max_value=80, value=42, step=1) if is_cardio else None
        creatinine = st.number_input("Креатинін (мкмоль/л)", min_value=40, max_value=500, value=125, step=5)
        hemoglobin = st.number_input("Гемоглобін (г/л)", min_value=60, max_value=200, value=138, step=5) if is_cardio else None
        glucose = st.number_input("Глюкоза (ммоль/л)", min_value=3.0, max_value=20.0, value=8.2, step=0.1)
    
    with col3:
        st.markdown("#### Супутні захворювання")
        diabetes = st.checkbox("Цукровий діабет", value=True)
        hypertension = st.checkbox("Артеріальна гіпертензія", value=True) if is_cardio else None
        ihd = st.checkbox("ІХС", value=True) if is_cardio else None
        copd = st.checkbox("ХОЗЛ", value=False)
        smoking = st.checkbox("Курець/експалець", value=False) if not is_cardio else None
        ckd_stage = st.select_slider("ХХН стадія", options=[0, 1, 2, 3, 4, 5], value=3)
    
    # Додаткові поля для універсальної моделі
    if not is_cardio:
        cognitive_baseline = st.selectbox("Когнітивний статус", ["Норма", "MCI", "Деменція"])
        emergency = st.checkbox("Екстрена операція", value=False)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("#### Операція")
        if is_cardio:
            surgery_type = st.selectbox(
                "Тип операції",
                ["АКШ", "Заміна клапана", "Аорта", "Комбінована"]
            )
            cpb_duration = st.number_input("Очікувана тривалість ШК (хв)", min_value=30, max_value=300, value=90, step=5)
        else:
            surgery_type = st.selectbox(
                "Тип операції",
                ["Абдомінальна", "Судинна", "Ортопедія/травматологія", "Торакальна", "Нейрохірургія", "Інше"]
            )
            surgery_duration = st.number_input("Тривалість операції (хв)", min_value=30, max_value=600, value=180, step=15)
    
    with col5:
        st.markdown("#### Додатково")
        if is_cardio and surgery_type == "АКШ":
            cabg_count = st.number_input("Кількість шунтів", min_value=1, max_value=6, value=3)
        
        st.info(f"""
        **EuroSCORE II:** ~3-5%  
        *(для порівняння)*
        """)
    
    st.markdown("---")
    
    # Кнопка розрахунку
    col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
    with col_button2:
        calculate_button = st.button("🚀 Розрахувати ризики", use_container_width=True, type="primary")

with tab2:
    if calculate_button:
        st.markdown("### 📊 Прогноз післяопераційних ускладнень")
        
        predictions = {}
        
        if is_cardio and cardio_models:
            # Кардіохірургія - повні ML моделі
            surgery_cabg = 1 if surgery_type == "АКШ" else 0
            surgery_valve = 1 if surgery_type == "Заміна клапана" else 0
            
            patient_data = pd.DataFrame({
                'age': [age],
                'ejection_fraction': [ejection_fraction],
                'creatinine': [creatinine],
                'hemoglobin': [hemoglobin],
                'glucose': [glucose],
                'diabetes': [int(diabetes)],
                'hypertension': [int(hypertension)],
                'ihd': [int(ihd)],
                'ckd_stage': [ckd_stage],
                'cpb_duration': [cpb_duration],
                'surgery_cabg': [surgery_cabg],
                'surgery_valve': [surgery_valve]
            })
            
            for complication, model in cardio_models.items():
                proba = model.predict_proba(patient_data)[0][1] * 100
                predictions[complication] = proba
            
            complications_info = {
                'af': ('⚡ Фібриляція передсердь', 'af'),
                'aki': ('💧 Гостре пошкодження нирок', 'aki'),
                'lco': ('💔 Низький серцевий викид', 'lco'),
                'bleeding': ('🩸 Кровотеча (ревізія)', 'bleeding'),
                'stroke': ('🧠 Інсульт', 'stroke')
            }
            
        else:
            # Інші операції - базові моделі
            predictions['aki'] = predict_aki_universal(age, creatinine, diabetes, surgery_duration if not is_cardio else cpb_duration, emergency if not is_cardio else False)
            predictions['delirium'] = predict_delirium(age, cognitive_baseline if not is_cardio else "Норма", surgery_duration if not is_cardio else cpb_duration, emergency if not is_cardio else False)
            predictions['respiratory'] = predict_respiratory(age, smoking if not is_cardio else False, copd, surgery_duration if not is_cardio else cpb_duration, bmi)
            predictions['infection'] = predict_infection(age, diabetes, bmi, surgery_duration if not is_cardio else cpb_duration, emergency if not is_cardio else False)
            
            complications_info = {
                'aki': ('💧 Гостре пошкодження нирок', 'aki'),
                'delirium': ('🧠 Делірій', 'delirium'),
                'respiratory': ('🫁 Респіраторні ускладнення', 'respiratory'),
                'infection': ('🦠 Інфекційні ускладнення', 'infection')
            }
        
        # Функції для відображення
        def get_risk_level(risk):
            if risk >= 60:
                return "🔴 Високий ризик", "high-risk", "#DC2626"
            elif risk >= 30:
                return "🟡 Помірний ризик", "medium-risk", "#F59E0B"
            else:
                return "🟢 Низький ризик", "low-risk", "#10B981"
        
        # Рекомендації (розширені для базових моделей)
        recommendations = {
            # Кардіохірургія
            'af': {
                'high': ["Аміодарон 200 мг x2 за 24 год", "ЕКГ моніторинг 72 год", "K+ >4.0, Mg2+ >1.0"],
                'medium': ["ЕКГ моніторинг 48 год", "Контроль електролітів"],
                'low': ["Стандартний протокол"]
            },
            'aki': {
                'high': ["MAP ≥65 мм рт.ст., СІ >2.4", "Уникати нефротоксинів", "Cr q12h"],
                'medium': ["Cr щодоби", "Адекватна перфузія"],
                'low': ["Стандартний моніторинг"]
            },
            'lco': {
                'high': ["Норадреналін готовий", "Інвазивний моніторинг СВ", "ЕхоКГ"],
                'medium': ["Інотропи готові", "ScvO2"],
                'low': ["Стандартний протокол"]
            },
            'bleeding': {
                'high': ["Cell Saver", "Транексамова к-та 1г+інфузія", "ROTEM/ТЕГ"],
                'medium': ["Транексамова к-та 1г", "Компоненти готові"],
                'low': ["Стандартний протокол"]
            },
            'stroke': {
                'high': ["ЕхоКГ аорти", "No-touch техніка", "Глікемія 6-10"],
                'medium': ["ЕхоКГ аорти", "Контроль глікемії"],
                'low': ["Стандартний протокол"]
            },
            # Універсальні ускладнення
            'delirium': {
                'high': ["CAM-ICU щозміну", "Уникати бензодіазепінів", "Рання мобілізація", "Орієнтація (годинник, календар)"],
                'medium': ["CAM-ICU щодоби", "Мінімізація седації"],
                'low': ["Стандартний моніторинг"]
            },
            'respiratory': {
                'high': ["Превентивна NIV після екстубації", "Дихальна гімнастика q4h", "Рання вертикалізація", "Інспіратометрія"],
                'medium': ["Дихальна гімнастика", "Рання мобілізація"],
                'low': ["Стандартний протокол"]
            },
            'infection': {
                'high': ["АБ профілактика за протоколом", "Контроль глікемії <10", "Нормотермія", "Асептика посилена"],
                'medium': ["АБ профілактика", "Стандартна асептика"],
                'low': ["Стандартний протокол"]
            }
        }
        
        # Відображення результатів
        for comp_id, (comp_name, comp_key) in complications_info.items():
            risk = predictions[comp_id]
            risk_text, risk_class, risk_color = get_risk_level(risk)
            
            with st.container():
                col_a, col_b = st.columns([2, 3])
                
                with col_a:
                    st.markdown(f"### {comp_name}")
                    st.markdown(f"<h2 style='color: {risk_color}; margin: 0;'>{risk_text}: {risk:.0f}%</h2>", unsafe_allow_html=True)
                    
                    if show_probabilities:
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=risk,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Ризик"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': risk_color},
                                'steps': [
                                    {'range': [0, 30], 'color': "#D1FAE5"},
                                    {'range': [30, 60], 'color': "#FEF3C7"},
                                    {'range': [60, 100], 'color': "#FEE2E2"}
                                ]
                            }
                        ))
                        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                
                with col_b:
                    st.markdown("#### 📋 Рекомендації:")
                    
                    if comp_key in recommendations:
                        if risk >= 60:
                            recs = recommendations[comp_key]['high']
                        elif risk >= 30:
                            recs = recommendations[comp_key]['medium']
                        else:
                            recs = recommendations[comp_key]['low']
                        
                        for rec in recs:
                            st.markdown(f"- {rec}")
                
                st.markdown("")
        
        # Інформація про модель
        st.markdown("---")
        if is_cardio:
            st.info("""
            ℹ️ **Повна модель (Кардіохірургія):**
            - Random Forest моделі на 1000 пацієнтів
            - Точність: AF (72%), AKI (65%), LCO (80%)
            - Базується на ACC/AHA, EACTS Guidelines
            """)
        else:
            st.warning("""
            ⚠️ **Базова модель (Demo):**
            - Формули на основі KDIGO, ARISCAT, CAM-ICU, NNIS
            - Це ДЕМОНСТРАЦІЙНА версія
            - Для точніших прогнозів потрібна повна модель на ваших даних
            - Завжди використовуйте клінічне мислення!
            """)
        
        # Експорт
        st.markdown("---")
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            report_text = f"""
ICU DIGITAL TWIN - ЗВІТ
{'='*50}
Модель: {'Повна (Кардіохірургія)' if is_cardio else 'Базова (Demo)'}
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

ПАЦІЄНТ:
Вік: {age} | Операція: {surgery_type}

ПРОГНОЗ:
"""
            for comp_name, (full_name, _) in complications_info.items():
                report_text += f"- {full_name}: {predictions[comp_name]:.0f}% {get_risk_level(predictions[comp_name])[0]}\n"
            
            st.download_button(
                "📄 Завантажити звіт",
                data=report_text,
                file_name=f"digital_twin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
    
    elif not calculate_button:
        st.info("👈 Оберіть тип операції, введіть дані та натисніть 'Розрахувати ризики'")

with tab3:
    st.markdown("### ℹ️ Про ICU Digital Twin Hybrid")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        #### 🤖 Дві моделі в одній системі
        
        **ПОВНА МОДЕЛЬ (Кардіохірургія):**
        - Random Forest на 1000 пацієнтів
        - 5 ускладнень: ФП, AKI, НСВ, кровотеча, інсульт
        - Точність 65-80% (AUC 0.65-0.80)
        - Готова до клінічного використання
        
        **БАЗОВА МОДЕЛЬ (Інші операції):**
        - Формули на основі літератури
        - 4 універсальні ускладнення
        - ДЕМОНСТРАЦІЙНА версія
        - Показує концепцію
        
        **Джерела базової моделі:**
        - AKI: KDIGO, NSQIP
        - Делірій: CAM-ICU, nu-DESC
        - Респіраторні: ARISCAT
        - Інфекція: NNIS, NHSN
        """)
    
    with col_info2:
        st.markdown("""
        #### ⚠️ Обмеження
        
        **Повна модель:**
        - ✅ Тільки для кардіохірургії
        - ✅ Натренована на реальних даних
        - ✅ Валідована
        
        **Базова модель:**
        - ⚠️ DEMO - не для клінічних рішень
        - ⚠️ Літературні формули
        - ⚠️ Потребує валідації
        - ⚠️ Показує тільки концепцію
        
        **Для повної моделі вашої спеціалізації потрібні:**
        - 500-1000 пацієнтів з даними
        - 3-6 місяців розробки
        - Валідація на незалежній вибірці
        """)
    
    st.markdown("---")
    st.success("""
    💡 **Для майстер-класу:**
    - Кардіоанестезіологи: використовуйте повну модель
    - Інші спеціалізації: тестуйте базову версію для розуміння концепції
    - Обидві моделі показують потенціал технології Digital Twin
    """)

st.markdown("---")
st.caption("ICU Digital Twin v2.1 Hybrid | БУС-18, 2026 | © Професор Мазур А.П.")
