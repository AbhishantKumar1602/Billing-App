import sys, sqlite3, json, os
from datetime import datetime

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QFrame, QDoubleSpinBox, QMessageBox, QFileDialog,
    QHeaderView, QDialog, QGridLayout, QTabWidget, QStatusBar,
    QAbstractItemView, QCompleter, QDialogButtonBox, QScrollArea,
    QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QMarginsF
from PyQt6.QtGui import QPageSize, QPageLayout, QFont, QColor, QPalette
import platform

# ════════════════════════════════════════════════
#  THEME SYSTEM
# ════════════════════════════════════════════════
THEMES = {
    "dark": {
        "BG_DARK":       "#111217",  # true dark, elegant
        "BG_CARD":       "#181a22",
        "BG_INPUT":      "#20222b",
        "BG_HOVER":      "#23263a",
        "ACCENT":        "#00bcd4",  # cyan/teal accent
        "ACCENT_LIGHT":  "#26e6ff",
        "ACCENT_DIM":    "#00bcd420",
        "ACCENT_GLOW":   "#00bcd410",
        "GREEN":         "#27d99a",
        "GREEN_DIM":     "#27d99a20",
        "RED_C":         "#ff4f6e",
        "RED_DIM":       "#ff4f6e20",
        "YELLOW":        "#f5c842",
        "YELLOW_DIM":    "#f5c84220",
        "TEXT_PRIMARY":  "#eaf6fb",
        "TEXT_MUTED":    "#7bb7c7",
        "TEXT_FAINT":    "#2a2d38",
        "BORDER":        "#1a1c23",
        "BORDER_LIGHT":  "#2d3150",
        "TOPBAR":        "#15171e",
        "TOPBAR_BORDER": "#00bcd4",
        "TABLE_ALT":     "#171a23",
        "NETCARD_BG":    "#16232b",
        "NETCARD_BORDER":"#00bcd4",
        "SCROLLBAR":     "#23263a",
    },
    "light": {
        "BG_DARK":       "#f7f8f5",  # warm off-white
        "BG_CARD":       "#fdfdfb",
        "BG_INPUT":      "#f2f6f5",
        "BG_HOVER":      "#e6f0ee",
        "ACCENT":        "#008080",  # deep teal accent
        "ACCENT_LIGHT":  "#26bfa6",
        "ACCENT_DIM":    "#00808020",
        "ACCENT_GLOW":   "#00808010",
        "GREEN":         "#16a872",
        "GREEN_DIM":     "#16a87218",
        "RED_C":         "#dc3558",
        "RED_DIM":       "#dc355818",
        "YELLOW":        "#b8860b",
        "YELLOW_DIM":    "#b8860b18",
        "TEXT_PRIMARY":  "#1a2a2a",
        "TEXT_MUTED":    "#4b6d6a",
        "TEXT_FAINT":    "#c0c2d8",
        "BORDER":        "#dbe6e4",
        "BORDER_LIGHT":  "#c0d3d0",
        "TOPBAR":        "#fdfdfb",
        "TOPBAR_BORDER": "#008080",
        "TABLE_ALT":     "#f3f7f5",
        "NETCARD_BG":    "#eafaf7",
        "NETCARD_BORDER":"#008080",
        "SCROLLBAR":     "#d8eaea",
    }
}

_CURRENT_THEME = "dark"

def T(key):
    return THEMES[_CURRENT_THEME][key]

def build_stylesheet():
    return f"""
QMainWindow, QWidget {{
    background: {T('BG_DARK')};
    color: {T('TEXT_PRIMARY')};
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
    font-size: 13px;
}}
QTabWidget::pane {{
    border: none;
    background: {T('BG_DARK')};
    top: 0px;
}}
QTabWidget > QWidget {{ background: {T('BG_DARK')}; }}
QTabBar {{
    background: {T('BG_CARD')};
    border-bottom: 2px solid {T('BORDER')};
}}
QTabBar::tab {{
    background: transparent;
    color: {T('TEXT_MUTED')};
    padding: 14px 36px;
    font-weight: 700;
    font-size: 13px;
    border: none;
    border-bottom: 2px solid transparent;
    min-width: 120px;
    letter-spacing: 1.2px;
    transition: color 0.2s, background 0.2s, border 0.2s;
}}
QTabBar::tab:selected {{
    color: {T('ACCENT_LIGHT')};
    border-bottom: 2px solid {T('ACCENT')};
    font-weight: 700;
    background: {T('ACCENT_GLOW')};
}}
QTabBar::tab:hover:!selected {{
    color: {T('TEXT_PRIMARY')};
    background: {T('BG_HOVER')};
}}
QLineEdit, QDoubleSpinBox, QSpinBox {{
    background: {T('BG_INPUT')};
    border: 1.5px solid {T('BORDER')};
    border-radius: 7px;
    padding: 8px 12px;
    color: {T('TEXT_PRIMARY')};
    font-size: 13px;
    selection-background-color: {T('ACCENT')};
    min-height: 18px;
}}
QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {{
    border: 1.5px solid {T('ACCENT')};
    background: {T('BG_HOVER')};
}}
QLineEdit:read-only {{
    background: {T('BG_DARK')};
    color: {T('TEXT_MUTED')};
    border: 1.5px solid {T('BORDER')};
    border-radius: 7px;
}}
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
QSpinBox::up-button, QSpinBox::down-button {{ width: 0px; border: none; }}
QTableWidget {{
    background: {T('BG_DARK')};
    border: 1.5px solid {T('BORDER')};
    border-radius: 10px;
    gridline-color: {T('BORDER')};
    color: {T('TEXT_PRIMARY')};
    font-size: 13px;
    outline: none;
}}
QTableWidget::item {{ padding: 7px 9px; border: none; }}
QTableWidget::item:selected {{
    background: {T('ACCENT_DIM')};
    color: {T('ACCENT_LIGHT')};
}}
QTableWidget::item:alternate {{ background: {T('TABLE_ALT')}; }}
QHeaderView {{ background: transparent; border: none; }}
QHeaderView::section {{
    background: {T('BG_CARD')};
    color: {T('TEXT_MUTED')};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 10px 9px;
    border: none;
    border-bottom: 2px solid {T('ACCENT')};
    border-right: 1px solid {T('BORDER')};
}}
QHeaderView::section:last {{ border-right: none; }}
QPushButton {{
    background: {T('BG_HOVER')};
    color: {T('TEXT_PRIMARY')};
    border: 1.5px solid {T('BORDER_LIGHT')};
    border-radius: 9px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 13px;
    min-height: 18px;
    transition: background 0.2s, color 0.2s, border 0.2s;
    box-shadow: 0 1px 6px {T('ACCENT_GLOW')};
}}
QPushButton:hover {{
    background: {T('ACCENT_GLOW')};
    color: {T('ACCENT_LIGHT')};
    border-color: {T('ACCENT')};
    box-shadow: 0 2px 12px {T('ACCENT_GLOW')};
}}
QPushButton:pressed {{ background: {T('ACCENT_DIM')}; border-color: {T('ACCENT')}; }}
QPushButton#accent {{
    background: {T('ACCENT')};
    color: white;
    border: none;
    padding: 9px 24px;
    font-size: 13px;
    font-weight: 700;
    border-radius: 7px;
}}
QPushButton#accent:hover {{ background: {T('ACCENT_LIGHT')}; }}
QPushButton#green {{
    background: {T('GREEN_DIM')};
    color: {T('GREEN')};
    border: 1.5px solid {T('GREEN')};
    padding: 9px 22px;
    font-size: 13px;
    font-weight: 700;
    border-radius: 7px;
}}
QPushButton#green:hover {{ background: {T('GREEN')}33; color: white; }}
QPushButton#red {{
    background: {T('RED_DIM')};
    color: {T('RED_C')};
    border: 1.5px solid {T('RED_C')};
    border-radius: 7px;
    padding: 8px 15px;
    font-weight: 600;
    font-size: 12px;
}}
QPushButton#red:hover {{ background: {T('RED_C')}33; }}
QPushButton#yellow {{
    background: {T('YELLOW_DIM')};
    color: {T('YELLOW')};
    border: 1.5px solid {T('YELLOW')};
    padding: 9px 22px;
    font-size: 13px;
    font-weight: 700;
    border-radius: 7px;
}}
QPushButton#yellow:hover {{ background: {T('YELLOW')}33; color: white; }}
QPushButton#theme_btn {{
    background: {T('BG_HOVER')};
    color: {T('TEXT_MUTED')};
    border: 1.5px solid {T('BORDER_LIGHT')};
    border-radius: 14px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    min-width: 80px;
}}
QPushButton#theme_btn:hover {{
    border-color: {T('ACCENT')};
    color: {T('ACCENT_LIGHT')};
    background: {T('ACCENT_GLOW')};
}}
QFrame#card {{
    background: {T('BG_CARD')};
    border: 1.5px solid {T('BORDER')};
    border-radius: 16px;
    box-shadow: 0 2px 16px {T('ACCENT_GLOW')};
    transition: background 0.3s, border 0.3s, box-shadow 0.3s;
}}
QFrame#netcard {{
    background: {T('NETCARD_BG')};
    border: 2px solid {T('NETCARD_BORDER')};
    border-radius: 16px;
    box-shadow: 0 2px 18px {T('ACCENT_GLOW')};
    transition: background 0.3s, border 0.3s, box-shadow 0.3s;
}}
QFrame#topbar {{
    background: {T('TOPBAR')};
    border-bottom: 2px solid {T('TOPBAR_BORDER')};
    box-shadow: 0 2px 12px {T('ACCENT_GLOW')};
    transition: background 0.3s, border 0.3s, box-shadow 0.3s;
}}
QFrame#divider_h {{
    background: {T('BORDER')};
    max-height: 1px; min-height: 1px; border: none;
}}
QFrame#divider_v {{
    background: {T('BORDER')};
    max-width: 1px; min-width: 1px; border: none;
}}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {T('BG_DARK')};
    width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {T('SCROLLBAR')};
    border-radius: 3px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {T('ACCENT')}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QStatusBar {{
    background: {T('BG_CARD')};
    color: {T('TEXT_MUTED')};
    font-size: 11px;
    border-top: 1px solid {T('BORDER')};
    padding: 3px 16px;
}}
QDialog {{ background: {T('BG_DARK')}; color: {T('TEXT_PRIMARY')}; }}
QDialogButtonBox QPushButton {{ min-width: 88px; padding: 8px 18px; }}
QAbstractItemView {{
    background: {T('BG_CARD')};
    color: {T('TEXT_PRIMARY')};
    border: 1.5px solid {T('ACCENT')};
    border-radius: 7px;
    selection-background-color: {T('ACCENT')};
    font-size: 13px;
    padding: 4px;
    outline: none;
}}
QMessageBox {{ background: {T('BG_CARD')}; }}
QMessageBox QLabel {{ color: {T('TEXT_PRIMARY')}; background: transparent; }}
QToolTip {{
    background: {T('BG_CARD')};
    color: {T('TEXT_PRIMARY')};
    border: 1px solid {T('BORDER_LIGHT')};
    border-radius: 5px;
    padding: 5px 9px;
    font-size: 11px;
}}
"""

# Fallback globals for hardcoded widget stylesheets
BG_DARK = THEMES["dark"]["BG_DARK"]
BG_CARD = THEMES["dark"]["BG_CARD"]
BG_INPUT = THEMES["dark"]["BG_INPUT"]
BG_HOVER = THEMES["dark"]["BG_HOVER"]
ACCENT = THEMES["dark"]["ACCENT"]
ACCENT_LIGHT = THEMES["dark"]["ACCENT_LIGHT"]
GREEN = THEMES["dark"]["GREEN"]
RED_C = THEMES["dark"]["RED_C"]
YELLOW = THEMES["dark"]["YELLOW"]
TEXT_PRIMARY = THEMES["dark"]["TEXT_PRIMARY"]
TEXT_MUTED = THEMES["dark"]["TEXT_MUTED"]
BORDER = THEMES["dark"]["BORDER"]

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "billing.db")

# ═══════════════════════════════════════
#  DATABASE
# ═══════════════════════════════════════
def init_db():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT, date TEXT, patient_name TEXT, patient_phone TEXT,
        patient_email TEXT, doctor TEXT,
        items TEXT, subtotal REAL, discount_pct REAL, discount_amt REAL,
        cgst REAL, sgst REAL, round_off REAL, net_amount REAL, created_at TEXT)""")
    # Migrate invoices
    existing = [row[1] for row in c.execute("PRAGMA table_info(invoices)").fetchall()]
    for col, dtype in [("discount_pct","REAL"),("discount_amt","REAL"),("round_off","REAL"),
                        ("patient_phone","TEXT"),("patient_email","TEXT")]:
        if col not in existing:
            c.execute(f"ALTER TABLE invoices ADD COLUMN {col} {dtype} DEFAULT ''")

    c.execute("""CREATE TABLE IF NOT EXISTS shop_settings (
        id INTEGER PRIMARY KEY, shop_name TEXT, store_tag TEXT, dr_name TEXT, address TEXT,
        phone TEXT, gstin TEXT, dl_no TEXT, food_lic TEXT)""")
    shop_cols = [row[1] for row in c.execute("PRAGMA table_info(shop_settings)").fetchall()]
    if 'dr_name' not in shop_cols:
        c.execute("ALTER TABLE shop_settings ADD COLUMN dr_name TEXT DEFAULT ''")
    if 'store_tag' not in shop_cols:
        c.execute("ALTER TABLE shop_settings ADD COLUMN store_tag TEXT DEFAULT ''")

    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, pack_size TEXT, hsn TEXT,
        price REAL DEFAULT 0, cgst_pct REAL DEFAULT 2.5,
        sgst_pct REAL DEFAULT 2.5, category TEXT DEFAULT '')""")

    c.execute("SELECT COUNT(*) FROM shop_settings")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO shop_settings
            (id,shop_name,store_tag,dr_name,address,phone,gstin,dl_no,food_lic)
            VALUES (1,'VIJAY HOMOEO STORES','Homoeopathic Store','Dr. Vijay Kumar',
            'C-13/31, Shopping Centre, Kaveri Path, Mansarover, Jaipur-302020',
            '0141-2393120','08ABUPJ0002E1Z2','JPR/2006/11275-11276','22218046001325')""")
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO products (name,pack_size,hsn,price,cgst_pct,sgst_pct,category) VALUES (?,?,?,?,?,?,?)", [
            ("Montana Hair Oil","200ml","33059011",180.00,2.5,2.5,"Hair Care"),
            ("Montana Herbal Shampoo","400ml","33051090",271.00,9.0,9.0,"Hair Care"),
            ("SBL Arnica Hair Oil","100ml","33059011",145.00,2.5,2.5,"Hair Care"),
            ("Calcarea Carb 30","30g","30049099",85.00,5.0,5.0,"Homoeopathy"),
            ("Nux Vomica 30","30g","30049099",85.00,5.0,5.0,"Homoeopathy"),
            ("Belladonna 200","30ml","30049099",95.00,5.0,5.0,"Homoeopathy"),
            ("Aloe Vera Gel","150g","33049900",120.00,9.0,9.0,"Skin Care"),
        ])
    conn.commit(); conn.close()

def get_shop():
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row
    c = conn.cursor(); c.execute("SELECT * FROM shop_settings WHERE id=1")
    row = c.fetchone(); conn.close()
    return dict(row) if row else {}

def next_invoice_no():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM invoices")
    n = c.fetchone()[0]; conn.close()
    return f"R-{str(n+1).zfill(6)}"

def save_invoice(d):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""INSERT INTO invoices
        (invoice_no,date,patient_name,patient_phone,patient_email,doctor,items,
         subtotal,discount_pct,discount_amt,cgst,sgst,round_off,net_amount,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (d["invoice_no"],d["date"],d["patient_name"],d.get("patient_phone",""),
         d.get("patient_email",""),d["doctor"],json.dumps(d["items"]),
         d["subtotal"],d["discount_pct"],d["discount_amt"],d["cgst"],d["sgst"],
         d["round_off"],d["net_amount"],datetime.now().isoformat()))
    conn.commit(); conn.close()

def all_invoices():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT id,invoice_no,date,patient_name,net_amount FROM invoices ORDER BY id DESC")
    r = c.fetchall(); conn.close(); return r

def invoice_by_id(inv_id):
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row
    c = conn.cursor(); c.execute("SELECT * FROM invoices WHERE id=?", (inv_id,))
    row = c.fetchone(); conn.close()
    if row:
        d = dict(row); d["items"] = json.loads(d["items"]); return d
    return None

def get_all_products():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT id,name,pack_size,hsn,price,cgst_pct,sgst_pct,category FROM products ORDER BY category,name")
    r = c.fetchall(); conn.close(); return r

def get_product_by_name(name):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT * FROM products WHERE name=? COLLATE NOCASE LIMIT 1", (name,))
    row = c.fetchone(); conn.close()
    if row: return {"id":row[0],"name":row[1],"pack_size":row[2],"hsn":row[3],
                    "price":row[4],"cgst_pct":row[5],"sgst_pct":row[6],"category":row[7]}
    return None

def add_product(name,pack_size,hsn,price,cgst,sgst,category):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("INSERT INTO products(name,pack_size,hsn,price,cgst_pct,sgst_pct,category)VALUES(?,?,?,?,?,?,?)",
              (name,pack_size,hsn,price,cgst,sgst,category))
    conn.commit(); conn.close()

def update_product(pid,name,pack_size,hsn,price,cgst,sgst,category):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("UPDATE products SET name=?,pack_size=?,hsn=?,price=?,cgst_pct=?,sgst_pct=?,category=? WHERE id=?",
              (name,pack_size,hsn,price,cgst,sgst,category,pid))
    conn.commit(); conn.close()

def delete_product(pid):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("DELETE FROM products WHERE id=?",(pid,)); conn.commit(); conn.close()

def num_words(n):
    ones=['','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten',
          'Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
    tens_=['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
    def h(n):
        if n<20: return ones[n]
        elif n<100: return tens_[n//10]+(' '+ones[n%10] if n%10 else '')
        elif n<1000: return ones[n//100]+' Hundred'+(' '+h(n%100) if n%100 else '')
        elif n<100000: return h(n//1000)+' Thousand'+(' '+h(n%1000) if n%1000 else '')
        else: return h(n//100000)+' Lakh'+(' '+h(n%100000) if n%100000 else '')
    n=int(n); return 'Zero' if n==0 else h(n)+' Only'

# ═══════════════════════════════════════
#  INVOICE HTML — redesigned 3-column header
# ═══════════════════════════════════════
INVOICE_CSS = """<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',Arial,sans-serif;font-size:10px;color:#1a1a2e;background:#fff}
.copy{padding:7px 11px 5px 11px}
.copy-label{
  display:inline-flex;align-items:center;gap:5px;
  background:#1a1a2e;color:#fff;font-size:7.5px;font-weight:800;
  letter-spacing:2px;padding:2px 10px 2px 7px;border-radius:3px;
  margin-bottom:4px;text-transform:uppercase}
.tax-banner{
  background:linear-gradient(135deg,#1a1a2e 0%,#2e2860 100%);
  color:#fff;text-align:center;padding:4px 0;font-size:9.5px;
  letter-spacing:4px;font-weight:800;border-radius:3px;margin-bottom:5px}
/* 3-column header */
.hdr{display:flex;align-items:stretch;border:1.5px solid #1a1a2e;
     border-radius:4px;margin-bottom:6px;overflow:hidden}
.hdr-left{width:32%;padding:7px 9px;border-right:1px solid #ddd;background:#f7f8ff}
.hdr-left .dr-name{font-size:11.5px;font-weight:800;color:#1a1a2e;margin-bottom:4px}
.hdr-left .lbl{font-size:7px;color:#999;text-transform:uppercase;letter-spacing:1px;font-weight:700}
.hdr-left .val{font-size:8.5px;color:#333;font-weight:600;margin-bottom:3px}
.hdr-center{flex:1;text-align:center;padding:8px 12px;display:flex;flex-direction:column;justify-content:center}
.shop-name{font-size:17px;font-weight:900;color:#1a1a2e;letter-spacing:0.5px;line-height:1.2}
.shop-tag{font-size:7.5px;color:#6666aa;letter-spacing:2px;text-transform:uppercase;margin-top:2px}
.shop-addr{font-size:8px;color:#555;margin-top:4px;line-height:1.7}
.hdr-right{width:28%;padding:7px 9px;border-left:1px solid #ddd;background:#f7f8ff;text-align:right}
.hdr-right .lbl{font-size:7px;color:#999;text-transform:uppercase;letter-spacing:1px;font-weight:700}
.hdr-right .val{font-size:10px;color:#1a1a2e;font-weight:700;margin-bottom:5px}
/* patient row */
.meta{display:flex;gap:5px;margin-bottom:5px}
.meta-box{flex:1;border:1px solid #e4e6f5;border-radius:4px;padding:4px 8px;background:#f8f9ff}
.meta-box .lbl{font-size:7.5px;color:#888;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:1px}
.meta-box .val{font-size:10px;font-weight:700;color:#1a1a2e}
.meta-box .sub{font-size:8px;color:#666;margin-top:1px}
/* table */
table{width:100%;border-collapse:collapse;margin-bottom:5px}
thead tr{background:#1a1a2e;color:#fff}
th{padding:5px 3px;font-size:7.5px;text-align:center;font-weight:700;text-transform:uppercase;letter-spacing:0.5px}
th.l{text-align:left;padding-left:6px}th.r{text-align:right;padding-right:6px}
td{border-bottom:1px solid #eef0f8;font-size:9px;padding:3px 3px;color:#222}
td.l{text-align:left;padding-left:6px}
td.r{text-align:right;padding-right:6px;font-weight:600}
td.c{text-align:center}
tbody tr:nth-child(even){background:#f5f7ff}
tbody tr:last-child td{border-bottom:1.5px solid #1a1a2e}
/* bottom */
.bottom{display:flex;gap:8px;align-items:flex-start}
.words-box{flex:1;background:#fffef0;border:1px solid #e8e0a0;border-radius:4px;padding:5px 8px}
.words-box .wlbl{font-size:7px;color:#999;text-transform:uppercase;font-weight:700;letter-spacing:1px;margin-bottom:2px}
.words-box .wval{font-size:8.5px;color:#333;font-style:italic;line-height:1.5}
.totals{min-width:195px;border:1px solid #e0e0f0;border-radius:4px;overflow:hidden}
.trow{display:flex;justify-content:space-between;padding:3px 9px;border-bottom:1px solid #f0f0f8;font-size:9px}
.trow.disc{color:#b00;background:#fff5f5}
.trow.gst{color:#145214;background:#f0fff4}
.trow.net{background:#1a1a2e;color:#fff;font-size:11.5px;font-weight:900;border:none;padding:5px 9px}
/* footer */
.footer{margin-top:5px;display:flex;justify-content:space-between;
  border-top:1px solid #ddd;padding-top:4px;font-size:7.5px;color:#666;line-height:1.7}
.sig{border-top:1px solid #555;display:inline-block;min-width:120px;
  padding-top:3px;margin-top:16px;text-align:center;font-size:7.5px}
.page-cut{border:none;border-top:1.5px dashed #bbb;margin:3px 0;
  text-align:center;font-size:7px;color:#bbb;letter-spacing:3px;padding:2px 0}
</style>"""

def _inv_body(d, shop, label=""):
    rows = ""
    for i, item in enumerate(d.get("items",[]), 1):
        pack  = item.get('pack_size','').strip()
        pname = item.get('product','')
        # Pack shown inline: "Montana Hair Oil - 200ml"
        pcell = f"{pname} <span style='color:#888;font-weight:400'>- {pack}</span>" if pack else pname
        try: qd = int(item['qty']) if float(item['qty'])==int(float(item['qty'])) else item['qty']
        except: qd = item.get('qty','')
        # Amount = qty * rate + GST on that amount
        qty   = float(item.get('qty', 0))
        rate  = float(item.get('rate', 0))
        cp    = float(item.get('cgst_pct', 0))
        sp    = float(item.get('sgst_pct', 0))
        base  = qty * rate
        gst_amt = base * (cp + sp) / 100
        total_amt = base + gst_amt
        rows += f"""<tr>
          <td class=c>{i}</td><td class=l>{pcell}</td>
          <td class=c>{item.get('hsn','')}</td><td class=c>{qd}</td>
          <td class=r>&#8377;{rate:.2f}</td>
          <td class=c>{cp}%</td>
          <td class=c>{sp}%</td>
          <td class=r>&#8377;{total_amt:.2f}</td>
        </tr>"""
    net = d.get('net_amount', 0)
    s = shop

    label_html = ""
    if label:
        icon = "📋" if "Admin" in label else "🧾"
        label_html = f'<div class="copy-label"><span>{icon}</span> {label.upper()}</div>'

    ph = d.get('patient_phone','').strip()
    pe = d.get('patient_email','').strip()

    # Build inline patient info string: Name  |  Phone (if any)  |  Email (if any)
    pat_parts = [f"Name: <b>{d.get('patient_name','—')}</b>"]
    if ph: pat_parts.append(f"Phone: {ph}")
    if pe: pat_parts.append(f"Email: {pe}")
    pat_inline = ' &nbsp;&#124;&#124;&nbsp; '.join(pat_parts)

    return f"""
<div class="copy">
  {label_html}
  <div class="tax-banner">✦ &nbsp; T A X &nbsp; I N V O I C E &nbsp; ✦</div>
  <div class="hdr">
    <div class="hdr-left">
      <div class="dr-name">{s.get('dr_name','')}</div>
      <div class="lbl">GSTIN</div>
      <div class="val">{s.get('gstin','')}</div>
      <div class="lbl">D.L. No.</div>
      <div class="val">{s.get('dl_no','')}</div>
      <div class="lbl">Food Lic.</div>
      <div class="val">{s.get('food_lic','')}</div>
    </div>
    <div class="hdr-center">
      <div class="shop-name">{s.get('shop_name','')}</div>
      <div class="shop-tag">{s.get('store_tag','')}</div>
      <div class="shop-addr">{s.get('address','')}<br>📞 {s.get('phone','')}</div>
    </div>
    <div class="hdr-right">
      <div class="lbl">Invoice No.</div>
      <div class="val">{d.get('invoice_no','—')}</div>
      <div class="lbl">Date</div>
      <div class="val">{d.get('date','—')}</div>
    </div>
  </div>
  <div class="meta">
    <div class="meta-box" style="flex:3">
      <div class="lbl">Patient Details</div>
      <div class="val" style="font-size:9.5px;font-weight:500">{pat_inline}</div>
    </div>
  </div>
  <table>
    <thead><tr>
      <th style="width:22px">#</th>
      <th class=l>Product Name</th>
      <th style="width:68px">HSN</th>
      <th style="width:30px">Qty</th>
      <th style="width:68px" class=r>Rate</th>
      <th style="width:46px">CGST%</th>
      <th style="width:46px">SGST%</th>
      <th style="width:70px" class=r>Amount</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <div class="bottom">
    <div class="words-box">
      <div class="wlbl">Amount in Words</div>
      <div class="wval">&#8377; {num_words(int(round(net)))}</div>
    </div>
    <div class="totals">
      <div class="trow"><span>Subtotal</span><span>&#8377;{d.get('subtotal',0):.2f}</span></div>
      <div class="trow disc"><span>Discount ({d.get('discount_pct',0):.1f}%)</span><span>&#8722;&#8377;{d.get('discount_amt',0):.2f}</span></div>
      <div class="trow gst"><span>CGST</span><span>&#8377;{d.get('cgst',0):.2f}</span></div>
      <div class="trow gst"><span>SGST</span><span>&#8377;{d.get('sgst',0):.2f}</span></div>
      <div class="trow"><span>Round Off</span><span>&#8377;{d.get('round_off',0):.2f}</span></div>
      <div class="trow net"><span>NET AMOUNT</span><span>&#8377;{net:.2f}</span></div>
    </div>
  </div>
  <div class="footer">
    <div>
      <b>Terms &amp; Conditions</b><br>
      &bull; Goods once sold will not be taken back.<br>
      &bull; Bills not paid by due date attract 24% interest.<br>
      &bull; All disputes subject to local jurisdiction.
    </div>
    <div style="text-align:right">
      <div class="sig">Authorised Signatory<br><b>For {s.get('shop_name','')}</b></div>
    </div>
  </div>
</div>"""

def build_preview_html(d, shop):
    return f"""<html><head><meta charset='utf-8'>{INVOICE_CSS}
    <style>
    body{{background:#d8dae8;margin:0;padding:20px}}
    .page{{background:#fff;max-width:750px;margin:0 auto;
           box-shadow:0 6px 30px rgba(0,0,0,0.22);border-radius:5px}}
    </style>
    </head><body><div class="page">{_inv_body(d,shop)}</div></body></html>"""

def build_dual_html(d, shop):
    """Both Admin + Customer copies on one A4 — compact CSS overrides"""
    return f"""<html><head><meta charset='utf-8'>{INVOICE_CSS}
    <style>
    @page{{size:A4;margin:4mm 5mm}}
    body{{margin:0;padding:0;background:#fff}}
    .copy{{padding:5px 8px 3px 8px}}
    .shop-name{{font-size:14px}}
    .shop-addr{{font-size:7.5px;margin-top:3px}}
    .tax-banner{{font-size:8.5px;padding:3px 0;letter-spacing:3px}}
    .hdr-left .dr-name{{font-size:10px}}
    .hdr-left .lbl,.hdr-right .lbl{{font-size:6.5px}}
    .hdr-left .val,.hdr-right .val{{font-size:8px;margin-bottom:2px}}
    th{{font-size:7px;padding:4px 2px}}
    td{{font-size:8.5px;padding:2.5px 2px}}
    .meta-box .val{{font-size:9px}}
    .meta-box .lbl{{font-size:7px}}
    .trow{{font-size:8.5px;padding:2.5px 8px}}
    .trow.net{{font-size:10.5px;padding:4px 8px}}
    .words-box .wval{{font-size:8px}}
    .words-box .wlbl{{font-size:6.5px}}
    .footer{{font-size:6.5px;margin-top:4px;padding-top:3px}}
    .sig{{margin-top:12px;min-width:100px;font-size:7px}}
    .copy-label{{font-size:7px;padding:1.5px 8px 1.5px 6px}}
    </style>
    </head><body>
    {_inv_body(d,shop,'Admin Copy')}
    <div class="page-cut">&mdash; &mdash; &mdash; CUT HERE &mdash; &mdash; &mdash;</div>
    {_inv_body(d,shop,'Customer Copy')}
    </body></html>"""

# ═══════════════════════════════════════
#  HELPER WIDGETS
# ═══════════════════════════════════════
def mk_section(txt):
    l = QLabel(txt.upper())
    l.setStyleSheet(f"color:{T('TEXT_MUTED')};font-size:10px;font-weight:700;"
                    f"letter-spacing:1.2px;background:transparent;margin-bottom:1px")
    return l

def pill(txt, color=None, bg=None):
    if color is None: color = T('ACCENT')
    if bg is None: bg = color + "22"
    l = QLabel(txt)
    l.setStyleSheet(f"color:{color};background:{bg};border:1px solid {color}44;"
                    f"border-radius:9px;padding:2px 10px;font-size:10px;font-weight:700")
    l.setFixedHeight(22)
    return l

# ═══════════════════════════════════════
#  PREVIEW DIALOG
# ═══════════════════════════════════════
class PreviewDialog(QDialog):
    def __init__(self, html, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Invoice Preview")
        self.setWindowFlags(Qt.WindowType.Dialog |
                            Qt.WindowType.WindowMaximizeButtonHint |
                            Qt.WindowType.WindowCloseButtonHint)
        self.resize(820, 920)
        self.setStyleSheet(f"background:{T('BG_DARK')};")
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0); l.setSpacing(0)

        bar = QFrame(); bar.setObjectName("topbar"); bar.setFixedHeight(50)
        bl = QHBoxLayout(bar); bl.setContentsMargins(18,0,18,0); bl.setSpacing(10)
        icon = QLabel("◈"); icon.setStyleSheet(f"color:{T('ACCENT')};font-size:18px;background:transparent")
        ttl  = QLabel("Invoice Preview")
        ttl.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-weight:700;font-size:14px;background:transparent")
        hint = QLabel("Single copy preview  ·  PDF export has both copies")
        hint.setStyleSheet(f"color:{T('TEXT_MUTED')};font-size:11px;background:transparent")
        btn_close = QPushButton("✕  Close"); btn_close.setFixedWidth(90); btn_close.setFixedHeight(30)
        btn_close.clicked.connect(self.close)
        bl.addWidget(icon); bl.addSpacing(6); bl.addWidget(ttl); bl.addStretch()
        bl.addWidget(hint); bl.addSpacing(14); bl.addWidget(btn_close)
        l.addWidget(bar)

        self.web = QWebEngineView()
        self.web.setHtml(html)
        l.addWidget(self.web)

# ═══════════════════════════════════════
#  BILLING TAB
# ═══════════════════════════════════════
class BillingTab(QWidget):
    invoice_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.shop = get_shop()
        self._current_data = {}
        self._build_ui()
        self._reset()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 14, 20, 12)
        root.setSpacing(10)

        # ── Title row ─────────────────────────────────────────
        title_row = QHBoxLayout(); title_row.setSpacing(8)
        icon = QLabel("◈")
        icon.setStyleSheet(f"color:{T('ACCENT')};font-size:17px;background:transparent;font-weight:900")
        title = QLabel("New Invoice")
        title.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-size:18px;font-weight:800;background:transparent")
        title_row.addWidget(icon); title_row.addSpacing(4); title_row.addWidget(title); title_row.addStretch()
        self.inv_badge = QLabel("R-000001")
        self.inv_badge.setStyleSheet(
            f"color:{T('GREEN')};font-size:13px;font-weight:800;"
            f"background:{T('BG_CARD')};border:1.5px solid {T('GREEN')}44;"
            f"border-radius:7px;padding:4px 14px;letter-spacing:0.5px")
        title_row.addWidget(self.inv_badge)
        root.addLayout(title_row)

        # ── Patient card ──────────────────────────────────────
        pcard = QFrame(); pcard.setObjectName("card")
        pg = QGridLayout(pcard); pg.setContentsMargins(16,13,16,13); pg.setSpacing(8)
        pg.setColumnStretch(0,4); pg.setColumnStretch(1,2); pg.setColumnStretch(2,3); pg.setColumnStretch(3,2)

        self.patient_edit = QLineEdit(); self.patient_edit.setPlaceholderText("Patient / Customer name")
        self.phone_edit   = QLineEdit(); self.phone_edit.setPlaceholderText("Phone number")
        self.email_edit   = QLineEdit(); self.email_edit.setPlaceholderText("Email (optional)")
        self.date_edit    = QLineEdit(); self.date_edit.setFixedWidth(115)
        self.invoice_no   = ""

        pg.addWidget(mk_section("Patient Name"), 0, 0)
        pg.addWidget(mk_section("Phone"),         0, 1)
        pg.addWidget(mk_section("Email"),         0, 2)
        pg.addWidget(mk_section("Date"),          0, 3)
        pg.addWidget(self.patient_edit, 1, 0)
        pg.addWidget(self.phone_edit,   1, 1)
        pg.addWidget(self.email_edit,   1, 2)
        pg.addWidget(self.date_edit,    1, 3)
        root.addWidget(pcard)

        # ── Items row header ──────────────────────────────────
        items_hdr = QHBoxLayout(); items_hdr.setSpacing(8)
        items_lbl = QLabel("BILL ITEMS")
        items_lbl.setStyleSheet(
            f"color:{T('TEXT_MUTED')};font-size:10px;font-weight:700;"
            f"letter-spacing:1.5px;background:transparent")
        items_hdr.addWidget(items_lbl); items_hdr.addStretch()
        btn_add_row = QPushButton("＋  Add Item")
        btn_del_row = QPushButton("✕  Remove"); btn_del_row.setObjectName("red")
        btn_add_row.setFixedHeight(30); btn_del_row.setFixedHeight(30)
        btn_add_row.clicked.connect(lambda: self._add_row())
        btn_del_row.clicked.connect(self._del_row)
        items_hdr.addWidget(btn_add_row); items_hdr.addWidget(btn_del_row)
        root.addLayout(items_hdr)

        # ── Items table ───────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["#","Product Name","Pack","HSN","Qty","Rate (₹)","CGST %","SGST %"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for col in [0,2,3,4,5,6,7]: hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0,32); self.table.setColumnWidth(2,72)
        self.table.setColumnWidth(3,84); self.table.setColumnWidth(4,46)
        self.table.setColumnWidth(5,88); self.table.setColumnWidth(6,66); self.table.setColumnWidth(7,66)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(148)
        self.table.setMaximumHeight(232)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.itemChanged.connect(lambda _: self._recalc())
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table)

        # ── Totals + Net (side by side) ───────────────────────
        bot = QHBoxLayout(); bot.setSpacing(10)

        tcard = QFrame(); tcard.setObjectName("card")
        tg = QGridLayout(tcard); tg.setContentsMargins(14,11,14,11); tg.setSpacing(8)
        self.subtotal_f = QLineEdit("0.00"); self.subtotal_f.setReadOnly(True)
        self.disc_edit  = QLineEdit("10.0"); self.disc_edit.setPlaceholderText("%")
        self.disc_edit.textChanged.connect(self._recalc)
        self.disc_amt_f = QLineEdit("0.00"); self.disc_amt_f.setReadOnly(True)
        self.cgst_f     = QLineEdit("0.00"); self.cgst_f.setReadOnly(True)
        self.sgst_f     = QLineEdit("0.00"); self.sgst_f.setReadOnly(True)
        disc_lyt = QHBoxLayout(); disc_lyt.setSpacing(3); disc_lyt.setContentsMargins(0,0,0,0)
        disc_lyt.addWidget(self.disc_edit)
        pct_l = QLabel("%"); pct_l.setStyleSheet(f"color:{T('TEXT_MUTED')};background:transparent;font-size:13px")
        disc_lyt.addWidget(pct_l); disc_lyt.addStretch()
        for col,lbl in enumerate(["Subtotal","Discount","Disc. Amount","CGST Total","SGST Total"]):
            tg.addWidget(mk_section(lbl),0,col)
        tg.addWidget(self.subtotal_f,1,0); tg.addLayout(disc_lyt,1,1)
        tg.addWidget(self.disc_amt_f,1,2); tg.addWidget(self.cgst_f,1,3); tg.addWidget(self.sgst_f,1,4)
        bot.addWidget(tcard,3)

        netcard = QFrame(); netcard.setObjectName("netcard")
        nl = QVBoxLayout(netcard); nl.setContentsMargins(16,10,16,10); nl.setSpacing(2)
        net_lbl = QLabel("NET AMOUNT")
        net_lbl.setStyleSheet(f"font-size:9px;font-weight:700;color:{T('TEXT_MUTED')};"
                               f"letter-spacing:2.5px;background:transparent")
        net_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.net_display = QLabel("₹ 0.00")
        self.net_display.setStyleSheet(
            f"font-size:24px;font-weight:900;color:{T('ACCENT_LIGHT')};background:transparent")
        self.net_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nl.addWidget(net_lbl); nl.addWidget(self.net_display)
        bot.addWidget(netcard,1)
        root.addLayout(bot)

        # ── Action buttons ────────────────────────────────────
        abr = QHBoxLayout(); abr.setSpacing(8)
        btn_new     = QPushButton("＋  New Invoice")
        btn_preview = QPushButton("◉  Preview");      btn_preview.setObjectName("accent")
        btn_save    = QPushButton("✔  Save Invoice");  btn_save.setObjectName("green")
        btn_pdf     = QPushButton("⬇  Export PDF");    btn_pdf.setObjectName("yellow")
        btn_print   = QPushButton("⎙  Print")
        for b in [btn_new,btn_preview,btn_save,btn_pdf,btn_print]: b.setFixedHeight(36)
        btn_new.setToolTip("Clear and start a new invoice")
        btn_pdf.setToolTip("Export both Admin & Customer copies as one PDF")
        btn_new.clicked.connect(self._reset)
        btn_preview.clicked.connect(self._preview)
        btn_save.clicked.connect(self._save)
        btn_pdf.clicked.connect(self._export_pdf)
        btn_print.clicked.connect(self._print)
        abr.addWidget(btn_new); abr.addStretch()
        abr.addWidget(btn_preview); abr.addWidget(btn_save)
        abr.addWidget(btn_pdf); abr.addWidget(btn_print)
        root.addLayout(abr)

    # ── Helpers ──────────────────────────────────────────────
    def _add_row(self, data=None):
        self.table.blockSignals(True)
        r = self.table.rowCount(); self.table.insertRow(r)

        sr = QTableWidgetItem(str(r+1))
        sr.setFlags(Qt.ItemFlag.ItemIsEnabled)
        sr.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        sr.setForeground(QColor(T('TEXT_MUTED')))
        self.table.setItem(r, 0, sr)

        prod_edit = QLineEdit()
        prod_edit.setStyleSheet(
            f"background:{T('BG_INPUT')};border:none;color:{T('TEXT_PRIMARY')};"
            f"font-size:13px;padding:5px 10px;border-radius:0")
        names = [p[1] for p in get_all_products()]
        comp = QCompleter(names, prod_edit)
        comp.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        comp.setFilterMode(Qt.MatchFlag.MatchContains)
        prod_edit.setCompleter(comp)

        def fill(name, row=r):
            p = get_product_by_name(name)
            if p:
                self.table.blockSignals(True)
                self._sc(row,2,p.get("pack_size",""))
                self._sc(row,3,p.get("hsn",""))
                self._sc(row,4,"1")
                self._sc(row,5,str(p.get("price",0)))
                self._sc(row,6,str(p.get("cgst_pct",2.5)))
                self._sc(row,7,str(p.get("sgst_pct",2.5)))
                self.table.blockSignals(False)
                self._recalc()

        prod_edit.textChanged.connect(lambda t: fill(t) if get_product_by_name(t) else None)
        comp.activated.connect(fill)
        self.table.setCellWidget(r, 1, prod_edit)

        for c, v in enumerate(["","","1","0","2.5","2.5"], 2):
            it = QTableWidgetItem(v); it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, c, it)

        if data:
            prod_edit.setText(data.get("product",""))
            self._sc(r,2,data.get("pack_size",""))
            self._sc(r,3,data.get("hsn",""))
            self._sc(r,4,str(data.get("qty",1)))
            self._sc(r,5,str(data.get("rate",0)))
            self._sc(r,6,str(data.get("cgst_pct",2.5)))
            self._sc(r,7,str(data.get("sgst_pct",2.5)))

        self.table.setRowHeight(r,38); self.table.blockSignals(False); self._recalc()

    def _sc(self, r, c, val):
        it = self.table.item(r, c)
        if it: it.setText(str(val))
        else:
            it = QTableWidgetItem(str(val)); it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, c, it)

    def _del_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
            for i in range(self.table.rowCount()):
                self.table.item(i,0).setText(str(i+1))
            self._recalc()

    def _collect(self):
        self.table.blockSignals(True)
        items=[]; sub=0; ct=0; st=0
        for r in range(self.table.rowCount()):
            w = self.table.cellWidget(r,1); pname = w.text() if w else ""
            def cell(c, row=r):
                it = self.table.item(row,c); return it.text() if it else ""
            try: qty=float(cell(4))
            except: qty=0
            try: rate=float(cell(5))
            except: rate=0
            try: cp=float(cell(6))
            except: cp=0
            try: sp=float(cell(7))
            except: sp=0
            base=qty*rate
            cgst_item=base*cp/100; sgst_item=base*sp/100
            amt=base+cgst_item+sgst_item   # GST-inclusive per item
            ct+=cgst_item; st+=sgst_item; sub+=base
            items.append({"product":pname,"pack_size":cell(2),"hsn":cell(3),
                          "qty":qty,"rate":rate,"cgst_pct":cp,"sgst_pct":sp,"amount":amt})
        try: dp=max(0.0,min(100.0,float(self.disc_edit.text())))
        except: dp=0.0
        da=sub*dp/100; after=sub-da
        ratio=after/sub if sub else 0; ct*=ratio; st*=ratio
        net_raw=after+ct+st; netr=round(net_raw); ro=netr-net_raw
        self.table.blockSignals(False)
        return {
            "invoice_no":    self.invoice_no,
            "date":          self.date_edit.text(),
            "patient_name":  self.patient_edit.text(),
            "patient_phone": self.phone_edit.text(),
            "patient_email": self.email_edit.text(),
            "doctor":        self.shop.get("dr_name",""),
            "items": items,
            "subtotal":     round(sub,2), "discount_pct":dp,
            "discount_amt": round(da,2),  "cgst":round(ct,2),
            "sgst":         round(st,2),  "round_off":round(ro,2),
            "net_amount":   float(netr)
        }

    def _recalc(self):
        d = self._collect(); self._current_data = d
        self.subtotal_f.setText(f"{d['subtotal']:.2f}")
        self.disc_amt_f.setText(f"{d['discount_amt']:.2f}")
        self.cgst_f.setText(f"{d['cgst']:.2f}")
        self.sgst_f.setText(f"{d['sgst']:.2f}")
        self.net_display.setText(f"₹ {d['net_amount']:.2f}")

    def _reset(self):
        self.table.blockSignals(True); self.table.setRowCount(0); self.table.blockSignals(False)
        self.patient_edit.clear(); self.phone_edit.clear(); self.email_edit.clear()
        self.invoice_no = next_invoice_no()
        self.inv_badge.setText(self.invoice_no)
        self.date_edit.setText(datetime.now().strftime("%d-%m-%Y"))
        self.disc_edit.setText("10.0")
        self._add_row(); self._recalc()

    def _preview(self):
        d = self._collect()
        dlg = PreviewDialog(build_preview_html(d, self.shop), self)
        dlg.exec()

    def _save(self):
        d = self._collect()
        if not d["patient_name"].strip():
            QMessageBox.warning(self,"Missing Info","Please enter patient name."); return
        save_invoice(d)
        QMessageBox.information(self,"✔  Saved",f"Invoice {d['invoice_no']} saved!")
        self.invoice_saved.emit(); self._reset()

    def _export_pdf(self):
        d = self._collect()
        path,_ = QFileDialog.getSaveFileName(self,"Export PDF — Both Copies on A4",
            f"Invoice_{d['invoice_no'].replace('/','-')}.pdf","PDF Files (*.pdf)")
        if not path: return
        self._pdf_path = path
        self._pdf_web = QWebEngineView()
        self._pdf_web.loadFinished.connect(lambda ok: self._render_pdf())
        self._pdf_web.setHtml(build_dual_html(d, self.shop))

    def _render_pdf(self):
        layout = QPageLayout(QPageSize(QPageSize.PageSizeId.A4),
                             QPageLayout.Orientation.Portrait, QMarginsF(4,4,4,4))
        def _done(path):
            QMessageBox.information(self,"✔  PDF Exported",
                f"Saved — Admin + Customer on one A4:\n{self._pdf_path}")
            try:
                if platform.system()=="Windows": os.startfile(self._pdf_path)
                elif platform.system()=="Darwin": os.system(f'open "{self._pdf_path}"')
            except: pass
        self._pdf_web.printToPdf(self._pdf_path, layout)
        self._pdf_web.pdfPrintingFinished.connect(_done)

    def _print(self):
        d = self._collect()
        self._print_web = QWebEngineView()
        self._print_web.loadFinished.connect(self._do_print)
        self._print_web.setHtml(build_dual_html(d, self.shop))

    def _do_print(self):
        layout = QPageLayout(QPageSize(QPageSize.PageSizeId.A4),
                             QPageLayout.Orientation.Portrait, QMarginsF(4,4,4,4))
        tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)),"_print_tmp.pdf")
        def _open(path):
            try:
                if platform.system()=="Windows": os.startfile(tmp)
                elif platform.system()=="Darwin": os.system(f'open "{tmp}"')
                else: os.system(f'xdg-open "{tmp}"')
            except: pass
        self._print_web.printToPdf(tmp, layout)
        self._print_web.pdfPrintingFinished.connect(_open)

    def load_invoice(self, d):
        self.table.blockSignals(True); self.table.setRowCount(0); self.table.blockSignals(False)
        self.patient_edit.setText(d.get("patient_name",""))
        self.phone_edit.setText(d.get("patient_phone",""))
        self.email_edit.setText(d.get("patient_email",""))
        self.invoice_no = d.get("invoice_no","")
        self.inv_badge.setText(self.invoice_no)
        self.date_edit.setText(d.get("date",""))
        self.disc_edit.setText(str(d.get("discount_pct",10.0)))
        for item in d.get("items",[]): self._add_row(item)
        self._recalc()

    def refresh_shop(self): self.shop = get_shop()

# ═══════════════════════════════════════
#  PRODUCT CATALOGUE
# ═══════════════════════════════════════
class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product" if product else "Add Product")
        self.setMinimumWidth(440)
        l = QVBoxLayout(self); l.setSpacing(14); l.setContentsMargins(22,20,22,20)

        hdr = QHBoxLayout()
        icon = QLabel("◈"); icon.setStyleSheet(f"color:{T('ACCENT')};font-size:16px;background:transparent")
        title = QLabel("Edit Product" if product else "Add New Product")
        title.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-size:15px;font-weight:800;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(7); hdr.addWidget(title)
        l.addLayout(hdr)

        card = QFrame(); card.setObjectName("card")
        g = QGridLayout(card); g.setContentsMargins(16,16,16,16); g.setSpacing(10)
        self.name_e  = QLineEdit(); self.name_e.setPlaceholderText("e.g. Montana Hair Oil")
        self.pack_e  = QLineEdit(); self.pack_e.setPlaceholderText("e.g. 200ml, 30g")
        self.hsn_e   = QLineEdit(); self.hsn_e.setPlaceholderText("e.g. 33059011")
        self.price_e = QDoubleSpinBox(); self.price_e.setRange(0,999999); self.price_e.setDecimals(2); self.price_e.setPrefix("₹ ")
        self.cgst_e  = QDoubleSpinBox(); self.cgst_e.setRange(0,28); self.cgst_e.setDecimals(2); self.cgst_e.setSuffix(" %")
        self.sgst_e  = QDoubleSpinBox(); self.sgst_e.setRange(0,28); self.sgst_e.setDecimals(2); self.sgst_e.setSuffix(" %")
        self.cat_e   = QLineEdit(); self.cat_e.setPlaceholderText("e.g. Hair Care, Homoeopathy")
        if product:
            self.name_e.setText(product.get("name","")); self.pack_e.setText(product.get("pack_size",""))
            self.hsn_e.setText(product.get("hsn","")); self.price_e.setValue(product.get("price",0))
            self.cgst_e.setValue(product.get("cgst_pct",2.5)); self.sgst_e.setValue(product.get("sgst_pct",2.5))
            self.cat_e.setText(product.get("category",""))
        for i,(lb,w) in enumerate([("PRODUCT NAME *",self.name_e),("PACK SIZE",self.pack_e),
                                    ("HSN CODE",self.hsn_e),("PRICE / MRP",self.price_e),
                                    ("CGST %",self.cgst_e),("SGST %",self.sgst_e),("CATEGORY",self.cat_e)]):
            g.addWidget(mk_section(lb),i,0); g.addWidget(w,i,1)
        l.addWidget(card)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        btns.button(QDialogButtonBox.StandardButton.Save).setObjectName("accent")
        btns.accepted.connect(self._ok); btns.rejected.connect(self.reject)
        l.addWidget(btns)

    def _ok(self):
        if not self.name_e.text().strip():
            QMessageBox.warning(self,"Required","Product name is required."); return
        self.accept()

    def get_data(self):
        return {"name":self.name_e.text().strip(),"pack_size":self.pack_e.text().strip(),
                "hsn":self.hsn_e.text().strip(),"price":self.price_e.value(),
                "cgst_pct":self.cgst_e.value(),"sgst_pct":self.sgst_e.value(),
                "category":self.cat_e.text().strip()}

class CatalogueTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(20,18,20,18); l.setSpacing(12)
        hdr = QHBoxLayout()
        icon = QLabel("✦"); icon.setStyleSheet(f"color:{T('ACCENT')};font-size:17px;background:transparent")
        title = QLabel("Product Catalogue")
        title.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-size:17px;font-weight:700;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(8); hdr.addWidget(title); hdr.addStretch()
        l.addLayout(hdr)
        sub = QLabel("Manage medicines & products — they auto-fill in the billing form when you type.")
        sub.setStyleSheet(f"color:{T('TEXT_MUTED')};font-size:12px;background:transparent")
        sub.setWordWrap(True); l.addWidget(sub)
        top = QHBoxLayout(); top.setSpacing(8)
        self.search = QLineEdit(); self.search.setPlaceholderText("🔍  Search by name, HSN, or category…")
        self.search.textChanged.connect(self._filter)
        btn_add  = QPushButton("＋  Add");   btn_add.setObjectName("accent")
        btn_edit = QPushButton("✏  Edit");   btn_edit.setObjectName("green")
        btn_del  = QPushButton("🗑  Delete"); btn_del.setObjectName("red")
        btn_add.clicked.connect(self._add); btn_edit.clicked.connect(self._edit); btn_del.clicked.connect(self._delete)
        for b in [btn_add,btn_edit,btn_del]: b.setFixedHeight(34)
        top.addWidget(self.search); top.addWidget(btn_add); top.addWidget(btn_edit); top.addWidget(btn_del)
        l.addLayout(top)
        self.table = QTableWidget(); self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID","Product Name","Pack Size","HSN","Price (₹)","CGST %","SGST %","Category"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0,40); self.table.setColumnWidth(2,80); self.table.setColumnWidth(3,90)
        self.table.setColumnWidth(4,90); self.table.setColumnWidth(5,70); self.table.setColumnWidth(6,70)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False); self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit)
        l.addWidget(self.table); self._all=[]; self.load()

    def load(self): self._all=get_all_products(); self._show(self._all)

    def _show(self, data):
        self.table.setRowCount(len(data))
        for r,p in enumerate(data):
            for c,v in enumerate(p):
                if c==4: txt=f"{float(v):.2f}"
                elif c in(5,6): txt=f"{float(v):.2f}%"
                else: txt=str(v)
                it=QTableWidgetItem(txt)
                align=Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter if c==1 else Qt.AlignmentFlag.AlignCenter
                it.setTextAlignment(align)
                if c==4: it.setForeground(QColor(GREEN))
                elif c in(5,6): it.setForeground(QColor(YELLOW))
                self.table.setItem(r,c,it)
            self.table.setRowHeight(r,36)

    def _filter(self,txt):
        txt=txt.lower()
        self._show([p for p in self._all if txt in p[1].lower() or txt in(p[3]or'').lower() or txt in(p[7]or'').lower()])

    def _add(self):
        dlg=ProductDialog(self)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            d=dlg.get_data(); add_product(d["name"],d["pack_size"],d["hsn"],d["price"],d["cgst_pct"],d["sgst_pct"],d["category"]); self.load()

    def _edit(self):
        row=self.table.currentRow()
        if row<0: QMessageBox.information(self,"Select","Please select a product to edit."); return
        pid=int(self.table.item(row,0).text())
        prod=next((p for p in self._all if p[0]==pid),None)
        if not prod: return
        p={"id":prod[0],"name":prod[1],"pack_size":prod[2],"hsn":prod[3],"price":prod[4],"cgst_pct":prod[5],"sgst_pct":prod[6],"category":prod[7]}
        dlg=ProductDialog(self,p)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            d=dlg.get_data(); update_product(pid,d["name"],d["pack_size"],d["hsn"],d["price"],d["cgst_pct"],d["sgst_pct"],d["category"]); self.load()

    def _delete(self):
        row=self.table.currentRow()
        if row<0: QMessageBox.information(self,"Select","Please select a product."); return
        name=self.table.item(row,1).text(); pid=int(self.table.item(row,0).text())
        if QMessageBox.question(self,"Confirm Delete",f"Delete '{name}'?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)==QMessageBox.StandardButton.Yes:
            delete_product(pid); self.load()

# ═══════════════════════════════════════
#  HISTORY TAB
# ═══════════════════════════════════════
class HistoryTab(QWidget):
    open_invoice=pyqtSignal(dict)
    def __init__(self,parent=None):
        super().__init__(parent)
        l=QVBoxLayout(self); l.setContentsMargins(20,18,20,18); l.setSpacing(12)
        hdr=QHBoxLayout()
        icon=QLabel("⊞"); icon.setStyleSheet(f"color:{T('ACCENT')};font-size:17px;background:transparent")
        title=QLabel("Invoice History"); title.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-size:17px;font-weight:700;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(8); hdr.addWidget(title); hdr.addStretch()
        l.addLayout(hdr)
        top=QHBoxLayout(); top.setSpacing(8)
        self.search=QLineEdit(); self.search.setPlaceholderText("🔍  Search by patient name or invoice number…")
        self.search.textChanged.connect(self._filter)
        btn_r=QPushButton("↺  Refresh"); btn_r.setFixedHeight(34); btn_r.clicked.connect(self.load_data)
        btn_o=QPushButton("⤴  Open Invoice"); btn_o.setObjectName("accent"); btn_o.setFixedHeight(34); btn_o.clicked.connect(self._open)
        top.addWidget(self.search); top.addWidget(btn_r); top.addWidget(btn_o)
        l.addLayout(top)
        self.table=QTableWidget(); self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Invoice No.","Date","Patient Name","Net Amount"])
        self.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False); self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._open)
        l.addWidget(self.table); self._data=[]; self.load_data()

    def load_data(self): self._data=all_invoices(); self._show(self._data)
    def _show(self,data):
        self.table.setRowCount(len(data))
        for r,inv in enumerate(data):
            for c,v in enumerate(inv):
                t=f"₹ {float(v):.2f}" if c==4 else str(v)
                it=QTableWidgetItem(t); it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if c==4: it.setForeground(QColor(GREEN))
                self.table.setItem(r,c,it)
            self.table.setRowHeight(r,36)
    def _filter(self,txt):
        txt=txt.lower()
        self._show([x for x in self._data if txt in str(x[1]).lower() or txt in str(x[3]).lower()])
    def _open(self):
        row=self.table.currentRow()
        if row<0: return
        d=invoice_by_id(int(self.table.item(row,0).text()))
        if d: self.open_invoice.emit(d)

# ═══════════════════════════════════════
#  SETTINGS TAB
# ═══════════════════════════════════════
class SettingsTab(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        l=QVBoxLayout(self); l.setContentsMargins(20,18,20,18)
        l.setAlignment(Qt.AlignmentFlag.AlignTop); l.setSpacing(14)
        hdr=QHBoxLayout()
        icon=QLabel("⚙"); icon.setStyleSheet(f"color:{T('ACCENT')};font-size:17px;background:transparent")
        title=QLabel("Shop Settings"); title.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-size:17px;font-weight:700;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(8); hdr.addWidget(title); hdr.addStretch()
        l.addLayout(hdr)
        note=QLabel("These details appear on every invoice. Doctor name auto-fills as 'Ref. Doctor' on each bill.")
        note.setStyleSheet(f"color:{T('TEXT_MUTED')};font-size:12px;background:transparent"); l.addWidget(note)
        card=QFrame(); card.setObjectName("card"); card.setMaximumWidth(600)
        g=QGridLayout(card); g.setContentsMargins(20,18,20,18); g.setSpacing(12)
        self.fields={}; s=get_shop()
        for i,(k,lb) in enumerate([("shop_name","SHOP NAME"),("store_tag","STORE TAG (e.g. Homoeopathic Store)"),
                                    ("dr_name","DOCTOR / PROPRIETOR NAME"),
                                    ("address","ADDRESS"),("phone","PHONE"),
                                    ("gstin","GSTIN"),("dl_no","D.L. NO."),("food_lic","FOOD LIC.")]):
            g.addWidget(mk_section(lb),i,0); f=QLineEdit(s.get(k,"")); self.fields[k]=f; g.addWidget(f,i,1)
        l.addWidget(card)
        btn=QPushButton("✔  Save Settings"); btn.setObjectName("accent")
        btn.setFixedWidth(180); btn.setFixedHeight(36); btn.clicked.connect(self._save); l.addWidget(btn)

    def _save(self):
        conn=sqlite3.connect(DB_PATH); c=conn.cursor()
        c.execute("UPDATE shop_settings SET shop_name=?,store_tag=?,dr_name=?,address=?,phone=?,gstin=?,dl_no=?,food_lic=? WHERE id=1",
            tuple(self.fields[k].text() for k in ["shop_name","store_tag","dr_name","address","phone","gstin","dl_no","food_lic"]))
        conn.commit(); conn.close()
        QMessageBox.information(self,"✔  Saved","Settings saved successfully!")

# ═══════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing App — Vijay Homoeo Stores")
        self._is_dark = True
        self._build()

    def _build(self):
        central = QWidget()
        cl = QVBoxLayout(central); cl.setContentsMargins(0,0,0,0); cl.setSpacing(0)

        # ── Top bar ─────────────────────────────────────
        topbar = QFrame(); topbar.setObjectName("topbar"); topbar.setFixedHeight(52)
        tbl = QHBoxLayout(topbar); tbl.setContentsMargins(20,0,20,0); tbl.setSpacing(10)

        dot = QLabel("◈")
        dot.setStyleSheet(f"color:{T('ACCENT')};font-size:20px;font-weight:900;background:transparent")
        app_title = QLabel("Billing App")
        app_title.setStyleSheet(f"color:{T('TEXT_PRIMARY')};font-size:16px;font-weight:800;background:transparent")

        divv = QFrame(); divv.setObjectName("divider_v"); divv.setFixedSize(1,22)
        shop_lbl = QLabel(get_shop().get("shop_name",""))
        shop_lbl.setStyleSheet(f"color:{T('TEXT_MUTED')};font-size:11px;background:transparent")

        tbl.addWidget(dot); tbl.addSpacing(3); tbl.addWidget(app_title)
        tbl.addSpacing(8); tbl.addWidget(divv); tbl.addSpacing(8); tbl.addWidget(shop_lbl)
        tbl.addStretch()

        self.theme_btn = QPushButton("☀  Light")
        self.theme_btn.setObjectName("theme_btn"); self.theme_btn.setFixedHeight(28)
        self.theme_btn.clicked.connect(self._toggle_theme)
        tbl.addWidget(self.theme_btn); tbl.addSpacing(4)

        v_lbl = QLabel("v3.0")
        v_lbl.setStyleSheet(
            f"color:{T('GREEN')};background:{T('GREEN')}18;border:1px solid {T('GREEN')}44;"
            f"border-radius:8px;padding:2px 9px;font-size:10px;font-weight:700")
        tbl.addWidget(v_lbl)
        cl.addWidget(topbar)

        # ── Tabs ─────────────────────────────────────────
        self.tabs = QTabWidget()
        self.bt  = BillingTab()
        self.ht  = HistoryTab()
        self.cat = CatalogueTab()
        self.st  = SettingsTab()
        self.tabs.addTab(self.bt,  "  ◈  New Invoice  ")
        self.tabs.addTab(self.ht,  "  ⊞  History  ")
        self.tabs.addTab(self.cat, "  ✦  Catalogue  ")
        self.tabs.addTab(self.st,  "  ⚙  Settings  ")
        cl.addWidget(self.tabs)

        self.bt.invoice_saved.connect(self.ht.load_data)
        self.ht.open_invoice.connect(lambda d: (self.bt.load_invoice(d), self.tabs.setCurrentIndex(0)))
        self.tabs.currentChanged.connect(lambda i: self.bt.refresh_shop() if i==0 else None)
        self.setCentralWidget(central)

        sb = QStatusBar()
        sb.showMessage(f"  ◈  Ready  ·  Dr. name fills from Settings  ·  "
                       f"PDF = Admin + Customer on one A4  ·  {get_shop().get('shop_name','')}")
        self.setStatusBar(sb)

    def _toggle_theme(self):
        global _CURRENT_THEME
        self._is_dark = not self._is_dark
        _CURRENT_THEME = "dark" if self._is_dark else "light"
        QApplication.instance().setStyleSheet(build_stylesheet())
        self.theme_btn.setText("☀  Light" if self._is_dark else "🌙  Dark")

def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(build_stylesheet())
    win = MainWindow()
    win.showMaximized()   # open full screen on launch
    sys.exit(app.exec())

if __name__ == "__main__":
    main()