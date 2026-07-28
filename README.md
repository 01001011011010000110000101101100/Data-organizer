# Pt.info (Patient Information Manager)
**Cross-Platform application** directed toward nurses to management patient data quickly and share the data with the rest of the medical staff.
---
## Features :

* **Cross-Platform :** the program based on Flet and automatically detect Android environment and saves the database records on `/storage/emulated/0/Documents/nurse_data.csv`.
* **Smart Abbreviation Formatting :** automatically detected and converts the stander medical abbreviations (e.g., `ICU`, `MV`, `NPO`) to uppercase for standardized documentation, while properly formatting regular text.
* **Asynchronous I/O:** uses `aiofiles` and non-blocking I/O operating for smooth UI transitions and file handling.
* **Data Sorting:** automatically sorts patient entries numerically and alphabetically by bed number for rapid navigation.

---
## Structure :
```text
Pt_info 
├── constants.py       # Defines medical abbreviation dictionary & dynamic CSV/Log path resolution
├── main.py            # Core GUI flow, layout rendering, event handlers, and asynchronous storage tasks
├── ui_components.py   # Modular Flet UI components (e.g., patient card creation)
└── utils.py           # Helper utilities for CSV initialization, text parsing, and logging maintenance
```
---
## Prerequisites & Dependencies :

Make sure you have Python 3.8+ installed. The project relies on the following major packages:
* `Flet` - GUI framework built on Flutter.
* `aiofiles` - Asynchronous file I/O operation.

### Getting started :
1. Clone or Download the Repository :
```bash
git clone "https://github.com/01001011011010000110000101101100/Pt-Info"
cd "Data-organizer"
```
2. Create virtual environment (Prefers) :
```bash
python -m venv .venv
```
3. Activate the virtual environment :
```bash
source .venv/bin/activate
```
4. Install all packages from `requirements.txt` via pip :
```bash
pip install -r requirements.txt
```
5. Run the program :
```bash
python main.py
```
