"""
ICU DIGITAL TWIN - GOOGLE COLAB
БУС-18 Майстер-клас | 2026

ІНСТРУКЦІЯ:
1. Запустіть комірку 1 (встановлення)
2. Запустіть комірку 2 (завантаження файлів)
3. Запустіть комірку 3 (запуск Streamlit)
4. Запустіть комірку 4 (публічний URL)
5. Відкрийте URL у браузері

Професор Мазур А.П.
"""

# ============================================
# КОМІРКА 1: ВСТАНОВЛЕННЯ ПРОГРАМ
# ============================================

print("=" * 70)
print("🏥 ICU DIGITAL TWIN - БУС-18")
print("=" * 70)
print("")
print("🔧 КРОК 1: Встановлення програм...")
print("")

import subprocess
import sys

# Встановлення
packages = [
    'streamlit',
    'scikit-learn',
    'plotly',
    'joblib',
    'pandas',
    'numpy'
]

for package in packages:
    print(f"  📦 Встановлюємо {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

print("")
print("✅ ВСІ ПРОГРАМИ ВСТАНОВЛЕНО!")
print("")
print("⏱️  Це зайняло ~30 секунд")
print("")
print("👉 НАСТУПНИЙ КРОК: Запустіть КОМІРКУ 2 для завантаження файлів")
print("")

# ============================================
# КОМІРКА 2: ЗАВАНТАЖЕННЯ ФАЙЛІВ
# ============================================

print("=" * 70)
print("📦 КРОК 2: Завантаження файлів")
print("=" * 70)
print("")
print("ПОТРІБНО ЗАВАНТАЖИТИ:")
print("  1️⃣  streamlit_app_full.py (основний додаток)")
print("  2️⃣  all_surgery_metrics.json (метрики)")
print("  3️⃣  Всі model_*.pkl файли (36 штук)")
print("")
print("=" * 70)
print("")
print("❗ ВАЖЛИВО:")
print("  • Завантажуйте ВСІ 38 ФАЙЛІВ ОДРАЗУ")
print("  • Виберіть всі файли в провіднику (Ctrl+A)")
print("  • Натисніть 'Відкрити'")
print("")
print("⏳ Після вибору файлів чекайте 30-60 секунд...")
print("")
print("=" * 70)
print("")

from google.colab import files
import os

uploaded = files.upload()

print("")
print("=" * 70)
print("✅ ЗАВАНТАЖЕННЯ ЗАВЕРШЕНО!")
print("=" * 70)
print("")
print(f"📊 Завантажено файлів: {len(uploaded)}")
print("")

# Перевірка
required_files = {
    'streamlit_app_full.py': False,
    'all_surgery_metrics.json': False,
    'models': 0
}

for filename in uploaded.keys():
    size_mb = len(uploaded[filename]) / (1024*1024)
    print(f"  ✓ {filename} ({size_mb:.2f} MB)")
    
    if filename == 'streamlit_app_full.py':
        required_files['streamlit_app_full.py'] = True
    elif filename == 'all_surgery_metrics.json':
        required_files['all_surgery_metrics.json'] = True
    elif filename.startswith('model_') and filename.endswith('.pkl'):
        required_files['models'] += 1

print("")
print("=" * 70)
print("🔍 ПЕРЕВІРКА ФАЙЛІВ:")
print("=" * 70)

if required_files['streamlit_app_full.py']:
    print("  ✅ streamlit_app_full.py - OK")
else:
    print("  ❌ streamlit_app_full.py - ВІДСУТНІЙ!")

if required_files['all_surgery_metrics.json']:
    print("  ✅ all_surgery_metrics.json - OK")
else:
    print("  ⚠️  all_surgery_metrics.json - відсутній (необов'язковий)")

print(f"  {'✅' if required_files['models'] >= 30 else '❌'} ML моделі: {required_files['models']}/36")

print("")

if required_files['streamlit_app_full.py'] and required_files['models'] >= 30:
    print("✅ ВСЕ ГОТОВО ДО ЗАПУСКУ!")
    print("")
    print("👉 НАСТУПНИЙ КРОК: Запустіть КОМІРКУ 3 для запуску Streamlit")
else:
    print("⚠️  УВАГА: Не вистачає файлів!")
    print("   Завантажте відсутні файли та запустіть цю комірку знову")

print("")

# ============================================
# КОМІРКА 3: ЗАПУСК STREAMLIT
# ============================================

print("=" * 70)
print("🚀 КРОК 3: Запуск Streamlit")
print("=" * 70)
print("")

import subprocess
import time

# Перевірка що файл існує
if not os.path.exists('streamlit_app_full.py'):
    print("❌ ПОМИЛКА: streamlit_app_full.py не знайдено!")
    print("   Поверніться до КОМІРКИ 2 та завантажте файли")
else:
    print("✓ streamlit_app_full.py знайдено")
    print("")
    print("🔧 Запускаємо Streamlit сервер...")
    print("   (це займе ~15 секунд)")
    print("")
    
    # Запуск Streamlit у фоновому режимі
    process = subprocess.Popen([
        "streamlit", "run", 
        "streamlit_app_full.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("⏳ Чекаємо 15 секунд...")
    for i in range(15, 0, -1):
        print(f"   {i} секунд...", end='\r')
        time.sleep(1)
    
    print("")
    print("")
    print("=" * 70)
    print("✅ STREAMLIT ЗАПУЩЕНО!")
    print("=" * 70)
    print("")
    print("📱 Сервер працює на http://localhost:8501")
    print("")
    print("👉 НАСТУПНИЙ КРОК: Запустіть КОМІРКУ 4 для створення публічного URL")
    print("")

# ============================================
# КОМІРКА 4: СТВОРЕННЯ ПУБЛІЧНОГО URL
# ============================================

print("=" * 70)
print("🌐 КРОК 4: Створення публічного URL")
print("=" * 70)
print("")
print("Використовуємо Cloudflare Tunnel (безкоштовно, без реєстрації)")
print("")
print("❗ ВАЖЛИВО:")
print("  • НЕ ЗУПИНЯЙТЕ цю комірку!")
print("  • Поки вона працює - URL активний")
print("  • URL буде працювати ~12 годин")
print("")
print("=" * 70)
print("")

# Завантаження cloudflared
print("📥 Завантажуємо Cloudflare Tunnel...")
subprocess.run([
    "wget", "-q",
    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
], check=True)

subprocess.run(["chmod", "+x", "cloudflared-linux-amd64"], check=True)

print("✅ Tunnel готовий!")
print("")
print("=" * 70)
print("🔗 ВАШ ПУБЛІЧНИЙ URL З'ЯВИТЬСЯ НИЖЧЕ:")
print("=" * 70)
print("")
print("⏳ Зачекайте 5-10 секунд...")
print("")

# Запуск тунелю
# Ця команда працює доки не зупините комірку
subprocess.run(["./cloudflared-linux-amd64", "tunnel", "--url", "http://localhost:8501"])

# ============================================
# ДОДАТКОВА КОМІРКА: ДІАГНОСТИКА
# ============================================

print("=" * 70)
print("🔍 ДІАГНОСТИКА")
print("=" * 70)
print("")

# Перевірка файлів
print("📁 Файли у поточній директорії:")
files_list = [f for f in os.listdir('.') if f.endswith('.py') or f.endswith('.pkl') or f.endswith('.json')]
print(f"   Всього файлів: {len(files_list)}")
print("")

# Перевірка моделей
pkl_files = [f for f in files_list if f.endswith('.pkl')]
print(f"📊 ML моделі (.pkl): {len(pkl_files)}")
for surgery_type in ['cardiac', 'abdominal', 'vascular', 'orthopedic', 'thoracic']:
    count = len([f for f in pkl_files if f.startswith(f'model_{surgery_type}_')])
    status = "✅" if count > 0 else "❌"
    print(f"   {status} {surgery_type}: {count} моделей")

print("")

# Перевірка процесів
print("🔄 Запущені процеси:")
result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
if 'streamlit' in result.stdout:
    print("   ✅ Streamlit працює")
else:
    print("   ❌ Streamlit НЕ працює")

if 'cloudflared' in result.stdout:
    print("   ✅ Cloudflare tunnel працює")
else:
    print("   ⚠️  Cloudflare tunnel не активний")

print("")
print("=" * 70)

# ============================================
# ДОДАТКОВА КОМІРКА: ПЕРЕЗАПУСК
# ============================================

print("=" * 70)
print("🔄 ПЕРЕЗАПУСК СИСТЕМИ")
print("=" * 70)
print("")
print("Якщо щось пішло не так, використайте цю комірку")
print("")

# Зупинка всіх процесів
print("⏸️  Зупиняємо всі процеси...")
subprocess.run(["pkill", "-f", "streamlit"], stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-f", "cloudflared"], stderr=subprocess.DEVNULL)

time.sleep(2)

print("✅ Всі процеси зупинено")
print("")
print("👉 ТЕПЕР:")
print("   1. Запустіть КОМІРКУ 3 (запуск Streamlit)")
print("   2. Запустіть КОМІРКУ 4 (публічний URL)")
print("")
print("=" * 70)
