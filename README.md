# 🧾 Billing App — Vijay Homoeo Stores
## Full Desktop Billing Application (Python + PyQt6)

---

## 📦 What's Included

| File | Purpose |
|------|---------|
| `billing_app.py` | Main application |
| `requirements.txt` | Python packages needed |
| `LAUNCH.bat` | One-click run (Windows) |
| `BUILD_EXE.bat` | Convert to standalone .exe |

---

## 🚀 How to Run

### Option 1 — Easiest (Just Double-Click)
1. Make sure Python is installed → https://python.org/downloads  
   ✅ During install, check **"Add Python to PATH"**
2. Double-click **`LAUNCH.bat`**  
   It auto-installs all packages and launches the app.

### Option 2 — Manual (Command Prompt)
```bash
pip install PyQt6 PyQt6-WebEngine
python billing_app.py
```

### Option 3 — Build a Standalone .EXE
Double-click **`BUILD_EXE.bat`**  
→ Your `.exe` will appear in the `dist/` folder  
→ Copy that `.exe` anywhere and run without needing Python installed

---

## 🖥️ Features

### 📝 New Invoice Tab
- Fill in Patient Name, Doctor, Invoice No., Date
- Add unlimited product rows (Description, HSN, Mfg, Pack, Batch, Qty, Rate, CGST%, SGST%)
- **Live preview** of the invoice updates as you type
- Auto-calculates: Subtotal → Discount → CGST/SGST → Net Amount → Round Off
- Amount in words auto-generated (e.g. "One Thousand Five Hundred Seventy Nine only")

### 📄 Export & Print
- **Export PDF** → Saves print-ready A4 PDF anywhere you choose
- **Print** → Opens print dialog for direct printing
- PDF auto-opens after export

### 📋 History Tab
- All saved invoices stored in local database (`billing.db`)
- Search by patient name or invoice number
- Double-click any invoice to reopen and reprint/re-export

### ⚙️ Settings Tab
- Edit Shop Name, Address, Phone, GSTIN, DL No., Food Lic. No.
- All details auto-appear in every invoice header

---

## 🗂️ Database
- SQLite database (`billing.db`) created automatically in same folder
- Stores all invoices permanently
- No internet connection required — fully offline

---

## 💡 Tips
- After saving an invoice, app auto-resets for the next bill
- Invoice numbers auto-increment (R-000001, R-000002...)
- You can reopen old invoices from History and re-export as PDF
- The database file can be backed up by simply copying `billing.db`

---

## ⚠️ Requirements
- Windows 10 / 11
- Python 3.10 or higher (only needed for Option 1 & 2)
- ~200MB disk space (for PyQt6 packages)
