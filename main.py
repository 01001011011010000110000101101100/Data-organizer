import logging
import csv
import os
import io
import ui_components as ui
import utils 
import constants as con
from re import match as re_match

from aiofiles import open as af_open
import flet as ft

logger = logging.getLogger(__name__)

#----
# ------------ Files are used ---------
# --------  MAIN PAGE ---------
async def main(page: ft.Page):
#---------- INITIALEZ PAGE  -------------------
    page.title = "Pt.info" 
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "adaptive"
    page.bgcolor = "#0d2f54" 
    page.theme_mode = ft.ThemeMode.DARK

#-----Varibales--------- 
    page.editing_bed_id = None # A global varibale to can enable editing later
    # cards_list = set()
# -----  files  ------
    await utils.init_csv()
    await utils.clear_logging_file()
    logger.info('The app is running')

#------------- INITIALEZ DATA -----------
    input_bg = ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
    text_color = ft.Colors.WHITE 
    border_co = "#0C58D3" 

    bed_num = ft.TextField(label="Bed Number (Bed no.)", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color, on_change=lambda e, : clear_bed_error())
    name_input = ft.TextField(label="Patient Name (Pt.Name)", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color, on_change=lambda e, : clear_name_error()) 
    nid_input = ft.TextField(label="National ID (NID)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color, input_filter=ft.NumbersOnlyInputFilter())
    sp_input = ft.TextField(label="Specialist (SP)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)
    diet_input = ft.TextField(label="Diet", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)  
    res_input = ft.TextField(label="Respiration System (RES)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)
    dx_input = ft.TextField(label="Diagnosis (Dx)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)
    cx_input = ft.TextField(label="Consultation (Cx)", cursor_color="blue", border_color=border_co, border_width=2, bgcolor=input_bg, color=text_color)

    # search_input = ft.TextField(label='Search by the Bed Number...', border_color=border_co, border_width=1, bgcolor=input_bg, color=text_color, width=1000, height=100, max_length=5, on_submit=lambda e, :page.run_task(searching))

    data_list = ft.ListView(expand=True)
    
#-------------- Sub Functions -------------------------
    def show_snack_bar(message : str, bg_color : ft.Colors) -> None: 
        page.show_dialog(ft.SnackBar(content=ft.Text(message, color=ft.Colors.WHITE, weight="bold"),bgcolor=bg_color,duration=2300))
        page.update()


    def edit_button(bed_val, name_val, national_id_val, specialist_val, diet_val, res_val, diagnosis_val, consultation_val) -> None:
        logger.info('User has preesed edit button')

        page.editing_bed_id = bed_val.strip().upper()

        bed_num.value = bed_val
        name_input.value = name_val
        nid_input.value = national_id_val
        sp_input.value = specialist_val
        diet_input.value = diet_val
        res_input.value = res_val
        dx_input.value = diagnosis_val
        cx_input.value = consultation_val

        save_text.value = 'Change' 
        save_style.bgcolor = ft.Colors.BLUE_700

        page.update()


    async def do_sharing_file() -> None:
        logger.info("User try to share the CSV file")
        try :
            
            if os.path.exists(con.CSV_FILE) :
                file = ft.ShareFile.from_path(con.CSV_FILE, name="nurse_data.csv") 

                share = ft.Share() # define the object

                await share.share_files(files=[file], text="Sharing patients data")
                logger.info('Share panel opend successfully')

                return
            
            show_snack_bar("The file does not exist. Please exit from this app and enter later", ft.Colors.RED_700)
            logger.critical("The CSV file does not exist!") # The CSV file is created when the app is running it cannot be unexists
            return
        
        except Exception as e :
            show_snack_bar("An unecepted error occurred pleas try agin later", ft.Colors.RED_700)
            logger.error(f"An error happend when the user press share button. More info : {e}")
            return

    def clear_bed_error() -> None:
        if bed_num.error:
            bed_num.error = None; page.update()
        
    def clear_name_error() -> None:
        if name_input.error:
                name_input.error = None; page.update()

#------------MAIN Functions--------------------------------

    async def load_data() -> None: # load data that in CSV file 

        logger.info('Refreshing the screen of data')
        data_list.controls.clear()#; cards_list.clear()

        try :

            async with af_open(con.CSV_FILE, mode='r', encoding='utf-8') as file:
                content = await file.read()

            lines = content.splitlines()
            reader = csv.reader(lines)
            next(reader, None) # Headers
            
            all_rows = [row for row in reader if row]

            def bed_sort_key(row) :
                bed = row[0]
                value = re_match(r"([A-Z]*)\s*(\d*)", bed)
                if value :
                    letter = value.group(1)
                    number = value.group(2) if value.group(2) else 0
                    return (letter, number)
                else :
                    return (bed, 0)

            all_rows.sort(key=bed_sort_key)

            for row in all_rows:
                if row:
                    
                    row_ui = ui.create_row_ui(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], lambda e, i=row[0]: page.run_task(delete_data, i), lambda e, r= row : edit_button(*r))
                    data_list.controls.append(row_ui)

        except Exception as e:
            show_snack_bar('An error occurred while load data. Exite from the app and enter later', ft.Colors.RED_700)
            logger.error(f'An error occurred while loading data on the user interface : {e}')


    async def add_data() -> None: # Concet with save button and refresh data when the user press it
        """"  check if bed name field and name field is embty or not and upload data to CSV file or change it  """

        if not bed_num.value :
            bed_num.error = "This field is required"; page.update()
            logger.warning('The user has forget enter the bed name')
            return
        if not name_input.value :
            name_input.error = "This field is required"; page.update()
            logger.warning("The user has forget enter the Pt.Name")
            return
        
        
        """  For better UX  """
        bed_num.value = bed_num.value.strip().upper()
        name_input.value = name_input.value.strip().title()
        nid_input.value = nid_input.value.strip()
        sp_input.value = sp_input.value.strip().title()
        diet_input.value = utils.clear_shortcut_inputs(diet_input.value)
        res_input.value = utils.clear_shortcut_inputs(res_input.value)
        dx_input.value = utils.clear_shortcut_inputs(dx_input.value)
        cx_input.value = utils.clear_shortcut_inputs(cx_input.value)
       
        
        try :
            """ Ckecks if the bed that user entered had used before or not """
            async with af_open(con.CSV_FILE, mode='r', encoding='utf-8') as file:
                content = await file.read() 

            lines = content.splitlines() # devided the patient data to can read it as CSV data
            reader = csv.reader(lines) # Read data in Memory for better performance
            rows = list(reader) # Make a list of CSV data to can make iteration on it

            for row in rows:
                if row and row[0].strip().upper() == bed_num.value and row[0] != page.editing_bed_id: # Ckecks if the bed name in CSV content and it does not in editing mode due to when user chose edit for a bed in the CSV file he can edit it
                    bed_num.error = 'This bed has used'
                    logger.warning('The user entred a bed had used before')
                    return

        except Exception as ea:
            show_snack_bar('An unexcept error occurred. Try agin later', ft.Colors.RED_700)
            logger.error(f'An error occurred while reading the CSV file to check if the bed has used before. More info : {ea}')
            return
        
        save_buttom.disabled = True # protaction from double presses on the button
        page.update() # Flet do Automatically update when the function is end but this chang is happens and end in this function.
                        #  Consequently, user canot see the change without this manually update

        try :
            """ Ckecks if this upload is overwrite on previous data or append a new data """
            if page.editing_bed_id is not None:
                async with af_open(con.CSV_FILE, mode='r', encoding='utf-8') as file:
                    content = await file.read()

                lines = content.splitlines()
                reader = csv.reader(lines)
                rows = list(reader)

                output = io.StringIO() 
                writer = csv.writer(output)

                for row in rows:
                    if row and row[0] == page.editing_bed_id :
                        writer.writerow([bed_num.value, name_input.value, nid_input.value, sp_input.value, diet_input.value, res_input.value, dx_input.value, cx_input.value])
                    
                    else :
                        writer.writerow(row) 

                csv_content = output.getvalue()
                output.close()    

                async with af_open(con.CSV_FILE, mode='w', encoding='utf-8') as file:
                    await file.write(csv_content)

                page.editing_bed_id = None 
                save_text.value = "Save";save_style.bgcolor = ft.Colors.GREEN_700

                show_snack_bar('Has changed successfully', ft.Colors.GREEN_700)

            else :

                logger.info("User saving data...")
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow([bed_num.value, name_input.value, nid_input.value, sp_input.value, diet_input.value, res_input.value, dx_input.value, cx_input.value])
                csv_content = output.getvalue()
                output.close()

                async with af_open(con.CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                    await file.write(csv_content)
            
        except Exception as er :
            show_snack_bar('An error occurred while saving data. Try agin later', ft.Colors.RED_700)
            logger.error(f"An error occurred while save or editing data in CSV file : {er}")
            return
        
        finally :
            bed_num.value = ""
            name_input.value = ""
            nid_input.value = ""
            sp_input.value = ""
            diet_input.value = ""
            res_input.value = ""
            dx_input.value = ""
            cx_input.value = ""

            bed_num.error = None; name_input.error = None # Better UX

            await load_data()
            save_buttom.disabled=False;  page.update() # Even if error occurrs, save buttom will be ebale to use agin
            show_snack_bar('Has saved successfully', ft.Colors.GREEN_700); logger.info("Has saved successfully")


    async def delete_data(id_to_delete: str) -> None:
        logger.info("User is deleting a data")
        try :
            async with af_open(con.CSV_FILE, mode='r', encoding='utf-8') as file:
                content = await file.read()

            lines = content.splitlines()
            reader = csv.reader(lines)
            rows = list(reader)

            output = io.StringIO()
            writer = csv.writer(output)

            for row in rows:
                if row and row[0] != id_to_delete:
                    writer.writerow(row)

            csv_content = output.getvalue()
            output.close()

            async with af_open(con.CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                await file.write(csv_content)

        except Exception as e:
            show_snack_bar('An error occurred while deleting data. Try agin later', ft.Colors.RED_700)
            logger.error(f"An error occurred while deleting data. More info : {e}")
            return  

        await load_data()

        show_snack_bar('Has deleted successfully', ft.Colors.GREEN_700); logger.info("Has deleted successfully")



    
#-----------------  Buttons  ---------------------------------
    save_text = ft.Text('Save', size=23, color='white', weight='bold') # The text out of the button object due to can change it to be the editing button and return to be the save button easely
    
    save_style = ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, shape=ft.RoundedRectangleBorder(radius=15), padding=20) # The same ^
    
    save_buttom = ft.Button(content=save_text, on_click=lambda e : page.run_task(add_data), style=save_style, expand=True)

    paint_buttom = ft.Button(content=ft.Text('Share', size=20, weight='bold'),
                             style=ft.ButtonStyle(bgcolor="#121010", side=ft.BorderSide(width=2, color=ft.Colors.BLUE_700),
                                         shape=ft.RoundedRectangleBorder(radius=15), padding=20), expand=True, on_click=lambda e, : page.run_task(do_sharing_file))
    
#----------------------  LOAD DATA ON THE PAGE  -----------------------

    label_re = ft.Text("* Required", color=ft.Colors.YELLOW_ACCENT_700, size=11, weight='bold')

    page.add(
        ft.Text("Add new data :", size=20, weight="bold", color="white"),
        label_re,
        bed_num,
        label_re,
        name_input,
        nid_input,
        sp_input,
        diet_input,
        res_input,
        dx_input,
        cx_input,
        ft.Row([save_buttom, paint_buttom], spacing=10, expand=True),
        ft.Divider(color="blue", thickness=10),
        ft.Text("Saved data :", size=20, weight="bold", color="white"),
        data_list 
    )

    await load_data(); page.update()
# -----------  START RUNNING  ------------
if __name__ == '__main__' :
    ft.run(main)
