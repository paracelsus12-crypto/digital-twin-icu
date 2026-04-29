import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import datetime
import os
import json

# Налаштування
st.set_page_config(
    page_title="ICU Digital Twin - Full",
    page_icon="❤️",
    layout="wide"
)

# Завантаження моделей
@st.cache_resource
def load_all_models():
# Завантаження моделей
@st.cache_resource
def load_all_models():
    models = {}
    # Отримуємо шлях до web_app папки
    if '__file__' in globals():
        base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        base_path = os.getcwd()
    
    # Шлях до моделей: ../models/
    models_path = os.path.join(base_path, '..', 'models')
    
    surgery_types = {
        'cardiac': ['aki', 'delirium', 'respiratory', 'infection', 'af', 'lco', 'stroke'],
        'abdominal': ['aki', 'delirium', 'respiratory', 'infection', 'anastomotic_leak', 'ileus', 'vte'],
        'vascular': ['aki', 'delirium', 'respiratory', 'infection', 'thrombosis', 'amputation'],
        'orthopedic': ['aki', 'delirium', 'respiratory', 'infection', 'vte', 'pji'],
        'thoracic': ['aki', 'delirium', 'respiratory', 'infection', 'air_leak', 'atelectasis']
    }
    
    for surgery_type, complications in surgery_types.items():
        models[surgery_type] = {}
        surgery_path = os.path.join(models_path, surgery_type)
        
        for comp in complications:
            try:
                # Спочатку пробуємо v3 (з VTE для абдомінальної)
                model_file = f'model_{surgery_type}_{comp}_v3.pkl'
                model_path = os.path.join(surgery_path, model_file)
                
                if not os.path.exists(model_path):
                    # Якщо немає v3, пробуємо v2 (зі статтю)
                    model_file = f'model_{surgery_type}_{comp}_v2.pkl'
                    model_path = os.path.join(surgery_path, model_file)
                
                if not os.path.exists(model_path):
                    # Якщо немає v2, пробуємо v1 (стару версію)
                    model_file = f'model_{surgery_type}_{comp}.pkl'
                    model_path = os.path.join(surgery_path, model_file)
                
                if os.path.exists(model_path):
                    models[surgery_type][comp] = joblib.load(model_path)
                else:
                    st.warning(f"Модель {surgery_type}/{comp} не знайдена по шляху {model_path}")
                    models[surgery_type][comp] = None
            except Exception as e:
                st.error(f"Помилка завантаження {surgery_type}/{comp}: {str(e)}")
                models[surgery_type][comp] = None
    
    return models

            except:
                models[surgery_type][comp] = None
    
    return models

all_models = load_all_models()

# CSS
st.markdown("""
<style>
.main-header {font-size: 2.5rem; color: #1E3A8A; text-align: center; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">❤️ ICU Digital Twin - Повна Версія</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">ML-прогнозування для всіх типів операцій</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Про систему")
    st.success("**32 ML моделі** для 5 типів операцій")
    st.markdown("---")
    st.caption("v3.0 | БУС-18, 2026")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📝 Введення даних", "📊 Результати", "ℹ️ Інформація"])

with tab1:
    st.markdown("### 🏥 Оберіть тип операції")
    
    surgery_type = st.selectbox(
        "Тип хірургічного втручання:",
        ["cardiac", "abdominal", "vascular", "orthopedic", "thoracic"],
        format_func=lambda x: {
            'cardiac': '❤️ Кардіохірургія (АКШ, клапани, аорта)',
            'abdominal': '🏥 Абдомінальна (резекції, холецистектомія)',
            'vascular': '🩸 Судинна (реваскуляризація, ендоваскулярні)',
            'orthopedic': '🦴 Ортопедія/травматологія (ендопротезування)',
            'thoracic': '🫁 Торакальна (резекції легені)'
        }[x]
    )
    
    st.markdown("---")
    st.markdown("### 👤 Дані пацієнта")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Демографія")
        age = st.number_input("Вік (років)", 18, 100, 68)
        
        # Перевіряємо чи є моделі v2 (зі статтю)
        has_sex_models = False
        if surgery_type and all_models.get(surgery_type):
            # Перевіряємо чи завантажились v2 моделі
            sample_model = list(all_models[surgery_type].values())[0]
            if sample_model and hasattr(sample_model, 'feature_names_in_'):
                has_sex_models = 'sex' in sample_model.feature_names_in_
        
        if has_sex_models:
            sex = st.radio("Стать", ["Жінка", "Чоловік"], index=1, horizontal=True)
            sex_male = 1 if sex == "Чоловік" else 0
        else:
            sex_male = None
            st.info("ℹ️ Для використання фактору 'Стать' завантажте моделі v2")
        
        weight = st.number_input("Вага (кг)", 40, 200, 82)
        height = st.number_input("Зріст (см)", 140, 220, 175)
        bmi = weight / ((height/100) ** 2)
        st.metric("ІМТ", f"{bmi:.1f}")
    
    with col2:
        st.markdown("#### Лабораторні")
        creatinine = st.number_input("Креатинін (мкмоль/л)", 40, 500, 125)
        hemoglobin = st.number_input("Гемоглобін (г/л)", 60, 200, 138)
        glucose = st.number_input("Глюкоза (ммоль/л)", 3.0, 20.0, 6.5, 0.1)
        
        if surgery_type == 'cardiac':
            ejection_fraction = st.slider("ФВ (%)", 15, 80, 42)
        
        if surgery_type == 'abdominal':
            albumin = st.number_input("Альбумін (г/л)", 20, 50, 38)
        
        if surgery_type == 'thoracic':
            fev1_percent = st.slider("ОФВ1 (%)", 25, 100, 70)
    
    with col3:
        st.markdown("#### Супутні")
        diabetes = st.checkbox("Цукровий діабет")
        hypertension = st.checkbox("Гіпертензія")
        copd = st.checkbox("ХОЗЛ")
        smoking = st.checkbox("Курець/експалець")
        ckd_stage = st.select_slider("ХХН стадія", [0,1,2,3,4,5], 0)
        asa_class = st.select_slider("ASA", [2,3,4], 3)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("#### Операція")
        
        if surgery_type == 'cardiac':
            surgery_subtype = st.selectbox("Тип", ["АКШ", "Заміна клапана", "Аорта"])
            cpb_duration = st.number_input("ШК (хв)", 30, 300, 90)
            surgery_duration = cpb_duration + 40
            surgery_cabg = 1 if surgery_subtype == "АКШ" else 0
            surgery_valve = 1 if "клапан" in surgery_subtype else 0
            ihd = st.checkbox("ІХС", value=True)
            
        elif surgery_type == 'abdominal':
            surgery_subtype = st.selectbox("Тип", ["Резекція кишки", "Холецистектомія", "Інше"])
            surgery_duration = st.number_input("Тривалість (хв)", 60, 420, 180)
            laparoscopic = st.checkbox("Лапароскопічна", value=True)
            oncology = st.checkbox("Онкологія")
            emergency = st.checkbox("Екстрена")
            
        elif surgery_type == 'vascular':
            surgery_subtype = st.selectbox("Тип", ["Реваскуляризація", "Ендоваскулярна", "Інше"])
            surgery_duration = st.number_input("Тривалість (хв)", 60, 360, 150)
            peripheral_artery_disease = st.checkbox("ХОЗАНК", value=True)
            critical_limb_ischemia = st.checkbox("Критична ішемія")
            emergency = st.checkbox("Екстрена")
            anticoagulants = st.checkbox("Антикоагулянти")
            
        elif surgery_type == 'orthopedic':
            surgery_subtype = st.selectbox("Тип", ["Ендопротезування", "Остеосинтез", "Інше"])
            surgery_duration = st.number_input("Тривалість (хв)", 45, 300, 120)
            joint_replacement = st.checkbox("Заміна суглоба", value=True)
            trauma = st.checkbox("Травма")
            anticoagulant_prophylaxis = st.checkbox("АК профілактика", value=True)
            
        elif surgery_type == 'thoracic':
            surgery_subtype = st.selectbox("Тип", ["Резекція легені", "Плевректомія", "Інше"])
            surgery_duration = st.number_input("Тривалість (хв)", 90, 420, 200)
            oncology = st.checkbox("Онкологія", value=True)
            vats = st.checkbox("VATS (відеоасистована)")
    
    with col5:
        st.markdown("#### Додатково")
        st.info(f"Тривалість: {surgery_duration} хв")
    
    st.markdown("---")
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        calc_btn = st.button("🚀 Розрахувати ризики", use_container_width=True, type="primary")

with tab2:
    if calc_btn:
        st.markdown("### 📊 Прогноз післяопераційних ускладнень")
        
        # Підготовка даних - ТОЧНИЙ ПОРЯДОК ЯК У ТРЕНУВАЛЬНИХ ДАНИХ!
        if surgery_type == 'cardiac':
            patient_data = {
                'age': age,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'creatinine': creatinine,
                'hemoglobin': hemoglobin,
                'glucose': glucose,
                'diabetes': int(diabetes),
                'hypertension': int(hypertension),
                'ckd_stage': ckd_stage,
                'copd': int(copd),
                'smoking': int(smoking),
                'asa_class': asa_class,
                'ejection_fraction': ejection_fraction,
                'ihd': int(ihd),
                'cpb_duration': cpb_duration,
                'surgery_cabg': surgery_cabg,
                'surgery_valve': surgery_valve,
                'surgery_duration': surgery_duration
            }
            # Додаємо sex тільки якщо є
            if sex_male is not None:
                patient_data = {
                    'age': age,
                    'sex': sex_male,
                    'weight': weight,
                    'height': height,
                    'bmi': bmi,
                    'creatinine': creatinine,
                    'hemoglobin': hemoglobin,
                    'glucose': glucose,
                    'diabetes': int(diabetes),
                    'hypertension': int(hypertension),
                    'ckd_stage': ckd_stage,
                    'copd': int(copd),
                    'smoking': int(smoking),
                    'asa_class': asa_class,
                    'ejection_fraction': ejection_fraction,
                    'ihd': int(ihd),
                    'cpb_duration': cpb_duration,
                    'surgery_cabg': surgery_cabg,
                    'surgery_valve': surgery_valve,
                    'surgery_duration': surgery_duration
                }
        elif surgery_type == 'abdominal':
            patient_data = {
                'age': age,
                'sex': sex_male,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'creatinine': creatinine,
                'hemoglobin': hemoglobin,
                'glucose': glucose,
                'diabetes': int(diabetes),
                'hypertension': int(hypertension),
                'ckd_stage': ckd_stage,
                'copd': int(copd),
                'smoking': int(smoking),
                'asa_class': asa_class,
                'albumin': albumin,
                'emergency': int(emergency),
                'laparoscopic': int(laparoscopic),
                'surgery_duration': surgery_duration,
                'oncology': int(oncology)
            }
        elif surgery_type == 'vascular':
            patient_data = {
                'age': age,
                'sex': sex_male,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'creatinine': creatinine,
                'hemoglobin': hemoglobin,
                'glucose': glucose,
                'diabetes': int(diabetes),
                'hypertension': int(hypertension),
                'ckd_stage': ckd_stage,
                'copd': int(copd),
                'smoking': int(smoking),
                'asa_class': asa_class,
                'peripheral_artery_disease': int(peripheral_artery_disease),
                'anticoagulants': int(anticoagulants),
                'emergency': int(emergency),
                'surgery_duration': surgery_duration,
                'critical_limb_ischemia': int(critical_limb_ischemia)
            }
        elif surgery_type == 'orthopedic':
            patient_data = {
                'age': age,
                'sex': sex_male,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'creatinine': creatinine,
                'hemoglobin': hemoglobin,
                'glucose': glucose,
                'diabetes': int(diabetes),
                'hypertension': int(hypertension),
                'ckd_stage': ckd_stage,
                'copd': int(copd),
                'smoking': int(smoking),
                'asa_class': asa_class,
                'joint_replacement': int(joint_replacement),
                'trauma': int(trauma),
                'surgery_duration': surgery_duration,
                'anticoagulant_prophylaxis': int(anticoagulant_prophylaxis)
            }
        elif surgery_type == 'thoracic':
            patient_data = {
                'age': age,
                'sex': sex_male,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'creatinine': creatinine,
                'hemoglobin': hemoglobin,
                'glucose': glucose,
                'diabetes': int(diabetes),
                'hypertension': int(hypertension),
                'ckd_stage': ckd_stage,
                'copd': int(copd),
                'smoking': int(smoking),
                'asa_class': asa_class,
                'fev1_percent': fev1_percent,
                'oncology': int(oncology),
                'surgery_duration': surgery_duration,
                'vats': int(vats)
            }
        
        df = pd.DataFrame([patient_data])
        
        # Прогнозування
        predictions = {}
        models = all_models[surgery_type]
        
        for comp_name, model in models.items():
            if model:
                try:
                    proba = model.predict_proba(df)[0][1] * 100
                    predictions[comp_name] = proba
                except Exception as e:
                    st.error(f"Помилка прогнозування {comp_name}: {str(e)}")
                    predictions[comp_name] = 0
            else:
                predictions[comp_name] = 0
        
        # Назви ускладнень
        comp_names = {
            'aki': '💧 Гостре пошкодження нирок (AKI)',
            'delirium': '🧠 Делірій',
            'respiratory': '🫁 Респіраторні ускладнення',
            'infection': '🦠 Інфекційні ускладнення',
            'af': '⚡ Фібриляція передсердь',
            'lco': '💔 Низький серцевий викид',
            'stroke': '🧠 Інсульт',
            'anastomotic_leak': '💥 Неспроможність анастомозу',
            'ileus': '🔄 Паралітичний іліус',
            'thrombosis': '🔴 Тромбоз',
            'amputation': '🦵 Ампутація',
            'vte': '🔴 Тромбоемболія (ТЕЛА)',
            'pji': '🦠 Перипротезна інфекція',
            'air_leak': '💨 Витік повітря',
            'atelectasis': '🫁 Ателектаз'
        }
        
        def get_risk_level(risk):
            if risk >= 60:
                return "🔴 Високий", "#DC2626"
            elif risk >= 30:
                return "🟡 Помірний", "#F59E0B"
            else:
                return "🟢 Низький", "#10B981"
        
        # Рекомендації (базові)
        recs = {
            'aki': {
                'high': ["MAP ≥65, СІ >2.4", "Cr q12h", "Уникати нефротоксинів"],
                'medium': ["Cr щодоби", "Адекватна перфузія"],
                'low': ["Стандартний моніторинг"]
            },
            'delirium': {
                'high': ["CAM-ICU q зміну", "Уникати бензодіазепінів", "Рання мобілізація"],
                'medium': ["CAM-ICU щодоби", "Мінімізація седації"],
                'low': ["Стандартний"]
            },
            'respiratory': {
                'high': ["Превентивна NIV", "Дих. гімнастика q4h", "Рання вертикалізація"],
                'medium': ["Дихальна гімнастика", "Рання мобілізація"],
                'low': ["Стандартний"]
            },
            'infection': {
                'high': ["АБ профілактика (цефазолін 2г в/в за 30-60хв до розрізу)", "Глікемія <10 ммоль/л", "Нормотермія >36°C", "Повторна доза АБ якщо операція >3год"],
                'medium': ["АБ профілактика (стандартна)", "Контроль глікемії", "Асептика"],
                'low': ["Стандартна АБ профілактика", "Асептика"]
            },
            'af': {
                'high': ["Аміодарон 200мг x2 (профілактика)", "ЕКГ моніторинг 72год", "K+ >4.0, Mg >1.0 ммоль/л", "β-блокатори якщо немає протипоказань"],
                'medium': ["ЕКГ моніторинг 48год", "Корекція електролітів (K+, Mg)", "Розглянути β-блокатори"],
                'low': ["ЕКГ моніторинг", "Стандартний контроль електролітів"]
            },
            'lco': {
                'high': ["Норадреналін готовий", "Інваз. моніторинг", "ЕхоКГ"],
                'medium': ["Інотропи готові", "ScvO2"],
                'low': ["Стандартний"]
            },
            'stroke': {
                'high': ["ЕхоКГ аорти", "No-touch", "Глікемія 6-10"],
                'medium': ["ЕхоКГ", "Контроль глікемії"],
                'low': ["Стандартний"]
            },
            'anastomotic_leak': {
                'high': ["Дренування", "Моніторинг С-реактивного білка", "КТ при підозрі"],
                'medium': ["Моніторинг клініки", "Дренаж"],
                'low': ["Стандартний"]
            },
            'ileus': {
                'high': ["Рання ентеральна стимуляція", "Прокінетики", "Мобілізація"],
                'medium': ["Рання мобілізація", "Моніторинг"],
                'low': ["Стандартний"]
            },
            'thrombosis': {
                'high': ["Ретельний моніторинг периферичної перфузії", "Доплер УЗД", "Антитромботична терапія"],
                'medium': ["Моніторинг перфузії", "УЗД"],
                'low': ["Стандартний"]
            },
            'amputation': {
                'high': ["Агресивна реваскуляризація", "Контроль глікемії", "Wound care"],
                'medium': ["Моніторинг ішемії"],
                'low': ["Стандартний"]
            },
            'vte': {
                'high': ["НМГ (еноксапарин 40мг/добу) або ПОАК (ривароксабан 10мг)", "Механічна компресія (ППК)", "Рання мобілізація", "Тривалість: 28-35 днів (Європ. настанови 2024)"],
                'medium': ["НМГ або ПОАК при факторах ризику", "Механічна компресія", "Рання мобілізація", "АСК 100мг - альтернатива при низькому ризику"],
                'low': ["Рання мобілізація (обов'язково!)", "Механічна компресія (опціонально)", "Фармако НЕ потрібна якщо немає факторів ризику"]
            },
            'pji': {
                'high': ["Подовжена АБ профілактика (цефазолін до 24год)", "Глікемія <10 ммоль/л (цукровий діабет!)", "Ретельна асептика", "ІМТ >40 - збільшити дозу АБ"],
                'medium': ["АБ профілактика стандартна", "Контроль глікемії", "Асептика"],
                'low': ["Стандартна АБ профілактика"]
            },
            'air_leak': {
                'high': ["Пролонгований дренаж", "Плевродез при потребі", "Моніторинг"],
                'medium': ["Дренаж до припинення", "Моніторинг"],
                'low': ["Стандартний"]
            },
            'atelectasis': {
                'high': ["Агресивна респіраторна терапія", "Фібробронхоскопія", "NIV"],
                'medium': ["Дихальна гімнастика", "Інспіратометрія"],
                'low': ["Стандартний"]
            }
        }
        
        # Відображення
        for comp, risk in predictions.items():
            level_text, color = get_risk_level(risk)
            
            col_a, col_b = st.columns([2, 3])
            
            with col_a:
                st.markdown(f"### {comp_names.get(comp, comp)}")
                st.markdown(f"<h2 style='color: {color};'>{level_text}: {risk:.0f}%</h2>", unsafe_allow_html=True)
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk,
                    title={'text': "Ризик"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': color},
                        'steps': [
                            {'range': [0, 30], 'color': "#D1FAE5"},
                            {'range': [30, 60], 'color': "#FEF3C7"},
                            {'range': [60, 100], 'color': "#FEE2E2"}
                        ]
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True, key=f"gauge_{surgery_type}_{comp}")
            
            with col_b:
                st.markdown("#### 📋 Рекомендації:")
                if comp in recs:
                    if risk >= 60:
                        r = recs[comp]['high']
                    elif risk >= 30:
                        r = recs[comp]['medium']
                    else:
                        r = recs[comp]['low']
                    for rec in r:
                        st.markdown(f"- {rec}")
            
            st.markdown("")
        
        st.markdown("---")
        st.info(f"ℹ️ Random Forest моделі на 1000 пацієнтів. Тип: {surgery_type}")
    
    else:
        st.info("👈 Введіть дані та натисніть 'Розрахувати'")

with tab3:
    st.markdown("### ℹ️ Про систему")
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("""
        #### 🤖 Повна ML-система
        
        **5 типів операцій:**
        - ❤️ Кардіохірургія (7 ускладнень)
        - 🏥 Абдомінальна (6 ускладнень)
        - 🩸 Судинна (6 ускладнень)
        - 🦴 Ортопедія (6 ускладнень)
        - 🫁 Торакальна (6 ускладнень)
        
        **32 Random Forest моделі**
        - 1000 пацієнтів на тип
        - AUC: 0.58 - 0.76
        """)
    
    with col_i2:
        st.markdown("""
        #### 📚 Для майстер-класу
        
        **Навчальні дані в комплекті:**
        - cardiac_training_data.csv
        - abdominal_training_data.csv
        - vascular_training_data.csv
        - orthopedic_training_data.csv
        - thoracic_training_data.csv
        
        **Учні можуть:**
        - Валідувати на своїх даних
        - Перетренувати моделі
        - Додати нові фактори
        """)
    
    st.success("✅ Готово для БУС-18 майстер-класу!")

st.markdown("---")
st.caption("ICU Digital Twin v3.0 Full | БУС-18, 2026 | © Prof. Mazur A.P.")
