"""
check_all.py — проверка всего перед сдачей демоэкзамена
Запускать из папки с main.py:
    python check_all.py
"""

import os
import sys

# ==================== 1. ПРОВЕРКА ФАЙЛОВ ====================
print("=" * 50)
print("1. ПРОВЕРКА ФАЙЛОВ")
print("=" * 50)

BASE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(BASE, "resources")
PHOTOS = os.path.join(RES, "photos")

files_to_check = [
    ("main.py", os.path.join(BASE, "main.py")),
    ("db.py", os.path.join(BASE, "db.py")),
    ("resources/icon.ico", os.path.join(RES, "icon.ico")),
    ("resources/icon.png", os.path.join(RES, "icon.png")),
    ("resources/picture.png", os.path.join(RES, "picture.png")),
    ("resources/photos/", PHOTOS),
]

all_ok = True
for name, path in files_to_check:
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    if not exists:
        all_ok = False
    print(f"  {status} {name}")

# ==================== 2. ПРОВЕРКА ИМПОРТОВ ====================
print("\n" + "=" * 50)
print("2. ПРОВЕРКА БИБЛИОТЕК")
print("=" * 50)

libs = [
    ("PyQt6", "PyQt6"),
    ("pymysql", "pymysql"),
    ("Pillow", "PIL"),
]

for name, import_name in libs:
    try:
        __import__(import_name)
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ❌ {name} — НЕ УСТАНОВЛЕН! pip install {name}")
        all_ok = False

# ==================== 3. ПРОВЕРКА БД ====================
print("\n" + "=" * 50)
print("3. ПРОВЕРКА БАЗЫ ДАННЫХ")
print("=" * 50)

try:
    from db import get_connection
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    
    # Проверка таблиц
    tables = [
        "users", "user_fio", "user_roles",
        "products", "categories", "manufacturers", "suppliers",
        "tovar",
        "orders", "order_status", "pvz",
    ]
    
    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) as cnt FROM {table}")
            cnt = cur.fetchone()["cnt"]
            status = "✅" if cnt > 0 else "⚠️ (пусто)"
            print(f"  {status} {table}: {cnt} записей")
        except Exception as e:
            print(f"  ❌ {table}: ОШИБКА — {str(e)[:50]}")
            all_ok = False
    
    # Проверка пользователей для входа
    cur.execute("""
        SELECT u.login, u.password, uf.fio, ur.role
        FROM users u
        JOIN user_fio uf ON u.fio = uf.fio_id
        JOIN user_roles ur ON u.role = ur.role_id
        LIMIT 3
    """)
    print("\n  Тестовые пользователи для входа:")
    for row in cur.fetchall():
        print(f"    {row['role']}: {row['login']} / {row['password']} ({row['fio']})")
    
    conn.close()
    print("  ✅ Подключение к БД успешно")
except Exception as e:
    print(f"  ❌ Ошибка БД: {e}")
    all_ok = False

# ==================== 4. ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА ====================
print("\n" + "=" * 50)
print("4. ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
print("=" * 50)

folders = ["resources", "resources/photos", "docs", "sql"]
for folder in folders:
    path = os.path.join(BASE, folder)
    exists = os.path.exists(path)
    status = "✅" if exists else "⚠️ (создай)"
    print(f"  {status} {folder}/")

# ==================== 5. ПРОВЕРКА ФОТО ТОВАРОВ ====================
print("\n" + "=" * 50)
print("5. ПРОВЕРКА ФОТО ТОВАРОВ")
print("=" * 50)

try:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT article, image_path FROM tovar WHERE image_path IS NOT NULL AND image_path != '' LIMIT 5")
    photos = cur.fetchall()
    
    if photos:
        for p in photos:
            path = os.path.join(PHOTOS, p["image_path"])
            exists = os.path.exists(path)
            status = "✅" if exists else "❌"
            print(f"  {status} {p['article']}: {p['image_path']}")
    else:
        print("  ⚠️ Нет товаров с фото в БД")
    conn.close()
except Exception as e:
    print(f"  ❌ Ошибка: {e}")

# ==================== 6. ИТОГ ====================
print("\n" + "=" * 50)
print("6. ИТОГ")
print("=" * 50)

# Проверка EXE
exe_path = os.path.join(BASE, "dist", "ShoeStore2026PUApp.exe")
if os.path.exists(exe_path):
    print("  ✅ EXE файл собран")
else:
    print("  ⚠️ EXE ещё не собран: python build_exe.py")

if all_ok:
    print("\n  ✅ ВСЁ ГОТОВО К СДАЧЕ!")
else:
    print("\n  ❌ ЕСТЬ ПРОБЛЕМЫ — исправь перед сдачей!")

print("\nНажми Enter для выхода...")
input()