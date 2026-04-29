# ICU DIGITAL TWIN - GOOGLE COLAB NOTEBOOK
# Копіюйте цей код в Google Colab і запускайте по черзі

# ============================================
# КРОК 1: Встановлення бібліотек
# ============================================

!pip install -q streamlit pyngrok scikit-learn plotly joblib

print("✅ Бібліотеки встановлено!")

# ============================================
# КРОК 2: Завантаження файлів
# ============================================

print("\n📁 Завантажте файли:")
print("   - streamlit_app.py")
print("   - model_af.pkl")
print("   - model_aki.pkl")
print("   - model_lco.pkl")
print("   - model_bleeding.pkl")
print("   - model_stroke.pkl")
print("\nКлікніть кнопку 'Choose Files' нижче ⬇️")

from google.colab import files
uploaded = files.upload()

print(f"\n✅ Завантажено {len(uploaded)} файлів!")

# ============================================
# КРОК 3: Налаштування ngrok (для публічного URL)
# ============================================

# Введіть свій authtoken з https://dashboard.ngrok.com/get-started/your-authtoken
# Реєстрація безкоштовна!

import getpass

print("\n🔑 Отримайте токен ngrok:")
print("   1. Перейдіть на: https://dashboard.ngrok.com/get-started/your-authtoken")
print("   2. Скопіюйте ваш authtoken")
print("   3. Вставте нижче:\n")

ngrok_token = getpass.getpass("Введіть ngrok authtoken: ")

!ngrok authtoken {ngrok_token}

print("\n✅ Ngrok налаштовано!")

# ============================================
# КРОК 4: Запуск Streamlit
# ============================================

import subprocess
import time
from pyngrok import ngrok

# Запуск Streamlit у фоновому режимі
streamlit_process = subprocess.Popen(
    ["streamlit", "run", "streamlit_app.py", "--server.port", "8501"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("\n⏳ Запуск Streamlit...")
time.sleep(10)  # Чекаємо 10 секунд

# Створення публічного URL через ngrok
public_url = ngrok.connect(8501)

print("\n" + "="*50)
print("🚀 ICU DIGITAL TWIN ЗАПУЩЕНО!")
print("="*50)
print(f"\n📱 Відкрийте додаток за адресою:")
print(f"   {public_url}")
print("\n💡 Поділіться цим URL з учасниками майстер-класу!")
print("\n⚠️  URL діє, поки цей notebook запущений")
print("="*50)

# Тримаємо процес активним
try:
    streamlit_process.wait()
except KeyboardInterrupt:
    print("\n⛔ Зупинка Streamlit...")
    streamlit_process.terminate()
    ngrok.disconnect(public_url)
