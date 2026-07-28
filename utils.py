import csv, os
from io import StringIO
from logging import getLogger
from constants import CSV_FILE, LOG_FILE, MEDICAL_ABBREVIATIONS

from aiofiles import open as af_open

logger = getLogger(__name__)

async def init_csv(): # initialize CSV file
    if not os.path.exists(CSV_FILE):

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["Bed no.", "Pt.Name", "NID", "SP", "DIET", "RES", "Dx", "Cx"]) 
        csv_content = output.getvalue()
        output.close()

        async with af_open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            await file.write(csv_content)

        logger.info("The file has initialized")

    logger.info('CSV file is already exists')


async def clear_logging_file():
    async with af_open(LOG_FILE, mode='w') as l:
        await l.write('')


def clear_shortcut_inputs(text: str) -> str: 
    try :
        words = text.strip().split()

        if len(words) > 1: # If the nurse enter more than one word that means he did not enter an abbreviation. Thus, return the text as will as it was entered 
            return " ".join([w.title() for w in words])  
        
        cleaned_word = []
        word = words[0]

        symbols =  [',', '.', '/', '(', ')', ';', '=', '!', '@', '#', '$', '%', '^', '&', '*', '_', '-', '\\']
        pure_word = "".join([char for char in word if char not in symbols])

        if pure_word.lower() in MEDICAL_ABBREVIATIONS :
            cleaned_word.append("".join([w.upper() for w in pure_word]))
            
        else :
            cleaned_word.append("".join(pure_word))

        return "".join(cleaned_word)
    except Exception as er :
        logger.error(f"An error occurred while clearing shortcuts. Mor info : {er}")