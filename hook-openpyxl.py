# PyInstaller hook for openpyxl
# Place this file in the same folder as THE_PHYSIOREHAB.spec
# It forces PyInstaller to collect ALL openpyxl submodules and data

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('openpyxl')
hiddenimports += ['et_xmlfile', 'xml.etree.ElementTree', 'xml.etree.cElementTree']
