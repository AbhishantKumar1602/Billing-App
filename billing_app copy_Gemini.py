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
#  MINIMALIST WHITE THEME
# ════════════════════════════════════════════════
BG        = "#f8f9fa"     # page background — very light grey
BG_CARD   = "#ffffff"     # cards / panels
BG_INPUT  = "#ffffff"     # input fields
BG_HOVER  = "#f1f3f5"     # hover state — slightly darker grey
ACCENT    = "#343a40"     # primary accent — dark grey for high contrast elements
ACCENT_L  = "#495057"     # lighter grey for hover
ACCENT_D  = "#343a4015"   # dim tint for backgrounds
GREEN     = "#28a745"     # A clear, standard green
GREEN_D   = "#28a74515"   # Tinted green
RED_C     = "#dc3545"     # A clear, standard red
RED_D     = "#dc354515"
YELLOW    = "#ffc107"     # Standard warning yellow/orange
YELLOW_D  = "#ffc10715"
TP        = "#212529"     # text primary — dark grey/black
TM        = "#6c757d"     # text muted — standard grey
BORDER    = "#dee2e6"     # border colour
BORDER_L  = "#ced4da"
TOPBAR_BG = "#ffffff"
ALT_ROW   = "#f8f9fa"     # Use the same as page background for simplicity
NET_BG    = GREEN_D      # Use tinted green for the net amount card
NET_BR    = GREEN        # Use green border for net amount card

def T(key):
    m = {"BG_DARK":BG,"BG_CARD":BG_CARD,"BG_INPUT":BG_INPUT,"BG_HOVER":BG_HOVER,
         "ACCENT":ACCENT,"ACCENT_LIGHT":ACCENT_L,"ACCENT_DIM":ACCENT_D,"ACCENT_GLOW":ACCENT_D,
         "GREEN":GREEN,"GREEN_DIM":GREEN_D,"RED_C":RED_C,"RED_DIM":RED_D,
         "YELLOW":YELLOW,"YELLOW_DIM":YELLOW_D,"TEXT_PRIMARY":TP,"TEXT_MUTED":TM,
         "TEXT_FAINT":BORDER,"BORDER":BORDER,"BORDER_LIGHT":BORDER_L,
         "TOPBAR":TOPBAR_BG,"TOPBAR_BORDER":ACCENT,"TABLE_ALT":ALT_ROW,
         "NETCARD_BG":NET_BG,"NETCARD_BORDER":NET_BR,"SCROLLBAR":BORDER}
    return m.get(key, "#000000")

def build_stylesheet():
    return f"""
QMainWindow, QWidget {{
    background: {BG};
    color: {TP};
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
    font-size: 14px;
}}
QTabWidget::pane {{
    border: none;
    background: {BG};
    top: 0px;
}}
QTabWidget > QWidget {{ background: {BG}; }}
QTabBar {{
    background: {BG_CARD};
    border-bottom: 2px solid {BORDER};
}}
QTabBar::tab {{
    background: transparent;
    color: {TM};
    padding: 14px 36px;
    font-weight: 700;
    font-size: 14px;
    border: none;
    border-bottom: 2px solid transparent;
    min-width: 120px;
    letter-spacing: 1.2px;
    transition: color 0.2s, background 0.2s, border 0.2s;
}}
QTabBar::tab:selected {{
    color: {ACCENT_L};
    border-bottom: 2px solid {ACCENT};
    font-weight: 700;
    background: {ACCENT_D};
}}
QTabBar::tab:hover:!selected {{
    color: {TP};
    background: {BG_HOVER};
}}
QLineEdit, QDoubleSpinBox, QSpinBox {{
    background: {BG_INPUT};
    border: 1.5px solid {BORDER};
    border-radius: 7px;
    padding: 8px 12px;
    color: {TP};
    font-size: 14px;
    selection-background-color: {ACCENT};
    min-height: 18px;
}}
QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {{
    border: 1.5px solid {ACCENT};
    background: {BG_CARD};
}}
QLineEdit:read-only {{
    background: {BG};
    color: {TM};
    border: 1.5px solid {BORDER};
    border-radius: 7px;
}}
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
QSpinBox::up-button, QSpinBox::down-button {{ width: 0px; border: none; }}
QTableWidget {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    gridline-color: {BORDER};
    color: {TP};
    font-size: 14px;
    outline: none;
}}
QTableWidget::item {{ padding: 5px 8px; border: none; }}
QTableWidget::item:selected {{
    background: {ACCENT_D};
    color: {ACCENT};
}}
QTableWidget::item:alternate {{ background: {ALT_ROW}; }}
QHeaderView {{ background: transparent; border: none; }}
QHeaderView::section {{
    background: {BG};
    color: {TM};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 9px 8px;
    border: none;
    border-bottom: 2px solid {ACCENT};
    border-right: 1px solid {BORDER};
    text-transform: uppercase;
}}
QHeaderView::section:last {{ border-right: none; }}
QPushButton {{
    background: {BG_CARD};
    color: {TP};
    border: 1px solid {BORDER_L};
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 14px;
    min-height: 16px;
}}
QPushButton:hover {{
    background: {BG_HOVER};
    color: {ACCENT};
    border-color: {ACCENT};
}}
QPushButton:pressed {{ background: {ACCENT_D}; border-color: {ACCENT}; }}
QPushButton#accent {{
    background: {ACCENT};
    color: white;
    border: none;
    padding: 9px 22px;
    font-size: 14px;
    font-weight: 700;
    border-radius: 8px;
}}
QPushButton#accent:hover {{ background: {ACCENT_L}; color: white; }}
QPushButton#green {{ /* Outline button */
    background: {GREEN_D};
    color: {GREEN};
    border: 1px solid {GREEN};
    padding: 9px 20px;
    font-size: 14px;
    font-weight: 700;
    border-radius: 8px;
}}
QPushButton#green:hover {{ background: {GREEN}; color: white; }}
QPushButton#red {{ /* Outline button */
    background: {RED_D};
    color: {RED_C};
    border: 1px solid {RED_C};
    border-radius: 7px;
    padding: 7px 14px;
    font-weight: 600;
    font-size: 12px;
}}
QPushButton#red:hover {{ background: {RED_C}; color: white; }}
QPushButton#yellow {{ /* Outline button */
    background: {YELLOW_D};
    color: {YELLOW};
    border: 1px solid {YELLOW};
    padding: 9px 20px;
    font-size: 14px;
    font-weight: 700;
    border-radius: 8px;
}}
QPushButton#yellow:hover {{ background: {YELLOW}; color: white; }}
QFrame#card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-bottom: 4px solid {BORDER_L};
    border-right: 2px solid {BORDER_L};
    border-radius: 12px;
}}
QFrame#netcard {{
    background: {NET_BG};
    border: 2px solid {NET_BR};
    border-bottom: 5px solid {NET_BR};
    border-radius: 12px;
}}
QFrame#statcard {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
QFrame#topbar {{
    background: {TOPBAR_BG};
    border-bottom: 2px solid {ACCENT};
}}
QFrame#divider_h {{
    background: {BORDER};
    max-height: 1px; min-height: 1px; border: none;
}}
QFrame#divider_v {{
    background: {BORDER};
    max-width: 1px; min-width: 1px; border: none;
}}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {BG};
    width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_L};
    border-radius: 3px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {ACCENT}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QStatusBar {{
    background: {BG_CARD};
    color: {TM};
    font-size: 11px;
    border-top: 1px solid {BORDER};
    padding: 3px 16px;
}}
QDialog {{ background: {BG}; color: {TP}; }}
QDialogButtonBox QPushButton {{ min-width: 88px; padding: 8px 18px; }}
QAbstractItemView {{
    background: {BG_CARD};
    color: {TP};
    border: 1.5px solid {ACCENT};
    border-radius: 7px;
    selection-background-color: {ACCENT};
    selection-color: {BG_CARD};
    font-size: 14px;
    padding: 4px;
    outline: none;
}}
QMessageBox {{ background: {BG_CARD}; }}
QMessageBox QLabel {{ color: {TP}; background: transparent; }}
QToolTip {{
    background: {BG_CARD};
    color: {TP};
    border: 1px solid {BORDER_L};
    border-radius: 5px;
    padding: 5px 9px;
    font-size: 12px;
}}
"""

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "billing.db")

# ═══════════════════════════════════════
#  DATABASE
# ═══════════════════════════════════════
def init_db():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT, date TEXT, patient_name TEXT, patient_phone TEXT,
        patient_email TEXT, patient_age TEXT, patient_gender TEXT, patient_address TEXT,
        doctor TEXT,
        items TEXT, subtotal REAL, discount_pct REAL, discount_amt REAL,
        round_off REAL, net_amount REAL,
        payment_mode TEXT, paid_amount REAL, deducted_advance REAL,
        total_received REAL, remaining_advance REAL, due_amount REAL,
        created_at TEXT)""")
    # Migrate invoices
    existing = [row[1] for row in c.execute("PRAGMA table_info(invoices)").fetchall()]
    for col, dtype in [("discount_pct","REAL"),("discount_amt","REAL"),("round_off","REAL"),
                        ("patient_phone","TEXT"),("patient_email","TEXT"),
                        ("patient_age","TEXT"),("patient_gender","TEXT"),("patient_address","TEXT"),
                        ("payment_mode","TEXT"),("paid_amount","REAL"),("deducted_advance","REAL"),
                        ("total_received","REAL"),("remaining_advance","REAL"),("due_amount","REAL")]:
        if col not in existing:
            c.execute(f"ALTER TABLE invoices ADD COLUMN {col} {dtype} DEFAULT ''")

    c.execute("""CREATE TABLE IF NOT EXISTS shop_settings (
        id INTEGER PRIMARY KEY, shop_name TEXT, store_tag TEXT, dr_name TEXT,
        address1 TEXT, address2 TEXT, address3 TEXT,
        phone TEXT, gstin TEXT, regd_no TEXT, website TEXT)""")
    shop_cols = [row[1] for row in c.execute("PRAGMA table_info(shop_settings)").fetchall()]
    if 'dr_name' not in shop_cols:
        c.execute("ALTER TABLE shop_settings ADD COLUMN dr_name TEXT DEFAULT ''")
    if 'store_tag' not in shop_cols:
        c.execute("ALTER TABLE shop_settings ADD COLUMN store_tag TEXT DEFAULT ''")
    for col in ['address1','address2','address3','regd_no','website']:
        if col not in shop_cols:
            c.execute(f"ALTER TABLE shop_settings ADD COLUMN {col} TEXT DEFAULT ''")

    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, pack_size TEXT,
        price REAL DEFAULT 0, category TEXT DEFAULT '')""")

    c.execute("SELECT COUNT(*) FROM shop_settings")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO shop_settings
            (id,shop_name,store_tag,dr_name,address1,address2,address3,phone,gstin,regd_no,website)
            VALUES (1,'THE PHYSIOREHAB','Physiotherapy Clinic','Dr. Upendra Agrawal (PT)',
            '65, Udai Nagar-A, Nirman Nagar','Near Mansarovar Metro Station','Jaipur, Rajasthan - 302019',
            '9828600634','','IAP/L-13459','www.thephysiorehab.com')""")
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO products (name,pack_size,price,category) VALUES (?,?,?,?)", [
            ("Physiotherapy Session","1 Visit",700.00,"Physiotherapy"),
            ("Ultrasound Therapy","1 Session",300.00,"Physiotherapy"),
            ("TENS Therapy","1 Session",250.00,"Physiotherapy"),
            ("Hot Wax Bath","1 Session",200.00,"Physiotherapy"),
            ("IFT Therapy","1 Session",280.00,"Physiotherapy"),
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
    c.execute("SELECT id,name,pack_size,price,category FROM products ORDER BY category,name")
    r = c.fetchall(); conn.close(); return r

def get_product_by_name(name):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT id,name,pack_size,price,category FROM products WHERE name=? COLLATE NOCASE LIMIT 1", (name,))
    row = c.fetchone(); conn.close()
    if row: return {"id":row[0],"name":row[1],"pack_size":row[2],
                    "price":row[3],"category":row[4]}
    return None

def add_product(name,pack_size,price,category):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("INSERT INTO products(name,pack_size,price,category)VALUES(?,?,?,?)",
              (name,pack_size,price,category))
    conn.commit(); conn.close()

def update_product(pid,name,pack_size,price,category):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("UPDATE products SET name=?,pack_size=?,price=?,category=? WHERE id=?",
              (name,pack_size,price,category,pid))
    conn.commit(); conn.close()
    conn.commit(); conn.close()

def delete_product(pid):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("DELETE FROM products WHERE id=?",(pid,)); conn.commit(); conn.close()

def save_invoice(d):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""INSERT INTO invoices
        (invoice_no,date,patient_name,patient_phone,patient_email,patient_age,patient_gender,
         patient_address,doctor,items,subtotal,discount_pct,discount_amt,round_off,net_amount,
         payment_mode,paid_amount,deducted_advance,total_received,remaining_advance,due_amount,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (d["invoice_no"],d["date"],d["patient_name"],d.get("patient_phone",""),
         d.get("patient_email",""),d.get("patient_age",""),d.get("patient_gender",""),
         d.get("patient_address",""),d["doctor"],json.dumps(d["items"]),
         d["subtotal"],d["discount_pct"],d["discount_amt"],d["round_off"],d["net_amount"],
         d.get("payment_mode","Cash"),d.get("paid_amount",0),d.get("deducted_advance",0),
         d.get("total_received",0),d.get("remaining_advance",0),d.get("due_amount",0),
         datetime.now().isoformat()))
    conn.commit(); conn.close()

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
.copy{padding:10px 14px 8px 14px}
.copy-label{
  display:inline-flex;align-items:center;gap:5px;
  background:#1a1a2e;color:#fff;font-size:7.5px;font-weight:800;
  letter-spacing:2px;padding:2px 10px 2px 7px;border-radius:3px;
  margin-bottom:6px;text-transform:uppercase}
/* HEADER: left=shop name+address, right=doctor+regd+mob+website */
.hdr{display:flex;align-items:flex-start;border-bottom:2px solid #1a1a2e;padding-bottom:8px;margin-bottom:7px}
.hdr-left{flex:1;padding-right:14px}
.shop-name{font-size:20px;font-weight:900;color:#1a1a2e;letter-spacing:0.5px;line-height:1.2}
.shop-tag{font-size:8px;color:#555;margin-top:2px}
.shop-addr-line{font-size:8.5px;color:#333;margin-top:1px;line-height:1.6}
.hdr-right{text-align:right;min-width:200px}
.dr-name{font-size:13px;font-weight:800;color:#1a1a2e;margin-bottom:3px}
.hdr-right .info-line{font-size:8.5px;color:#333;line-height:1.7}
/* invoice meta row */
.inv-meta{display:flex;justify-content:space-between;align-items:flex-start;
  border:1px solid #d0d4e8;border-radius:4px;padding:5px 10px;margin-bottom:6px;background:#f7f8ff}
.inv-meta .lbl{font-size:7px;color:#888;text-transform:uppercase;letter-spacing:1px;font-weight:700}
.inv-meta .val{font-size:9.5px;font-weight:700;color:#1a1a2e}
/* patient box */
.pat-box{border:1px solid #d0d4e8;border-radius:4px;padding:6px 10px;margin-bottom:6px;background:#f7f8ff}
.pat-box .lbl{font-size:7.5px;color:#888;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:3px}
.pat-row{display:flex;gap:20px;flex-wrap:wrap}
.pat-item{font-size:9px;color:#222}
.pat-item b{color:#1a1a2e}
/* table */
table{width:100%;border-collapse:collapse;margin-bottom:6px}
thead tr{background:#1a1a2e;color:#fff}
th{padding:5px 4px;font-size:7.5px;text-align:center;font-weight:700;text-transform:uppercase;letter-spacing:0.5px}
th.l{text-align:left;padding-left:8px}th.r{text-align:right;padding-right:8px}
td{border-bottom:1px solid #eef0f8;font-size:9px;padding:4px 4px;color:#222}
td.l{text-align:left;padding-left:8px}
td.r{text-align:right;padding-right:8px;font-weight:600}
td.c{text-align:center}
tbody tr:nth-child(even){background:#f5f7ff}
tbody tr:last-child td{border-bottom:1.5px solid #1a1a2e}
/* comments */
.comments{font-size:8px;color:#444;margin-bottom:6px;padding:4px 8px;background:#fffef0;
  border:1px solid #e8e0a0;border-radius:3px}
.comments b{color:#1a1a2e}
/* bottom section */
.bottom{display:flex;gap:10px;align-items:flex-start}
/* payment table */
.pay-table{flex:1;border:1px solid #d0d4e8;border-radius:4px;overflow:hidden}
.pay-table table{margin:0}
.pay-table thead tr{background:#2e2860}
.pay-table th{font-size:7px;padding:4px 4px}
.pay-table td{font-size:8.5px;padding:3px 4px}
/* totals */
.totals{min-width:210px;border:1px solid #d0d4e8;border-radius:4px;overflow:hidden}
.trow{display:flex;justify-content:space-between;padding:3.5px 10px;border-bottom:1px solid #eef0f8;font-size:9px}
.trow.disc{color:#b00000;background:#fff5f5}
.trow.roundoff{color:#555}
.trow.net{background:#1a1a2e;color:#fff;font-size:11.5px;font-weight:900;border:none;padding:5px 10px}
.trow.received{background:#e8f8ee;color:#145214;font-weight:700;font-size:9px}
.trow.advance{background:#fff8e1;color:#7a5500;font-size:9px}
.trow.due{background:#fff0f0;color:#b00;font-weight:700;font-size:9.5px}
/* footer */
.footer{margin-top:7px;display:flex;justify-content:space-between;
  border-top:1px solid #ddd;padding-top:5px;font-size:7.5px;color:#666;line-height:1.7}
.sig{border-top:1px solid #555;display:inline-block;min-width:120px;
  padding-top:3px;margin-top:18px;text-align:center;font-size:7.5px}
.page-cut{border:none;border-top:1.5px dashed #bbb;margin:4px 0;
  text-align:center;font-size:7px;color:#bbb;letter-spacing:3px;padding:2px 0}
</style>"""

def _inv_body(d, shop, label=""):
    rows = ""
    for i, item in enumerate(d.get("items",[]), 1):
        pack  = item.get('pack_size','').strip()
        pname = item.get('product','')
        pcell = f"{pname} <span style='color:#888;font-weight:400'>- {pack}</span>" if pack else pname
        try: qd = int(item['qty']) if float(item['qty'])==int(float(item['qty'])) else item['qty']
        except: qd = item.get('qty','')
        qty   = float(item.get('qty', 0))
        rate  = float(item.get('rate', 0))
        total_amt = qty * rate
        rows += f"""<tr>
          <td class=c>{i}</td><td class=l>{pcell}</td>
          <td class=c>{qd}</td>
          <td class=r>&#8377;{rate:.2f}</td>
          <td class=r>0.00</td>
          <td class=r>&#8377;{total_amt:.2f}</td>
        </tr>"""
    net = d.get('net_amount', 0)
    s = shop

    label_html = ""
    if label:
        icon = "📋" if "Admin" in label else "🧾"
        label_html = f'<div class="copy-label"><span>{icon}</span> {label.upper()}</div>'

    # Build address lines
    addr_parts = [s.get('address1',''), s.get('address2',''), s.get('address3','')]
    addr_html = '<br>'.join(p for p in addr_parts if p.strip())

    # Patient details
    pname = d.get('patient_name','—')
    page = d.get('patient_age','')
    pgend = d.get('patient_gender','')
    pph = d.get('patient_phone','')
    pemail = d.get('patient_email','')
    paddr = d.get('patient_address','')
    pat_items = [f"<span class='pat-item'><b>Name:</b> {pname}</span>"]
    if page: pat_items.append(f"<span class='pat-item'><b>Age:</b> {page} yrs</span>")
    if pgend: pat_items.append(f"<span class='pat-item'><b>Gender:</b> {pgend}</span>")
    if pph: pat_items.append(f"<span class='pat-item'><b>Mobile:</b> {pph}</span>")
    if pemail: pat_items.append(f"<span class='pat-item'><b>Email:</b> {pemail}</span>")
    if paddr: pat_items.append(f"<span class='pat-item'><b>Address:</b> {paddr}</span>")

    # Payment section
    pm      = d.get('payment_mode','Cash')
    paid    = float(d.get('paid_amount', net))
    ded_adv = float(d.get('deducted_advance', 0))
    tot_rec = float(d.get('total_received', paid))
    rem_adv = float(d.get('remaining_advance', 0))
    due     = float(d.get('due_amount', 0))

    # Discount row — only show if discount > 0
    dp = d.get('discount_pct', 0)
    da = d.get('discount_amt', 0)
    disc_row = ""
    if dp and dp > 0:
        disc_row = f'<div class="trow disc"><span>Discount ({dp:.1f}%)</span><span>&#8722;&#8377;{da:.2f}</span></div>'

    return f"""
<div class="copy">
  {label_html}
  <div class="hdr">
    <div class="hdr-left">
      <div class="shop-name">{s.get('shop_name','')}</div>
      <div class="shop-tag">{s.get('store_tag','')}</div>
      <div class="shop-addr-line">{addr_html}</div>
    </div>
    <div class="hdr-right">
      <div class="dr-name">{s.get('dr_name','')}</div>
      <div class="info-line">Regd.No.: {s.get('regd_no','')}</div>
      <div class="info-line">Mob.: {s.get('phone','')}</div>
      <div class="info-line">{s.get('website','')}</div>
    </div>
  </div>

  <div class="inv-meta">
    <div>
      <div class="lbl">Invoice Number</div>
      <div class="val">{d.get('invoice_no','—')}</div>
    </div>
    <div>
      <div class="lbl">Date</div>
      <div class="val">{d.get('date','—')}</div>
    </div>
    <div>
      <div class="lbl">Submitted For</div>
      <div class="val">{s.get('shop_name','')}</div>
    </div>
  </div>

  <div class="pat-box">
    <div class="lbl">Patient Details</div>
    <div class="pat-row">{''.join(pat_items)}</div>
  </div>

  <table>
    <thead><tr>
      <th style="width:22px">#</th>
      <th class=l>Description</th>
      <th style="width:36px">Unit</th>
      <th style="width:70px" class=r>Cost (&#8377;)</th>
      <th style="width:70px" class=r>Discount (&#8377;)</th>
      <th style="width:80px" class=r>Total (&#8377;)</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>

  <div class="bottom">
    <div class="pay-table">
      <table>
        <thead><tr>
          <th>Receipt No</th><th>Date</th><th>Payment Mode</th>
          <th>Deducted from Advance</th><th>Amount Received (&#8377;)</th><th>Due Amount (&#8377;)</th>
        </tr></thead>
        <tbody>
          <tr>
            <td class=c>—</td>
            <td class=c>{d.get('date','—')}</td>
            <td class=c>{pm}</td>
            <td class=c>{ded_adv:.2f}</td>
            <td class=c>{tot_rec:.2f}</td>
            <td class=c>{due:.2f}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="totals">
      <div class="trow"><span>Subtotal</span><span>&#8377;{d.get('subtotal',0):.2f}</span></div>
      {disc_row}
      <div class="trow roundoff"><span>Round Off</span><span>&#8377;{d.get('round_off',0):.2f}</span></div>
      <div class="trow net"><span>NET AMOUNT</span><span>&#8377;{net:.2f}</span></div>
      <div class="trow received"><span>Total Amount Received</span><span>&#8377;{tot_rec:.2f}</span></div>
      <div class="trow advance"><span>Remaining Advance Amount</span><span>&#8377;{rem_adv:.2f}</span></div>
      <div class="trow due"><span>Due Amount</span><span>&#8377;{due:.2f}</span></div>
    </div>
  </div>

  <div class="footer">
    <div>
      <b>Raised By: {s.get('shop_name','')}</b>
    </div>
    <div style="text-align:right">
      <div class="sig">Authorised by<br><b>{s.get('dr_name','')}</b></div>
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
    .shop-addr-line{{font-size:7px;margin-top:1px}}
    .hdr{{padding-bottom:5px;margin-bottom:5px}}
    .dr-name{{font-size:11px}}
    .hdr-right .info-line{{font-size:7.5px}}
    .inv-meta{{padding:3px 7px;margin-bottom:4px}}
    .inv-meta .val{{font-size:8.5px}}
    .pat-box{{padding:4px 7px;margin-bottom:4px}}
    .pat-item{{font-size:8px}}
    th{{font-size:7px;padding:4px 2px}}
    td{{font-size:8px;padding:2.5px 2px}}
    .trow{{font-size:8px;padding:2.5px 8px}}
    .trow.net{{font-size:10px;padding:4px 8px}}
    .footer{{font-size:6.5px;margin-top:4px;padding-top:3px}}
    .sig{{margin-top:10px;min-width:100px;font-size:7px}}
    .copy-label{{font-size:7px;padding:1.5px 8px 1.5px 6px}}
    .pay-table td{{font-size:7.5px;padding:2px 3px}}
    .pay-table th{{font-size:6.5px;padding:3px 2px}}
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
    l.setStyleSheet(f"color:{TM};font-size:12px;font-weight:700;"
                    f"letter-spacing:1.2px;background:transparent;margin-bottom:1px")
    return l

def pill(txt, color=None, bg=None):
    if color is None: color = ACCENT
    if bg is None: bg = color + "22"
    l = QLabel(txt)
    l.setStyleSheet(f"color:{color};background:{bg};border:1px solid {color}44;"
                    f"border-radius:9px;padding:2px 10px;font-size:11px;font-weight:700")
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
        self.setStyleSheet(f"background:{BG};")
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0); l.setSpacing(0)

        bar = QFrame(); bar.setObjectName("topbar"); bar.setFixedHeight(50)
        bl = QHBoxLayout(bar); bl.setContentsMargins(18,0,18,0); bl.setSpacing(10)
        icon = QLabel("◈"); icon.setStyleSheet(f"color:{ACCENT};font-size:18px;background:transparent")
        ttl  = QLabel("Invoice Preview")
        ttl.setStyleSheet(f"color:{TP};font-weight:700;font-size:14px;background:transparent")
        hint = QLabel("Single copy preview  ·  PDF export has both copies")
        hint.setStyleSheet(f"color:{TM};font-size:11px;background:transparent")
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
        root.setContentsMargins(16, 10, 16, 10)
        root.setSpacing(8)

        # ── Title row + action buttons (all in ONE row) ─────────
        title_row = QHBoxLayout(); title_row.setSpacing(8)
        icon = QLabel("◈")
        icon.setStyleSheet(f"color:{ACCENT};font-size:16px;background:transparent;font-weight:900")
        title = QLabel("New Invoice")
        title.setStyleSheet(f"color:{TP};font-size:16px;font-weight:800;background:transparent")
        self.inv_badge = QLabel("R-000001")
        self.inv_badge.setStyleSheet(
            f"color:{ACCENT};font-size:11px;font-weight:800;"
            f"background:{ACCENT_D};border:1px solid {ACCENT}55;"
            f"border-radius:6px;padding:2px 10px")
        title_row.addWidget(icon); title_row.addSpacing(4)
        title_row.addWidget(title); title_row.addSpacing(8)
        title_row.addWidget(self.inv_badge); title_row.addStretch()

        btn_new     = QPushButton("＋ New")
        btn_preview = QPushButton("◉ Preview");   btn_preview.setObjectName("accent")
        btn_save    = QPushButton("✔ Save");       btn_save.setObjectName("green")
        btn_pdf     = QPushButton("⬇ PDF");        btn_pdf.setObjectName("yellow")
        btn_print   = QPushButton("⎙ Print")
        for b in [btn_new,btn_preview,btn_save,btn_pdf,btn_print]:
            b.setFixedHeight(30)
        btn_new.setToolTip("Clear and start a new invoice")
        btn_pdf.setToolTip("Export Admin & Customer copies as one PDF")
        btn_new.clicked.connect(self._reset)
        btn_preview.clicked.connect(self._preview)
        btn_save.clicked.connect(self._save)
        btn_pdf.clicked.connect(self._export_pdf)
        btn_print.clicked.connect(self._print)
        for b in [btn_new, btn_preview, btn_save, btn_pdf, btn_print]:
            title_row.addWidget(b)
        root.addLayout(title_row)

        # ── Patient info — single compact horizontal card ──────
        pcard = QFrame(); pcard.setObjectName("card")
        pg = QHBoxLayout(pcard); pg.setContentsMargins(14,9,14,9); pg.setSpacing(14)

        def _lfield(label, placeholder, fixed_w=None):
            w = QWidget(); w.setStyleSheet("background:transparent")
            vl = QVBoxLayout(w); vl.setContentsMargins(0,0,0,0); vl.setSpacing(2)
            lbl = QLabel(label.upper())
            lbl.setStyleSheet(f"color:{TM};font-size:12px;font-weight:700;letter-spacing:1px;background:transparent")
            inp = QLineEdit(); inp.setPlaceholderText(placeholder)
            if fixed_w: inp.setFixedWidth(fixed_w)
            vl.addWidget(lbl); vl.addWidget(inp)
            return w, inp

        w1, self.patient_edit  = _lfield("Patient Name", "Patient / Customer name")
        w2, self.age_edit      = _lfield("Age",          "Age (yrs)",       75)
        w3, self.gender_edit   = _lfield("Gender",       "M / F / Other",   100)
        w4, self.phone_edit    = _lfield("Mobile",       "Phone number",   140)
        w5, self.email_edit    = _lfield("Email",        "Email (opt.)",   190)
        w6, self.date_edit     = _lfield("Date",         "DD-MM-YYYY",      110)
        self.invoice_no = ""

        pg.addWidget(w1, 3); pg.addWidget(w2); pg.addWidget(w3)
        pg.addWidget(w4); pg.addWidget(w5); pg.addWidget(w6)

        # Address row
        pcard2 = QFrame(); pcard2.setObjectName("card")
        pg2 = QHBoxLayout(pcard2); pg2.setContentsMargins(14,6,14,6); pg2.setSpacing(14)
        wa, self.addr_edit = _lfield("Patient Address", "Full address of patient")
        pg2.addWidget(wa)
        root.addWidget(pcard)
        root.addWidget(pcard2)

        # ── Items mini-header ──────────────────────────────────
        items_hdr = QHBoxLayout(); items_hdr.setSpacing(8)
        items_lbl = QLabel("BILL ITEMS")
        items_lbl.setStyleSheet(
            f"color:{TM};font-size:12px;font-weight:700;letter-spacing:1.5px;background:transparent")
        items_hdr.addWidget(items_lbl); items_hdr.addStretch()
        btn_add_row = QPushButton("＋  Add Item")
        btn_del_row = QPushButton("✕  Remove"); btn_del_row.setObjectName("red")
        btn_add_row.setFixedHeight(28); btn_del_row.setFixedHeight(28)
        btn_add_row.clicked.connect(lambda: self._add_row())
        btn_del_row.clicked.connect(self._del_row)
        items_hdr.addWidget(btn_add_row); items_hdr.addWidget(btn_del_row)
        root.addLayout(items_hdr)

        # ── Items table — STRETCH to fill all remaining space ──
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#","Description","Pack / Unit","Qty","Rate (₹)"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for col in [0,2,3,4]: hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0,30); self.table.setColumnWidth(2,90)
        self.table.setColumnWidth(3,50); self.table.setColumnWidth(4,90)
        self.table.setAlternatingRowColors(True)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.itemChanged.connect(lambda _: self._recalc())
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table, 1)   # ← stretch factor keeps table large

        # ── Totals strip + Net amount ──────────────────────────
        bot = QHBoxLayout(); bot.setSpacing(10)

        tcard = QFrame(); tcard.setObjectName("card")
        tg = QHBoxLayout(tcard); tg.setContentsMargins(14,8,14,8); tg.setSpacing(12)

        def _tfield(label, fixed_w=90):
            w = QWidget(); w.setStyleSheet("background:transparent")
            vl = QVBoxLayout(w); vl.setContentsMargins(0,0,0,0); vl.setSpacing(2)
            lbl = QLabel(label.upper())
            lbl.setStyleSheet(f"color:{TM};font-size:12px;font-weight:700;letter-spacing:1px;background:transparent")
            f = QLineEdit(); f.setReadOnly(True); f.setFixedWidth(fixed_w)
            vl.addWidget(lbl); vl.addWidget(f)
            return w, f

        def _efield(label, placeholder="", fixed_w=90):
            w = QWidget(); w.setStyleSheet("background:transparent")
            vl = QVBoxLayout(w); vl.setContentsMargins(0,0,0,0); vl.setSpacing(2)
            lbl = QLabel(label.upper())
            lbl.setStyleSheet(f"color:{TM};font-size:12px;font-weight:700;letter-spacing:1px;background:transparent")
            f = QLineEdit(); f.setPlaceholderText(placeholder); f.setFixedWidth(fixed_w)
            vl.addWidget(lbl); vl.addWidget(f)
            return w, f

        w_sub, self.subtotal_f = _tfield("Subtotal")

        wd = QWidget(); wd.setStyleSheet("background:transparent")
        vld = QVBoxLayout(wd); vld.setContentsMargins(0,0,0,0); vld.setSpacing(2)
        lbl_d = QLabel("DISCOUNT %")
        lbl_d.setStyleSheet(f"color:{TM};font-size:12px;font-weight:700;letter-spacing:1px;background:transparent")
        self.disc_edit = QLineEdit("0"); self.disc_edit.setFixedWidth(55)
        self.disc_edit.textChanged.connect(self._recalc)
        vld.addWidget(lbl_d); vld.addWidget(self.disc_edit)

        w_da, self.disc_amt_f = _tfield("Disc. Amt", 75)

        # Payment mode
        wpm = QWidget(); wpm.setStyleSheet("background:transparent")
        vlpm = QVBoxLayout(wpm); vlpm.setContentsMargins(0,0,0,0); vlpm.setSpacing(2)
        lbl_pm = QLabel("PAYMENT MODE")
        lbl_pm.setStyleSheet(f"color:{TM};font-size:12px;font-weight:700;letter-spacing:1px;background:transparent")
        from PyQt6.QtWidgets import QComboBox
        self.pay_mode = QComboBox(); self.pay_mode.addItems(["Cash","UPI","Cash + UPI","Other"])
        self.pay_mode.setFixedWidth(100)
        vlpm.addWidget(lbl_pm); vlpm.addWidget(self.pay_mode)

        w_paid, self.paid_edit     = _efield("Paid Amt",      "0.00", 80)
        self.paid_edit.textChanged.connect(self._recalc_payment)
        w_adv,  self.deduct_edit   = _efield("Deduct Advance","0.00", 90)
        self.deduct_edit.textChanged.connect(self._recalc_payment)

        for w in [w_sub, wd, w_da, wpm, w_paid, w_adv]:
            tg.addWidget(w)
        bot.addWidget(tcard, 3)

        netcard = QFrame(); netcard.setObjectName("netcard")
        nl = QVBoxLayout(netcard); nl.setContentsMargins(12,6,12,6); nl.setSpacing(0)
        net_lbl = QLabel("NET AMOUNT")
        net_lbl.setStyleSheet(f"font-size:11px;font-weight:700;color:{GREEN};"
                               f"letter-spacing:2px;background:transparent")
        net_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.net_display = QLabel("₹ 0.00")
        self.net_display.setStyleSheet(
            f"font-size:20px;font-weight:900;color:{GREEN};background:transparent")
        self.net_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        due_lbl = QLabel("DUE")
        due_lbl.setStyleSheet(f"font-size:10px;font-weight:700;color:{RED_C};"
                               f"letter-spacing:2px;background:transparent;margin-top:2px")
        due_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.due_display = QLabel("₹ 0.00")
        self.due_display.setStyleSheet(
            f"font-size:14px;font-weight:700;color:{RED_C};background:transparent")
        self.due_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        nl.addWidget(net_lbl); nl.addWidget(self.net_display)
        nl.addWidget(due_lbl); nl.addWidget(self.due_display)
        bot.addWidget(netcard, 1)
        root.addLayout(bot)

    # ── Helpers ──────────────────────────────────────────────
    def _add_row(self, data=None):
        self.table.blockSignals(True)
        r = self.table.rowCount(); self.table.insertRow(r)

        sr = QTableWidgetItem(str(r+1))
        sr.setFlags(Qt.ItemFlag.ItemIsEnabled)
        sr.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        sr.setForeground(QColor(TM))
        self.table.setItem(r, 0, sr)

        prod_edit = QLineEdit()
        prod_edit.setStyleSheet(
            f"background:{BG_INPUT};border:none;color:{TP};"
            f"font-size:14px;padding:5px 10px;border-radius:0")
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
                self._sc(row,3,"1")
                self._sc(row,4,str(p.get("price",0)))
                self.table.blockSignals(False)
                self._recalc()

        prod_edit.textChanged.connect(lambda t: fill(t) if get_product_by_name(t) else None)
        comp.activated.connect(fill)
        self.table.setCellWidget(r, 1, prod_edit)

        for c, v in enumerate(["","1","0"], 2):
            it = QTableWidgetItem(v); it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, c, it)

        if data:
            prod_edit.setText(data.get("product",""))
            self._sc(r,2,data.get("pack_size",""))
            self._sc(r,3,str(data.get("qty",1)))
            self._sc(r,4,str(data.get("rate",0)))

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
        items=[]; sub=0
        for r in range(self.table.rowCount()):
            w = self.table.cellWidget(r,1); pname = w.text() if w else ""
            def cell(c, row=r):
                it = self.table.item(row,c); return it.text() if it else ""
            try: qty=float(cell(3))
            except: qty=0
            try: rate=float(cell(4))
            except: rate=0
            base=qty*rate
            sub+=base
            items.append({"product":pname,"pack_size":cell(2),
                          "qty":qty,"rate":rate,"amount":base})
        try: dp=max(0.0,min(100.0,float(self.disc_edit.text())))
        except: dp=0.0
        da=sub*dp/100; after=sub-da
        net_raw=after; netr=round(net_raw); ro=netr-net_raw

        try: paid=max(0.0, float(self.paid_edit.text()))
        except: paid=float(netr)
        try: ded_adv=max(0.0, float(self.deduct_edit.text()))
        except: ded_adv=0.0
        tot_rec = paid + ded_adv
        rem_adv = 0.0
        due = max(0.0, float(netr) - tot_rec)

        self.table.blockSignals(False)
        return {
            "invoice_no":      self.invoice_no,
            "date":            self.date_edit.text(),
            "patient_name":    self.patient_edit.text(),
            "patient_age":     self.age_edit.text(),
            "patient_gender":  self.gender_edit.text(),
            "patient_phone":   self.phone_edit.text(),
            "patient_email":   self.email_edit.text(),
            "patient_address": self.addr_edit.text(),
            "doctor":          self.shop.get("dr_name",""),
            "items": items,
            "subtotal":        round(sub,2), "discount_pct":dp,
            "discount_amt":    round(da,2),  "round_off":round(ro,2),
            "net_amount":      float(netr),
            "payment_mode":    self.pay_mode.currentText(),
            "paid_amount":     round(paid,2),
            "deducted_advance":round(ded_adv,2),
            "total_received":  round(tot_rec,2),
            "remaining_advance":round(rem_adv,2),
            "due_amount":      round(due,2),
        }

    def _recalc(self):
        d = self._collect(); self._current_data = d
        self.subtotal_f.setText(f"{d['subtotal']:.2f}")
        self.disc_amt_f.setText(f"{d['discount_amt']:.2f}")
        self.net_display.setText(f"₹ {d['net_amount']:.2f}")
        self.due_display.setText(f"₹ {d['due_amount']:.2f}")

    def _recalc_payment(self):
        self._recalc()

    def _reset(self):
        self.table.blockSignals(True); self.table.setRowCount(0); self.table.blockSignals(False)
        self.patient_edit.clear(); self.age_edit.clear(); self.gender_edit.clear()
        self.phone_edit.clear(); self.email_edit.clear(); self.addr_edit.clear()
        self.invoice_no = next_invoice_no()
        self.inv_badge.setText(self.invoice_no)
        self.date_edit.setText(datetime.now().strftime("%d-%m-%Y"))
        self.disc_edit.setText("0")
        self.paid_edit.clear(); self.deduct_edit.clear()
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
        self.age_edit.setText(d.get("patient_age",""))
        self.gender_edit.setText(d.get("patient_gender",""))
        self.phone_edit.setText(d.get("patient_phone",""))
        self.email_edit.setText(d.get("patient_email",""))
        self.addr_edit.setText(d.get("patient_address",""))
        self.invoice_no = d.get("invoice_no","")
        self.inv_badge.setText(self.invoice_no)
        self.date_edit.setText(d.get("date",""))
        self.disc_edit.setText(str(d.get("discount_pct",0)))
        self.paid_edit.setText(str(d.get("paid_amount","")))
        self.deduct_edit.setText(str(d.get("deducted_advance","")))
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
        icon = QLabel("◈"); icon.setStyleSheet(f"color:{ACCENT};font-size:16px;background:transparent")
        title = QLabel("Edit Product" if product else "Add New Product")
        title.setStyleSheet(f"color:{TP};font-size:15px;font-weight:800;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(7); hdr.addWidget(title)
        l.addLayout(hdr)

        card = QFrame(); card.setObjectName("card")
        g = QGridLayout(card); g.setContentsMargins(16,16,16,16); g.setSpacing(10)
        self.name_e  = QLineEdit(); self.name_e.setPlaceholderText("e.g. Physiotherapy Session")
        self.pack_e  = QLineEdit(); self.pack_e.setPlaceholderText("e.g. 1 Visit, 1 Session")
        self.price_e = QDoubleSpinBox(); self.price_e.setRange(0,999999); self.price_e.setDecimals(2); self.price_e.setPrefix("₹ ")
        self.cat_e   = QLineEdit(); self.cat_e.setPlaceholderText("e.g. Physiotherapy, Consultation")
        if product:
            self.name_e.setText(product.get("name","")); self.pack_e.setText(product.get("pack_size",""))
            self.price_e.setValue(product.get("price",0))
            self.cat_e.setText(product.get("category",""))
        for i,(lb,w) in enumerate([("SERVICE / PRODUCT NAME *",self.name_e),("UNIT / PACK SIZE",self.pack_e),
                                    ("PRICE / RATE",self.price_e),("CATEGORY",self.cat_e)]):
            g.addWidget(mk_section(lb),i,0); g.addWidget(w,i,1)
        l.addWidget(card)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        btns.button(QDialogButtonBox.StandardButton.Save).setObjectName("accent")
        btns.accepted.connect(self._ok); btns.rejected.connect(self.reject)
        l.addWidget(btns)

    def _ok(self):
        if not self.name_e.text().strip():
            QMessageBox.warning(self,"Required","Product/Service name is required."); return
        self.accept()

    def get_data(self):
        return {"name":self.name_e.text().strip(),"pack_size":self.pack_e.text().strip(),
                "price":self.price_e.value(),"category":self.cat_e.text().strip()}

class CatalogueTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(20,18,20,18); l.setSpacing(12)
        hdr = QHBoxLayout()
        icon = QLabel("✦"); icon.setStyleSheet(f"color:{ACCENT};font-size:17px;background:transparent")
        title = QLabel("Product Catalogue")
        title.setStyleSheet(f"color:{TP};font-size:17px;font-weight:700;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(8); hdr.addWidget(title); hdr.addStretch()
        l.addLayout(hdr)
        sub = QLabel("Manage medicines & products — they auto-fill in the billing form when you type.")
        sub.setStyleSheet(f"color:{TM};font-size:12px;background:transparent")
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
        self.table = QTableWidget(); self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Service / Product Name","Unit / Pack","Price (₹)","Category"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0,40); self.table.setColumnWidth(2,100)
        self.table.setColumnWidth(3,90)
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
                if c==3: txt=f"{float(v):.2f}"
                else: txt=str(v)
                it=QTableWidgetItem(txt)
                align=Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter if c==1 else Qt.AlignmentFlag.AlignCenter
                it.setTextAlignment(align)
                if c==3: it.setForeground(QColor(GREEN))
                self.table.setItem(r,c,it)
            self.table.setRowHeight(r,36)

    def _filter(self,txt):
        txt=txt.lower()
        self._show([p for p in self._all if txt in p[1].lower() or txt in(p[4]or'').lower()])

    def _add(self):
        dlg=ProductDialog(self)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            d=dlg.get_data(); add_product(d["name"],d["pack_size"],d["price"],d["category"]); self.load()

    def _edit(self):
        row=self.table.currentRow()
        if row<0: QMessageBox.information(self,"Select","Please select a product to edit."); return
        pid=int(self.table.item(row,0).text())
        prod=next((p for p in self._all if p[0]==pid),None)
        if not prod: return
        p={"id":prod[0],"name":prod[1],"pack_size":prod[2],"price":prod[3],"category":prod[4]}
        dlg=ProductDialog(self,p)
        if dlg.exec()==QDialog.DialogCode.Accepted:
            d=dlg.get_data(); update_product(pid,d["name"],d["pack_size"],d["price"],d["category"]); self.load()

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
        icon=QLabel("⊞"); icon.setStyleSheet(f"color:{ACCENT};font-size:17px;background:transparent")
        title=QLabel("Invoice History"); title.setStyleSheet(f"color:{TP};font-size:17px;font-weight:700;background:transparent")
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
        icon=QLabel("⚙"); icon.setStyleSheet(f"color:{ACCENT};font-size:17px;background:transparent")
        title=QLabel("Shop Settings"); title.setStyleSheet(f"color:{TP};font-size:17px;font-weight:700;background:transparent")
        hdr.addWidget(icon); hdr.addSpacing(8); hdr.addWidget(title); hdr.addStretch()
        l.addLayout(hdr)
        note=QLabel("These details appear on every invoice. Doctor name auto-fills as 'Ref. Doctor' on each bill.")
        note.setStyleSheet(f"color:{TM};font-size:12px;background:transparent"); l.addWidget(note)
        card=QFrame(); card.setObjectName("card"); card.setMaximumWidth(600)
        g=QGridLayout(card); g.setContentsMargins(20,18,20,18); g.setSpacing(12)
        self.fields={}; s=get_shop()
        for i,(k,lb) in enumerate([("shop_name","SHOP NAME"),("store_tag","STORE TAG / SPECIALITY"),
                                    ("dr_name","DOCTOR / PROPRIETOR NAME"),
                                    ("regd_no","REGD. NO. (e.g. IAP/L-13459)"),
                                    ("address1","ADDRESS LINE 1"),
                                    ("address2","ADDRESS LINE 2"),
                                    ("address3","ADDRESS LINE 3 (City, State, PIN)"),
                                    ("phone","MOBILE / PHONE"),
                                    ("website","WEBSITE (e.g. www.example.com)")]):
            g.addWidget(mk_section(lb),i,0); f=QLineEdit(s.get(k,"")); self.fields[k]=f; g.addWidget(f,i,1)
        l.addWidget(card)
        btn=QPushButton("✔  Save Settings"); btn.setObjectName("accent")
        btn.setFixedWidth(180); btn.setFixedHeight(36); btn.clicked.connect(self._save); l.addWidget(btn)

    def _save(self):
        conn=sqlite3.connect(DB_PATH); c=conn.cursor()
        c.execute("UPDATE shop_settings SET shop_name=?,store_tag=?,dr_name=?,regd_no=?,address1=?,address2=?,address3=?,phone=?,website=? WHERE id=1",
            tuple(self.fields[k].text() for k in ["shop_name","store_tag","dr_name","regd_no","address1","address2","address3","phone","website"]))
        conn.commit(); conn.close()
        QMessageBox.information(self,"✔  Saved","Settings saved successfully!")

# ═══════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing App — Vijay Homoeo Stores")
        self._build()

    def _build(self):
        central = QWidget()
        cl = QVBoxLayout(central); cl.setContentsMargins(0,0,0,0); cl.setSpacing(0)

        # ── Top bar ─────────────────────────────────────
        topbar = QFrame(); topbar.setObjectName("topbar"); topbar.setFixedHeight(50)
        tbl = QHBoxLayout(topbar); tbl.setContentsMargins(20,0,20,0); tbl.setSpacing(10)

        dot = QLabel("◈")
        dot.setStyleSheet(f"color:{ACCENT};font-size:20px;font-weight:900;background:transparent")
        app_title = QLabel("Billing App")
        app_title.setStyleSheet(f"color:{TP};font-size:16px;font-weight:800;background:transparent")

        divv = QFrame(); divv.setObjectName("divider_v"); divv.setFixedSize(1,22)
        shop_lbl = QLabel(get_shop().get("shop_name",""))
        shop_lbl.setStyleSheet(f"color:{TM};font-size:11px;background:transparent")

        tbl.addWidget(dot); tbl.addSpacing(3); tbl.addWidget(app_title)
        tbl.addSpacing(8); tbl.addWidget(divv); tbl.addSpacing(8); tbl.addWidget(shop_lbl)
        tbl.addStretch()

        v_lbl = QLabel("v3.0")
        v_lbl.setStyleSheet(
            f"color:{ACCENT};background:{ACCENT_D};border:1px solid {ACCENT}44;"
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


def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(build_stylesheet())
    win = MainWindow()
    win.showMaximized()   # open full screen on launch
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
