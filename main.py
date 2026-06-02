# ========== ЧТО МЕНЯТЬ ПОД СВОЮ БД ==========
# 
# 1. ЦВЕТА — взять из руководства по стилю
# 2. НАЗВАНИЯ ТАБЛИЦ И ПОЛЕЙ — везде в SQL-запросах
# 3. ЗАГОЛОВОК ОКНА — строка с setWindowTitle


import sys, os, shutil, uuid
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import *
from db import get_connection

BASE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(BASE, "resources")
PHOTOS = os.path.join(RES, "photos")
ICON_ICO = os.path.join(RES, "icon.ico")
ICON_PNG = os.path.join(RES, "icon.png")
PICTURE = os.path.join(RES, "picture.png")
os.makedirs(PHOTOS, exist_ok=True)
# ⬇️ ЦВЕТА — ЗАМЕНИТЬ НА СВОИ
C_WHITE = "#FFFFFF"    # основной фон (всегда белый)
C_DISC = "#F4A460"     # скидка >12% (всегда этот)
C_ZERO = "#ADD8E6"     # нет на складе (может отличаться)

def db_query(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        conn.close()

def db_fetch_one(sql, params=None):
    rows = db_query(sql, params)
    return rows[0] if rows else None

def db_execute(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
    finally:
        conn.close()

class LoginDialog(QDialog):
     # ... без изменений ...
    def __init__(self):
        super().__init__()
        self.user_data = None
        self.setWindowTitle("Вход")
        self.setFixedSize(300, 150)
        if os.path.exists(ICON_ICO): self.setWindowIcon(QIcon(ICON_ICO))

        l = QVBoxLayout(self)
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Логин")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_edit.setPlaceholderText("Пароль")
        l.addWidget(QLabel("Логин:"))
        l.addWidget(self.login_edit)
        l.addWidget(QLabel("Пароль:"))
        l.addWidget(self.pwd_edit)

        b = QHBoxLayout()
        btn1 = QPushButton("Войти")
        btn2 = QPushButton("Гость")
        btn1.clicked.connect(self.on_login)
        btn2.clicked.connect(self.on_guest)
        b.addWidget(btn1)
        b.addWidget(btn2)
        l.addLayout(b)

    def on_login(self):
        lg = self.login_edit.text().strip()
        pw = self.pwd_edit.text().strip()
        if not lg or not pw:
            QMessageBox.warning(self, "Ошибка", "Заполните поля")
            return
        try:
        #ЗАПРОС ЛОГИНА — ЗАМЕНИТЬ НАЗВАНИЯ ТАБЛИЦ И ПОЛЕЙ
            row = db_fetch_one("""
                SELECT u.user_id, uf.fio, ur.role
                FROM users u
                JOIN user_fio uf ON u.fio = uf.fio_id
                JOIN user_roles ur ON u.role = ur.role_id
                WHERE u.login = %s AND u.password = %s
            """, (lg, pw))
            # ... дальше без изменений ...
        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", str(e))
            return
        if row:
            self.user_data = (row["user_id"], row["fio"], row["role"])
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

    def on_guest(self):
        self.user_data = (None, "Гость", "Гость")
        self.accept()

class ProductEdit(QDialog):
    def __init__(self, article=None):
        super().__init__()
        self.article = article
        self.img_path = ""
        self.setWindowTitle("Редактировать" if article else "Добавить")
        self.setFixedSize(500, 450)

        l = QFormLayout(self)

        self.art_edit = QLineEdit()
        self.name_combo = QComboBox()
        self.cat_combo = QComboBox()
        self.man_combo = QComboBox()
        self.sup_combo = QComboBox()
        self.price_edit = QLineEdit()
        self.stock_edit = QLineEdit()
        self.disc_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(60)
        # СПРАВОЧНИКИ ДЛЯ КОМБОБОКСОВ — ЗАМЕНИТЬ НАЗВАНИЯ ТАБЛИЦ И ПОЛЕЙ
        for r in db_query("SELECT product_id, name FROM products"):
            self.name_combo.addItem(r["name"], r["product_id"])
        for r in db_query("SELECT category_id, category_name FROM categories"):
            self.cat_combo.addItem(r["category_name"], r["category_id"])
        for r in db_query("SELECT manufacturer_id, manufacturer_name FROM manufacturers"):
            self.man_combo.addItem(r["manufacturer_name"], r["manufacturer_id"])
        for r in db_query("SELECT supplier_id, name FROM suppliers"):
            self.sup_combo.addItem(r["name"], r["supplier_id"])

        l.addRow("Артикул:", self.art_edit)
        l.addRow("Название:", self.name_combo)
        l.addRow("Категория:", self.cat_combo)
        l.addRow("Производитель:", self.man_combo)
        l.addRow("Поставщик:", self.sup_combo)
        l.addRow("Описание:", self.desc_edit)
        l.addRow("Цена:", self.price_edit)
        l.addRow("Склад:", self.stock_edit)
        l.addRow("Скидка %:", self.disc_edit)

        btn_img = QPushButton("Фото")
        btn_img.clicked.connect(self.pick_img)
        l.addRow("Фото:", btn_img)

        btns = QHBoxLayout()
        save = QPushButton("Сохранить")
        save.clicked.connect(self.save)
        cancel = QPushButton("Отмена")
        cancel.clicked.connect(self.reject)
        btns.addWidget(save)
        btns.addWidget(cancel)
        l.addRow(btns)

        if article:
            self.load_data(article)

    def load_data(self, article):
        # ⬇️ ЗАГРУЗКА ТОВАРА — ЗАМЕНИТЬ НАЗВАНИЕ ТАБЛИЦЫ И ПОЛЕЙ
        r = db_fetch_one("SELECT * FROM tovar WHERE article = %s", (article,))
        if not r:
            QMessageBox.critical(self, "Ошибка", "Товар не найден")
            self.reject()
            return
        # ⬇️ ПОЛЯ ТОВАРА — ЗАМЕНИТЬ НА СВОИ
        self.art_edit.setText(r["article"])
        self.art_edit.setReadOnly(True)
        self.price_edit.setText(str(r["price"] or ""))
        self.stock_edit.setText(str(r["stock_quantity"] or ""))
        self.disc_edit.setText(str(r["discount"] or ""))
        self.desc_edit.setText(r["description"] or "")
        self.img_path = r["image_path"] or ""
        # ⬇️ ID для комбобоксов — ЗАМЕНИТЬ НА СВОИ
        ci = self.name_combo.findData(r["product_id"])
        if ci >= 0: self.name_combo.setCurrentIndex(ci)
        ci = self.cat_combo.findData(r["category_id"])
        if ci >= 0: self.cat_combo.setCurrentIndex(ci)
        ci = self.man_combo.findData(r["manufacturer_id"])
        if ci >= 0: self.man_combo.setCurrentIndex(ci)
        ci = self.sup_combo.findData(r["supplier_id"])
        if ci >= 0: self.sup_combo.setCurrentIndex(ci)

    def pick_img(self):
        f, _ = QFileDialog.getOpenFileName(self, "Фото", "", "Images (*.png *.jpg)")
        if f: self.img_path = f

    def save(self):
        art = self.art_edit.text().strip()
        if not art:
            QMessageBox.warning(self, "Ошибка", "Введите артикул")
            return
        try:
            price = int(self.price_edit.text())
            stock = int(self.stock_edit.text())
            disc = int(self.disc_edit.text())
        except:
            QMessageBox.warning(self, "Ошибка", "Неверные числа")
            return

        saved = self.img_path
        if self.img_path and os.path.exists(self.img_path):
            ext = os.path.splitext(self.img_path)[1]
            fn = f"{uuid.uuid4().hex}{ext}"
            dest = os.path.join(PHOTOS, fn)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy(self.img_path, dest)
            saved = fn

        if self.article:
            # ⬇️ UPDATE — ЗАМЕНИТЬ НАЗВАНИЕ ТАБЛИЦЫ И ВСЕ ПОЛЯ
            db_execute("""
                UPDATE tovar SET product_id=%s, category_id=%s, manufacturer_id=%s,
                supplier_id=%s, description=%s, price=%s, stock_quantity=%s,
                discount=%s, image_path=%s
                WHERE article=%s
            """, (
                self.name_combo.currentData(), self.cat_combo.currentData(),
                self.man_combo.currentData(), self.sup_combo.currentData(),
                self.desc_edit.toPlainText(), price, stock, disc, saved,
                self.article
            ))
        else:
            # ⬇️ INSERT — ЗАМЕНИТЬ НАЗВАНИЕ ТАБЛИЦЫ И ВСЕ ПОЛЯ
            db_execute("""
                INSERT INTO tovar (article, product_id, category_id, manufacturer_id,
                supplier_id, description, price, stock_quantity, discount, image_path, unit_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
            """, (
                art, self.name_combo.currentData(), self.cat_combo.currentData(),
                self.man_combo.currentData(), self.sup_combo.currentData(),
                self.desc_edit.toPlainText(), price, stock, disc, saved
            ))
        self.accept()

class OrderEdit(QDialog):
    def __init__(self, order_id=None):
        super().__init__()
        self.order_id = order_id
        self.setWindowTitle("Редактировать заказ" if order_id else "Добавить заказ")
        self.setFixedSize(450, 350)

        l = QFormLayout(self)

        self.num_edit = QLineEdit()
        self.art_edit = QLineEdit()
        self.status_combo = QComboBox()
        self.pvz_combo = QComboBox()
        self.fio_combo = QComboBox()
        self.date1 = QDateEdit(QDate.currentDate())
        self.date1.setCalendarPopup(True)
        self.date2 = QDateEdit(QDate.currentDate().addDays(1))
        self.date2.setCalendarPopup(True)
        self.code_edit = QLineEdit()
        # ⬇️ СПРАВОЧНИКИ — ЗАМЕНИТЬ НАЗВАНИЯ ТАБЛИЦ И ПОЛЕЙ
        for r in db_query("SELECT status_id, status_name FROM order_status"):
            self.status_combo.addItem(r["status_name"], r["status_id"])
        for r in db_query("SELECT pvz_id, address FROM pvz"):
            self.pvz_combo.addItem(r["address"], r["pvz_id"])
        for r in db_query("SELECT fio_id, fio FROM user_fio"):
            self.fio_combo.addItem(r["fio"], r["fio_id"])

        l.addRow("Номер заказа:", self.num_edit)
        l.addRow("Артикулы:", self.art_edit)
        l.addRow("Статус:", self.status_combo)
        l.addRow("ПВЗ:", self.pvz_combo)
        l.addRow("Клиент:", self.fio_combo)
        l.addRow("Дата заказа:", self.date1)
        l.addRow("Дата доставки:", self.date2)
        l.addRow("Код получения:", self.code_edit)

        if order_id:
            r = db_fetch_one("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            if r:
                self.num_edit.setText(str(r["order_id"]))
                self.num_edit.setReadOnly(True)
                self.art_edit.setText(r["article_text"] or "")
                self.code_edit.setText(str(r["pickup_code"] or ""))
                si = self.status_combo.findData(r["status_id"])
                if si >= 0: self.status_combo.setCurrentIndex(si)
                pi = self.pvz_combo.findData(r["pvz_id"])
                if pi >= 0: self.pvz_combo.setCurrentIndex(pi)
                fi = self.fio_combo.findData(r["client_fio_id"])
                if fi >= 0: self.fio_combo.setCurrentIndex(fi)
                if r["order_date"]:
                    self.date1.setDate(QDate.fromString(r["order_date"], "yyyy-MM-dd"))
                if r["delivery_date"]:
                    self.date2.setDate(QDate.fromString(r["delivery_date"], "yyyy-MM-dd"))
        else:
            max_num = db_fetch_one("SELECT MAX(order_id) as m FROM orders")
            next_num = (max_num["m"] or 0) + 1 if max_num else 1
            self.num_edit.setText(str(next_num))
            self.num_edit.setReadOnly(True)
            max_code = db_fetch_one("SELECT MAX(pickup_code) as m FROM orders")
            next_code = (max_code["m"] or 900) + 1 if max_code else 901
            self.code_edit.setText(str(next_code))
            self.code_edit.setReadOnly(True)

        btns = QHBoxLayout()
        save = QPushButton("Сохранить")
        save.clicked.connect(self.save)
        cancel = QPushButton("Отмена")
        cancel.clicked.connect(self.reject)
        btns.addWidget(save)
        btns.addWidget(cancel)
        l.addRow(btns)

    def save(self):
        d1 = self.date1.date().toString("yyyy-MM-dd")
        d2 = self.date2.date().toString("yyyy-MM-dd")
        if self.order_id:
            # ⬇️ UPDATE ЗАКАЗА — ЗАМЕНИТЬ НАЗВАНИЕ ТАБЛИЦЫ И ПОЛЯ
            db_execute("""
                UPDATE orders SET article_text=%s, status_id=%s, pvz_id=%s,
                client_fio_id=%s, order_date=%s, delivery_date=%s
                WHERE order_id=%s
            """, (
                self.art_edit.text(), self.status_combo.currentData(),
                self.pvz_combo.currentData(), self.fio_combo.currentData(),
                d1, d2, self.order_id
            ))
        else:
            # ⬇️ INSERT ЗАКАЗА — ЗАМЕНИТЬ НАЗВАНИЕ ТАБЛИЦЫ И ПОЛЯ
            db_execute("""
                INSERT INTO orders (order_id, article_text, status_id, pvz_id,
                client_fio_id, order_date, delivery_date, pickup_code)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                int(self.num_edit.text()), self.art_edit.text(),
                self.status_combo.currentData(), self.pvz_combo.currentData(),
                self.fio_combo.currentData(), d1, d2, int(self.code_edit.text())
            ))
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.uid, self.fio, self.role = user_data
        self.edit_open = False
        # ⬇️ ЗАГОЛОВОК — ЗАМЕНИТЬ НА СВОЙ
        self.setWindowTitle("Список товаров")
        self.resize(1100, 650)
        if os.path.exists(ICON_ICO): self.setWindowIcon(QIcon(ICON_ICO))

        c = QWidget()
        self.setCentralWidget(c)
        l = QVBoxLayout(c)

        h = QHBoxLayout()
        if os.path.exists(ICON_PNG):
            logo = QLabel()
            logo.setPixmap(QPixmap(ICON_PNG).scaled(60, 40, Qt.AspectRatioMode.KeepAspectRatio))
            h.addWidget(logo)
        h.addStretch()
        h.addWidget(QLabel(f"{self.fio} ({self.role})"))
        btn_out = QPushButton("Выход")
        btn_out.clicked.connect(self.logout)
        h.addWidget(btn_out)
        l.addLayout(h)

        self.fbox = QWidget()
        fb = QHBoxLayout(self.fbox)
        fb.addWidget(QLabel("Поиск:"))
        self.search = QLineEdit()
        fb.addWidget(self.search)
        fb.addWidget(QLabel("Производитель:"))
        self.manuf = QComboBox()
        fb.addWidget(self.manuf)
        fb.addWidget(QLabel("Сортировка:"))
        self.sort = QComboBox()
        self.sort.addItems(["Нет", "Цена ↑", "Цена ↓", "Склад ↑", "Склад ↓"])
        fb.addWidget(self.sort)
        l.addWidget(self.fbox)

        self.abox = QWidget()
        ab = QHBoxLayout(self.abox)
        btn_add = QPushButton("Добавить")
        btn_edit = QPushButton("Изменить")
        btn_del = QPushButton("Удалить")
        ab.addWidget(btn_add)
        ab.addWidget(btn_edit)
        ab.addWidget(btn_del)
        l.addWidget(self.abox)

        self.btn_ord = QPushButton("Заказы")
        l.addWidget(self.btn_ord)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        # ⬇️ ЗАГОЛОВКИ ТАБЛИЦЫ — ПОДСТРОИТЬ ПОД СВОИ ПОЛЯ
        self.table.setHorizontalHeaderLabels(["Фото", "Артикул", "Название", "Категория", "Цена", "Скидка", "Склад", "Производитель"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.on_double_click)
        l.addWidget(self.table)

        self.search.textChanged.connect(self.load)
        self.manuf.currentTextChanged.connect(self.load)
        self.sort.currentTextChanged.connect(self.load)
        btn_add.clicked.connect(self.add_product)
        btn_edit.clicked.connect(self.edit_product)
        btn_del.clicked.connect(self.delete_product)
        self.btn_ord.clicked.connect(self.show_orders)

        self.apply_role()
        self.load_manuf()
        self.load()

    def apply_role(self):
        adv = self.role in ("Менеджер", "Администратор")
        adm = self.role == "Администратор"
        self.fbox.setVisible(adv)
        self.abox.setVisible(adm)
        self.btn_ord.setVisible(adv)

    def on_double_click(self):        
        if self.role == "Администратор":
            self.edit_product()

    def load_manuf(self):
        # ⬇️ ЗАГРУЗКА ПРОИЗВОДИТЕЛЕЙ — ЗАМЕНИТЬ ТАБЛИЦУ И ПОЛЕ
        self.manuf.clear()
        self.manuf.addItem("Все")
        for r in db_query("SELECT manufacturer_name FROM manufacturers ORDER BY manufacturer_name"):
            self.manuf.addItem(r["manufacturer_name"])

    def load(self):
        # ⬇️ ГЛАВНЫЙ ЗАПРОС — ЗАМЕНИТЬ ВСЕ НАЗВАНИЯ ТАБЛИЦ И ПОЛЕЙ
        q = """
            SELECT t.article, t.price, t.discount, t.stock_quantity, t.image_path,
                p.name AS product_name,
                c.category_name,
                m.manufacturer_name
            FROM tovar t
            JOIN products p ON t.product_id = p.product_id
            JOIN categories c ON t.category_id = c.category_id
            JOIN manufacturers m ON t.manufacturer_id = m.manufacturer_id
            WHERE 1=1
        """
        params = []
        if self.search.text():
            s = f"%{self.search.text().strip()}%"
            q += " AND (p.name LIKE %s OR m.manufacturer_name LIKE %s OR t.description LIKE %s)"
            params.extend([s, s, s])
        man = self.manuf.currentText()
        if man != "Все":
            q += " AND m.manufacturer_name = %s"
            params.append(man)
        sort = self.sort.currentText()
        if sort == "Цена повыш": q += " ORDER BY t.price ASC"
        elif sort == "Цена пониж": q += " ORDER BY t.price DESC"
        elif sort == "Склад повыш": q += " ORDER BY t.stock_quantity ASC"
        elif sort == "Склад пониж": q += " ORDER BY t.stock_quantity DESC"

        rows = db_query(q, params)
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            
            img = r["image_path"] or ""
            full_path = os.path.join(PHOTOS, img) if img else ""
            if os.path.exists(full_path):
                pix = QPixmap(full_path)
            else:
                pix = QPixmap(PICTURE)
            lbl = QLabel()
            lbl.setPixmap(pix.scaled(80, 60, Qt.AspectRatioMode.KeepAspectRatio))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(i, 0, lbl)

            self.table.setItem(i, 1, QTableWidgetItem(r["article"]))
            self.table.setItem(i, 2, QTableWidgetItem(r["product_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(r["category_name"]))
            price = int(r["price"] or 0)
            disc = int(r["discount"] or 0)
            if disc > 0:
                final = int(price * (1 - disc/100))
                txt = f"{price} -> {final}"
            else:
                txt = str(price)
            self.table.setItem(i, 4, QTableWidgetItem(txt))
            self.table.setItem(i, 5, QTableWidgetItem(f"{disc}%"))
            self.table.setItem(i, 6, QTableWidgetItem(str(r["stock_quantity"] or 0)))
            self.table.setItem(i, 7, QTableWidgetItem(r["manufacturer_name"]))

            color = QColor(C_WHITE)
            stock = int(r["stock_quantity"] or 0)
            if stock == 0: color = QColor(C_ZERO)
            elif disc > 12: color = QColor(C_DISC)
            for j in range(8):
                if self.table.item(i, j):
                    self.table.item(i, j).setBackground(color)

    def sel_article(self):
        r = self.table.currentRow()
        if r < 0: return None
        return self.table.item(r, 1).text()

    def add_product(self):
        if self.edit_open: return
        self.edit_open = True
        if ProductEdit().exec(): self.load()
        self.edit_open = False

    def edit_product(self):
        art = self.sel_article()
        if not art or self.edit_open: return
        self.edit_open = True
        if ProductEdit(art).exec(): self.load()
        self.edit_open = False

    def delete_product(self):
        art = self.sel_article()
        if not art: return
        # ⬇️ ПРОВЕРКА ЗАКАЗОВ — ЗАМЕНИТЬ ТАБЛИЦУ И ПОЛЕ
        cnt = db_fetch_one("SELECT COUNT(*) as c FROM orders WHERE article_text LIKE %s", (f"%{art}%",))
        if cnt and cnt["c"] > 0:
            QMessageBox.warning(self, "Ошибка", "Товар в заказах — нельзя удалить")
            return
         # ⬇️ УДАЛЕНИЕ — ЗАМЕНИТЬ ТАБЛИЦУ И ПОЛЕ
        if QMessageBox.question(self, "?", "Удалить?") == QMessageBox.StandardButton.Yes:
            db_execute("DELETE FROM tovar WHERE article = %s", (art,))
            self.load()

    def show_orders(self):
        dlg = OrdersWindow(self.role)
        dlg.exec()

    def logout(self):
        self.close()
        login = LoginDialog()
        if login.exec() == QDialog.DialogCode.Accepted:
            self.next_window = MainWindow(login.user_data)
            self.next_window.show()

class OrdersWindow(QDialog):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle("Заказы")
        self.resize(900, 500)

        l = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
         # ⬇️ ЗАГОЛОВКИ ТАБЛИЦЫ ЗАКАЗОВ
        self.table.setHorizontalHeaderLabels(["Номер", "Артикулы", "Статус", "ПВЗ", "Клиент", "Дата заказа", "Дата доставки"])
        self.table.doubleClicked.connect(self.on_double_click)
        l.addWidget(self.table)

        adm = self.role == "Администратор"
        btns = QHBoxLayout()
        if adm:
            btn_add = QPushButton("Добавить")
            btn_add.clicked.connect(self.add_order)
            btn_edit = QPushButton("Изменить")
            btn_edit.clicked.connect(self.edit_order)
            btn_del = QPushButton("Удалить")
            btn_del.clicked.connect(self.delete_order)
            btns.addWidget(btn_add)
            btns.addWidget(btn_edit)
            btns.addWidget(btn_del)
        btn_close = QPushButton("Назад")
        btn_close.clicked.connect(self.close)
        btns.addWidget(btn_close)
        l.addLayout(btns)

        self.load()

    def load(self):
        # ⬇️ ЗАПРОС ЗАКАЗОВ — ЗАМЕНИТЬ НАЗВАНИЯ ТАБЛИЦ И ПОЛЕЙ
        rows = db_query("""
            SELECT o.order_id, o.article_text, os.status_name,
                   p.address AS pvz_address, uf.fio, o.order_date, o.delivery_date
            FROM orders o
            JOIN order_status os ON o.status_id = os.status_id
            JOIN pvz p ON o.pvz_id = p.pvz_id
            LEFT JOIN user_fio uf ON o.client_fio_id = uf.fio_id
            ORDER BY o.order_id
        """)
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(r["order_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(r["article_text"] or ""))
            self.table.setItem(i, 2, QTableWidgetItem(r["status_name"] or ""))
            self.table.setItem(i, 3, QTableWidgetItem(r["pvz_address"] or ""))
            self.table.setItem(i, 4, QTableWidgetItem(r["fio"] or ""))
            self.table.setItem(i, 5, QTableWidgetItem(r["order_date"] or ""))
            self.table.setItem(i, 6, QTableWidgetItem(r["delivery_date"] or ""))

    def on_double_click(self):
        if self.role == "Администратор":
            self.edit_order()

    def sel_id(self):
        r = self.table.currentRow()
        if r < 0: return None
        return int(self.table.item(r, 0).text())

    def add_order(self):
        if OrderEdit().exec(): self.load()

    def edit_order(self):
        oid = self.sel_id()
        if oid and OrderEdit(oid).exec(): self.load()

    def delete_order(self):
        oid = self.sel_id()
        # ⬇️ УДАЛЕНИЕ ЗАКАЗА — ЗАМЕНИТЬ ТАБЛИЦУ И ПОЛЕ
        if oid and QMessageBox.question(self, "?", "Удалить?") == QMessageBox.StandardButton.Yes:
            db_execute("DELETE FROM orders WHERE order_id = %s", (oid,))
            self.load()

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Calibri", 11))

    login = LoginDialog()
    if login.exec() != QDialog.DialogCode.Accepted:
        sys.exit()

    win = MainWindow(login.user_data)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()