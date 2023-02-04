## CW Side of the GUI
import PySimpleGUI as sg
import pandas as pd
import datetime 

sg.theme('DarkGreen')
sg.set_options(font=12)

CW_Excel = 'C:/Cartridge_Tracking_UI/CW_Cartridge_Tracking/CW_Cartridge_Tracking.xlsx'

Current_Time = datetime.datetime.now() ## I use this line to get the current date and time
Formatted_Current_Time = Current_Time.strftime("%Y-%m-%d   %H:%M:%S")

df2 = pd.read_excel(CW_Excel)

def clear_input(window): ### This one is for the Clear button. Clear input function clears all values, including the title of my buttons lmao. So i have to specify more detailed. REFEREMCE: https://stackoverflow.com/questions/72973496/clearing-date-picker-in-pysimplegui
    for key, values in window.key_dict.items():
        if isinstance(values, sg.Combo) or isinstance(values, sg.Input) or isinstance(values, sg.Radio): ## This if loop helps to clear both combobox and input values, successfully ignoring the Button titles. Cant believe this worked.
            values.update(value='')

layout = [  
          [sg.Text('Please fill Up All Details Accordingly!', text_color = 'red', font = 15)], ## Font changes the size of the font
          [sg.Text('Please input current Date ("Y-M-D"  "H:M:S"): ', size = (40,1)), sg.InputText(Formatted_Current_Time, key = 'Date'), sg.CalendarButton('Submission Date', close_when_date_chosen = True, target = 'Date', size= (20,1))],
          [sg.Text('Please Input WWID:', size = (40,1)),sg.InputText(key = 'WWID')],
          [sg.Text('Please Input Current Shift: ', size = (40,1)), sg.Combo(['A2A1', 'C2B1','A1D1', 'D1B2', 'B1B2', 'C1A2', 'C1C2'], key = 'Shift', readonly = True)],
    
          [sg.Text('')],
    
          [sg.Text('CARTRIDGE CLEANING & INSPECTION DETAILS: ', text_color = 'red', font = 15)],

          [sg.Text('Cartridge ID: ', size = (40,1)), sg.InputText(key = 'Cartridge_ID')], ## Not defining anything inside sg.InputText() defaults the value index as [0], if we specify a key, the value will be stored as the new key
          [sg.Text('Cartridge Type: ', size = (40,1)), sg.Combo(['RS2-9F', 'RS1-9A', 'RS1-6F', 'RT4-6F'], key = 'Cartridge Type', readonly = True)],
          [sg.Text('Poppet ID Used: ', size = (40,1)), sg.InputText(key = 'Poppet_ID')],
          [sg.Text('Poppet Type Used: ', size = (40,1)), sg.Combo(['9B', '8C'], key = 'Poppet_Type', readonly = True)],
          [sg.Text('Nozzle Condition: ', size = (40,1)), sg.Combo(['GOOD', 'BAD'], size = (6,1) , key = 'Nozzle Condition', readonly = True)],
          [sg.Text('Sealant Condition: ', size = (40,1)), sg.Combo(['GOOD', 'BAD'], size = (6,1) , key  = 'Sealant Condition', readonly = True)],
          [sg.Text('Poppet Condition: ', size = (40,1)), sg.Combo(['GOOD', 'BAD'], size = (6,1) ,key  = 'Poppet Condition', readonly = True)],
          [sg.Text('Poppet Spring Condition: ', size = (40,1)), sg.Combo(['GOOD', 'BAD'], size = (6,1) , key  = 'Poppet Spring Condition', readonly = True)],
    
          [sg.Text('If "BAD" was selected, please remark, else put "N/A":', size = (40,1)), sg.InputText('N/A', key = 'Remark')],
    
          [sg.Button('Submit'), sg.Button('Clear'),sg.Button('Cancel')]
          
          ]
             
            

window = sg.Window('Cartridge Cleaning Tracking UI', layout)

input_key_list = [key for key, value in window.key_dict.items() if isinstance (value, sg.Combo) or isinstance (value, sg.Input)]
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
        
    if event == 'Clear':
        clear_input(window)
        
    if event == 'Submit': # If user clicks Submit
        if all(map(str.strip, [values[key] for key in input_key_list])): ## Same reference used as the input_key_list.
            df2 = df2.append(values, ignore_index = True) ## NOTE: Can only append a dict if ignore_index=True
            df2 = df2.drop('Submission Date', axis = 1)
            df2.to_excel(CW_Excel, index = False)
            sg.popup('Data Saved!!')
            clear_input(window)
        else:
            sg.popup('Form not completely filled up!')

window.close()
