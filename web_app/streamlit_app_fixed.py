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

# Завантаження моделей
@st.cache_resource
def load_models():
    models = {}
    try:
        # Використовуємо поточну директорію замість /home/claude/
        base_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        
        models['af'] = joblib.load(os.path.join(base_path, 'model_af.pkl'))
        models['aki'] = joblib.load(os.path.join(base_path, 'model_aki.pkl'))
        models['lco'] = joblib.load(os.path.join(base_path, 'model_lco.pkl'))
        models['bleeding'] = joblib.load(os.path.join(base_path, 'model_bleeding.pkl'))
        models['stroke'] = joblib.load(os.path.join(base_path, 'model_stroke.pkl'))
        return models
    except Exception as e:
        st.error(f"Помилка завантаження моделей: {e}")
        st.warning("Переконайтесь, що всі .pkl файли знаходяться в тій же папці, що й streamlit_app.py")
        return None

models = load_models()

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
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .high-risk {
        background-color: #FEE2E2;
        border-left: 5px solid #DC2626;
    }
    .medium-risk {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
    }
    .low-risk {
        background-color: #D1FAE5;
        border-left: 5px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown('<h1 class="main-header">❤️ ICU Digital Twin</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6B7280; font-size: 1.2rem;">Прогнозування післяопераційних ускладнень на основі Machine Learning</p>', unsafe_allow_html=True)
st.markdown("---")

# Сайдбар з інформацією
with st.sidebar:
    st.markdown("### 📊 Про систему")
    st.info("""
    **ICU Digital Twin** використовує Random Forest моделі для прогнозування:
    - 🔴 Фібриляція передсердь
    - 💧 Гостре пошкодження нирок
    - 💔 Низький серцевий викид
    - 🩸 Кровотеча
    - 🧠 Інсульт
    
    **Модель навчена на 1000 пацієнтів**
    """)
    
    st.markdown("### ⚙️ Налаштування")
    show_probabilities = st.checkbox("Показати ймовірності", value=True)
    show_feature_importance = st.checkbox("Показати важливість факторів", value=False)
    
    st.markdown("---")
    st.caption("Demo v2.0 | БУС-18, 2026")
    st.caption("© Професор Мазур А.П.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Введення даних", "📊 Результати прогнозу", "ℹ️ Інформація"])

with tab1:
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
        ejection_fraction = st.slider("Фракція викиду (%)", min_value=15, max_value=80, value=42, step=1)
        creatinine = st.number_input("Креатинін (мкмоль/л)", min_value=40, max_value=500, value=125, step=5)
        hemoglobin = st.number_input("Гемоглобін (г/л)", min_value=60, max_value=200, value=138, step=5)
        glucose = st.number_input("Глюкоза (ммоль/л)", min_value=3.0, max_value=20.0, value=8.2, step=0.1)
    
    with col3:
        st.markdown("#### Супутні захворювання")
        diabetes = st.checkbox("Цукровий діабет", value=True)
        hypertension = st.checkbox("Артеріальна гіпертензія", value=True)
        ihd = st.checkbox("ІХС", value=True)
        ckd_stage = st.select_slider("ХХН стадія", options=[0, 1, 2, 3, 4, 5], value=3)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("#### Операція")
        surgery_type = st.selectbox(
            "Тип операції",
            ["АКШ", "Заміна клапана", "Аорта", "Комбінована"]
        )
        cpb_duration = st.number_input("Очікувана тривалість ШК (хв)", min_value=30, max_value=300, value=90, step=5)
    
    with col5:
        st.markdown("#### Додатково")
        if surgery_type == "АКШ":
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
    if models and calculate_button:
        st.markdown("### 📊 Прогноз післяопераційних ускладнень")
        
        # Підготовка даних для моделі
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
        
        # Прогнозування
        predictions = {}
        for complication, model in models.items():
            proba = model.predict_proba(patient_data)[0][1] * 100
            predictions[complication] = proba
        
        # Функція для визначення рівня ризику
        def get_risk_level(risk):
            if risk >= 60:
                return "🔴 Високий ризик", "high-risk", "#DC2626"
            elif risk >= 30:
                return "🟡 Помірний ризик", "medium-risk", "#F59E0B"
            else:
                return "🟢 Низький ризик", "low-risk", "#10B981"
        
        # Рекомендації
        recommendations = {
            'af': {
                'high': [
                    "Аміодарон 200 мг per os x2 за 24 год до операції",
                    "Продовжити бета-блокатор до операції",
                    "ЕКГ моніторинг безперервний 72 години",
                    "Контроль електролітів: K+ >4.0, Mg2+ >1.0 ммоль/л",
                    "Уникати гіпотермії (<36°C)"
                ],
                'medium': [
                    "ЕКГ моніторинг 48 годин",
                    "Контроль електролітів щодоби",
                    "Продовжити бета-блокатор"
                ],
                'low': ["Стандартний протокол", "ЕКГ моніторинг 24 години"]
            },
            'aki': {
                'high': [
                    "Оптимізація перфузії: MAP ≥65 мм рт.ст., СІ >2.4 л/хв/м²",
                    "Уникати нефротоксичних препаратів (НПЗП, аміноглікозіди)",
                    "Моніторинг креатиніну кожні 12 годин",
                    "Адекватна гідратація (уникати гіповолемії)",
                    "Розглянути N-ацетилцистеїн 600 мг x2"
                ],
                'medium': [
                    "Моніторинг креатиніну щодоби",
                    "Підтримка адекватної перфузії",
                    "Уникати нефротоксинів"
                ],
                'low': ["Стандартний моніторинг", "Контроль креатиніну на 1, 3, 7 добу"]
            },
            'lco': {
                'high': [
                    "Норадреналін готовий (0.03-0.05 мкг/кг/хв)",
                    "Адреналін готовий (0.02-0.05 мкг/кг/хв)",
                    "Інвазивний моніторинг серцевого викиду",
                    "Повільна індукція анестезії",
                    "ІАВК готова (розглянути превентивну установку)",
                    "ЕхоКГ інтраопераційна обов'язкова"
                ],
                'medium': [
                    "Інотропна підтримка готова",
                    "Моніторинг ScvO2",
                    "ЕхоКГ за показаннями"
                ],
                'low': ["Стандартний протокол", "Інотропи готові"]
            },
            'bleeding': {
                'high': [
                    "Cell Saver обов'язково",
                    "Транексамова кислота: болюс 1г + інфузія 1г/год",
                    "Тромбоеластографія/ROTEM",
                    "Компоненти крові готові (ЕМ 4, ТМ 4, СЗП 4)",
                    "Хірургічна техніка: мінімізувати травматизацію"
                ],
                'medium': [
                    "Транексамова кислота 1г болюс",
                    "Компоненти крові готові",
                    "Cell Saver за показаннями"
                ],
                'low': ["Стандартний протокол", "Транексамова кислота 1г"]
            },
            'stroke': {
                'high': [
                    "ЕхоКГ аорти на атеросклероз",
                    "No-touch техніка канюляції аорти",
                    "Ретроградна перфузія мозку (за показаннями)",
                    "Строгий контроль глікемії (6-10 ммоль/л)",
                    "Неврологічний огляд щодоби 7 діб"
                ],
                'medium': [
                    "ЕхоКГ аорти",
                    "Контроль глікемії",
                    "Неврологічний огляд"
                ],
                'low': ["Стандартний протокол"]
            }
        }
        
        # Відображення результатів
        complications_info = {
            'af': ('⚡ Фібриляція передсердь', 'af'),
            'aki': ('💧 Гостре пошкодження нирок', 'aki'),
            'lco': ('💔 Низький серцевий викид', 'lco'),
            'bleeding': ('🩸 Кровотеча (ревізія)', 'bleeding'),
            'stroke': ('🧠 Інсульт', 'stroke')
        }
        
        for comp_id, (comp_name, comp_key) in complications_info.items():
            risk = predictions[comp_id]
            risk_text, risk_class, risk_color = get_risk_level(risk)
            
            with st.container():
                st.markdown(f'<div class="metric-card {risk_class}">', unsafe_allow_html=True)
                
                col_a, col_b = st.columns([2, 3])
                
                with col_a:
                    st.markdown(f"### {comp_name}")
                    st.markdown(f"<h2 style='color: {risk_color}; margin: 0;'>{risk_text}: {risk:.0f}%</h2>", unsafe_allow_html=True)
                    
                    # Gauge chart
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
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 60
                                }
                            }
                        ))
                        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                
                with col_b:
                    st.markdown("#### 📋 Рекомендації:")
                    
                    if risk >= 60:
                        recs = recommendations[comp_key]['high']
                    elif risk >= 30:
                        recs = recommendations[comp_key]['medium']
                    else:
                        recs = recommendations[comp_key]['low']
                    
                    for rec in recs:
                        st.markdown(f"- {rec}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("")
        
        # Загальна інформація
        st.markdown("---")
        st.info("""
        ℹ️ **Важлива інформація:**
        - Прогнози базуються на Random Forest моделях, натренованих на 1000 пацієнтів
        - Точність моделей: AF (72%), AKI (65%), LCO (80%), Кровотеча (64%), Інсульт (52%)
        - Завжди використовуйте клінічне мислення та індивідуальний підхід
        - AI - це інструмент допомоги, не замінник лікаря
        - Рекомендації базуються на актуальних клінічних настановах (ACC/AHA, EACTS)
        """)
        
        # Експорт результатів
        st.markdown("---")
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            # Підготовка тексту звіту
            report_text = f"""
ICU DIGITAL TWIN - ЗВІТ ПРОГНОЗУ
================================

Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

ДАНІ ПАЦІЄНТА:
- Вік: {age} років
- ФВ: {ejection_fraction}%
- Креатинін: {creatinine} мкмоль/л
- Операція: {surgery_type}

ПРОГНОЗ УСКЛАДНЕНЬ:
- Фібриляція передсердь: {predictions['af']:.0f}% {get_risk_level(predictions['af'])[0]}
- Гостре пошкодження нирок: {predictions['aki']:.0f}% {get_risk_level(predictions['aki'])[0]}
- Низький серцевий викид: {predictions['lco']:.0f}% {get_risk_level(predictions['lco'])[0]}
- Кровотеча: {predictions['bleeding']:.0f}% {get_risk_level(predictions['bleeding'])[0]}
- Інсульт: {predictions['stroke']:.0f}% {get_risk_level(predictions['stroke'])[0]}

Demo v2.0 | БУС-18, 2026
"""
            
            st.download_button(
                label="📄 Завантажити звіт (TXT)",
                data=report_text,
                file_name=f"digital_twin_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    elif not calculate_button:
        st.info("👈 Введіть дані пацієнта та натисніть 'Розрахувати ризики'")
    else:
        st.error("Помилка завантаження моделей. Перевірте, чи файли моделей (.pkl) знаходяться в тій же папці, що й streamlit_app.py")

with tab3:
    st.markdown("### ℹ️ Про ICU Digital Twin")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        #### 🤖 Machine Learning моделі
        
        Система використовує **Random Forest** моделі для прогнозування п'яти основних післяопераційних ускладнень:
        
        1. **Фібриляція передсердь (AF)** - AUC: 0.72
        2. **Гостре пошкодження нирок (AKI)** - AUC: 0.65
        3. **Низький серцевий викид (LCO)** - AUC: 0.80
        4. **Кровотеча** - AUC: 0.64
        5. **Інсульт** - AUC: 0.52
        
        **Навчальний датасет:** 1000 пацієнтів кардіохірургічного профілю
        
        **Особливості:**
        - 12 предикторів (вік, ФВ, лабораторія, супутні захворювання)
        - Автоматичний балансування класів
        - Валідація на тестовій вибірці (20%)
        """)
    
    with col_info2:
        st.markdown("""
        #### 📊 Ключові предиктори
        
        **Фібриляція передсердь:**
        - Фракція викиду (найважливіший)
        - Вік пацієнта
        - Тривалість штучного кровообігу
        
        **Гостре пошкодження нирок:**
        - Креатинін (найважливіший)
        - Фракція викиду
        - Тривалість ШК
        
        **Низький серцевий викид:**
        - Фракція викиду (найважливіший)
        - Тривалість ШК
        - Гемоглобін
        
        **Кровотеча:**
        - Гемоглобін
        - Креатинін
        - Глюкоза
        
        **Інсульт:**
        - Вік
        - Креатинін
        - Тривалість ШК
        """)
    
    st.markdown("---")
    st.markdown("""
    #### ⚠️ Обмеження та застереження
    
    - ❌ **НЕ є** медичним обладнанням або діагностичним пристроєм
    - ❌ **НЕ замінює** клінічне мислення лікаря
    - ❌ **НЕ гарантує** 100% точності прогнозів
    - ✅ **Є** інструментом підтримки прийняття рішень
    - ✅ **Допомагає** ідентифікувати пацієнтів високого ризику
    - ✅ **Базується** на актуальних клінічних настановах
    
    #### 📚 Джерела та посилання
    
    - ACC/AHA Guidelines for Cardiac Surgery (2023)
    - EACTS Guidelines for Postoperative Care (2024)
    - Halpern et al. (2024) - Digital twins in critical care
    - Guo W. (2025) - DT-ICU: Explainable Digital Twins
    
    #### 👨‍⚕️ Автор
    
    **Професор Мазур Андрій Петрович**  
    д.мед.н., професор кафедри анестезіології та інтенсивної терапії
    
    **Британо-Український Симпозіум (БУС-18), 2026**
    """)
    
    st.success("""
    💡 **Для майстер-класу:** Ця демо-версія створена для навчальних цілей. 
    Для реального клінічного використання потрібна валідація на незалежній вибірці 
    та отримання відповідних дозволів.
    """)

# Footer
st.markdown("---")
st.caption("ICU Digital Twin Demo v2.0 with ML | БУС-18, 2026 | © Професор Мазур А.П.")
