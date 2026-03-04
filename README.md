# THE PHYSIOREHAB — Billing App Setup Guide

## ▶ How to Customise for Any Clinic

Open `billing_final.py` in any text editor (Notepad is fine).
Find the **CLINIC CONFIGURATION** block near the top (around line 20).
Change only these values:

```python
CLINIC_NAME      = "THE PHYSIOREHAB"          # Big name on invoice
CLINIC_TAG       = "Physiotherapy Clinic"      # Smaller subtitle
CLINIC_ADDR1     = "65, Udai Nagar-A, Nirman Nagar"
CLINIC_ADDR2     = "Near Mansarovar Metro Station"
CLINIC_ADDR3     = "Jaipur, Rajasthan - 302019"
CLINIC_PHONE     = "9828600634"
CLINIC_WEBSITE   = "www.thephysiorehab.com"
CLINIC_DR_NAME   = "Dr. Upendra Agrawal (PT)"
CLINIC_REGD_NO   = "IAP/L-13459"              # Not shown on invoice, kept for records
CLINIC_LOGO_PATH = "logo.png"                  # Logo file name (place next to exe)
APP_TITLE        = "THE PHYSIOREHAB — Billing" # Window title bar
```

**No Settings tab** — the invoice layout is locked to these values.
Nobody using the app can accidentally change the clinic name or logo.


## ▶ Logo Setup

1. Rename your clinic logo file to `logo.png` (or `logo.jpg`)
2. Update `CLINIC_LOGO_PATH = "logo.png"` to match the filename
3. When running as EXE: place `logo.png` in the **same folder as the .exe**
4. When running as .py: place `logo.png` in the **same folder as billing_final.py**

Supported formats: PNG, JPG, JPEG


## ▶ Database (billing.db)

- Created automatically on first run
- Stored next to the `.exe` file (or next to the `.py` file)
- Contains all patients, invoices, and product catalogue
- **Back up this file regularly!** — it is your entire data store
- To move to a different location, change `DB_LOCATION` in the config block


## ▶ Building the EXE (Windows)

### Requirements
```
pip install PyQt6 PyQt6-WebEngine pyinstaller openpyxl
```

### Build
1. Double-click `build_exe.bat`   
   OR run in terminal:
   ```
   pyinstaller --onefile --windowed --name "PhysioRehab_Billing" billing_final.py
   ```
2. EXE appears in the `dist\` folder
3. Copy `logo.png` into the same `dist\` folder as the EXE
4. Run `PhysioRehab_Billing.exe` — `billing.db` is created automatically

### Folder structure after build
```
dist\
  PhysioRehab_Billing.exe    ← the app
  logo.png                   ← your clinic logo (copy here!)
  billing.db                 ← auto-created on first run (your data)
```


## ▶ Running directly as Python (no build)

```
python billing_final.py
```

Place `logo.png` in the same folder as `billing_final.py`.


## ▶ Invoice Details

- Invoice numbers: `IN-001`, `IN-002`, ...
- Receipt numbers: auto-generated from invoice number (`RCT-001`)
- PDF page: A5 Landscape
- Settings tab: **removed** (clinic details are locked in config)
