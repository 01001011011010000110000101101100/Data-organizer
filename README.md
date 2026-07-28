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

data_organizer 
├── constants.py       # Defines medical abbreviation dictionary & dynamic CSV/Log path resolution
├── main.py            # Core GUI flow, layout rendering, event handlers, and asynchronous storage tasks
├── ui_components.py   # Modular Flet UI components (e.g., patient card creation)
└── utils.py           # Helper utilities for CSV initialization, text parsing, and logging maintenance

---
## Prerequisites & Dependencies :
Make sure you have Python 3.8+ installed. The project relies on the following major packages:
* Flet - GUI framework built on Flutter.
* aiofiles - Asynchronous file I/O operation.
1. Create virtual environment (Prefers) :
``Bash
python -m venv .venv
``
2. Install all packages from `requirements.txt` via pip :
``Bash
pip install -r requirements.txt
``
### Getting started :
1. Clone or Download the Repository :
``Bash
git clone "https://github.com/01001011011010000110000101101100/Data-organizer"
cd "Data-organizer"
``
2. Activate the virtual environment :
``Bash
source .venv/bin/activate
``
3. Lunch the program :
``Bash
python main.py
``
