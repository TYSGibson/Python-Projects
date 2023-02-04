## REFERENCE FILE FOR PYSIMPLEGUI: https://www.pysimplegui.org/en/latest/call%20reference/#combo-element
## OS Side of the GUI

import PySimpleGUI as sg
import pandas as pd
import datetime 

sg.theme('LightBlue5')

##You can clear the selected value of a Combobox by setting its value to an empty string:
# ComboBox.set('')


## Functions that performs: 
# 1) Selected value clearing

def clear_input(window): ### This one is for the Clear button. Clear input function clears all values, including the title of my buttons lmao. So i have to specify more detailed. REFEREMCE: https://stackoverflow.com/questions/72973496/clearing-date-picker-in-pysimplegui
    for key, values in window.key_dict.items():
        if isinstance(values, sg.Combo) or isinstance(values, sg.Input): ## This if loop helps to clear both combobox and input values, successfully ignoring the Button titles. Cant believe this worked.
            values.update(value='')
            
# def clear_input(): ## This one is for the submit button, cause the previous clear input function only clears Input values, combo box values wont get cleared!!!
#     for key in values:
#         window[key]('')
#     return None

OS_Excel = 'C:/Cartridge_Tracking_UI/OS_Cartridge_Tracking/OS_Cartridge_Tracking.xlsx'

df = pd.read_excel(OS_Excel)

Current_Time = datetime.datetime.now() ## I use this line to get the current date and time
Formatted_Current_Time = Current_Time.strftime("%Y-%m-%d   %H:%M:%S")

sg.set_options(font = 12)

layout = [
          [sg.Text('Please fill Up All Details Accordingly!', text_color = 'red', font = 15)], ## Font changes the size of the font
          [sg.Text('Please input current Date ("Y-M-D"  "H:M:S"): ', size = (35,1)), sg.InputText(Formatted_Current_Time, key = 'Date'), sg.CalendarButton('Submission Date', close_when_date_chosen = True, target = 'Date', size= (20,1))], ## Size adjusts the size of the text
          [sg.Text('Please input WWID: ',size = (35,1)), sg.InputText(key = 'WWID')], 
          [sg.Text('Please Input Current Shift: ', size = (35,1)), sg.Combo(['A2A1', 'C2B1','A1D1', 'D1B2', 'B1B2', 'C1A2', 'C1C2'], key = 'Shift', readonly = True)],  
          
          [sg.Text('')],
    
          [sg.Text('Cartridge Details: ', text_color = 'red', font = 15)],
    
          [sg.Text('Link: ', size = (35,1)), sg.InputText(key = 'Link')],
          [sg.Text('Dispenser & Valve Location', size = (35,1)), sg.Combo(['D1V1', 'D1V2', 'D2V1', 'D2V2', 'D3V1', 'D3V2'],key = 'Dispenser & Valve Location', readonly = True)],
          [sg.Text('Cartridge ID Returned', size = (35,1)), sg.InputText(key = 'Cartridge_Returned')],  ## Not defining anything inside sg.InputText() defaults the value index as [0], if we specify a key, the value will be stored as the new key         
         ## Since I can select more than one checkbox, consider radio buttons/Combobox. REFERENCE: https://holypython.com/gui-with-python-checkboxes-and-radio-buttons-pysimplegui-part-ii/
          [sg.Text('Returned Cartridge Type', size = (35,1)), sg.Combo(['RS2-9F', 'RS1-9A', 'RS1-6F', 'RT4-6F' ], key = 'Returned Cartridge Type',readonly = True)], 

         [sg.Text('Cartridge ID Taken', size = (35,1)), sg.InputText(key = 'Cartridge_Taken')],                                 
         [sg.Text('Taken Cartridge Type', size = (35,1)), sg.Combo(['RS2-9F', 'RS1-9A', 'RS1-6F', 'RT4-6F'], key = 'Taken Cartridge Type', readonly = True)], 
                                           
          
          [sg.Text('Reason of Return: ', size = (35,1)), sg.Combo(['New Setup','OOC','EOD/Splashing', 'No Dispense', 'Others'], key = 'Reason', readonly = True), sg.Text('If "Others" selected, input reason, else put N/A: ', size = (35,1)), sg.InputText('N/A' , size = (10,1), key = 'Other Reason')],
    #           [sg.Text('If Other reason selected, input reason, else put N/A: ', size = (35,1)), sg.InputText('N/A' , key = 'Other Reason')],
            
          [sg.Button('Submit'),sg.Button('Clear'), sg.Button('Cancel')] 

          ]

window = sg.Window('Cartridge Tracking GUI', layout)

input_key_list = [key for key, value in window.key_dict.items() if isinstance (value, sg.Combo) or isinstance (value, sg.Input)]## Code to check if all input values are placed: Reference: https://stackoverflow.com/questions/68602498/check-if-all-inputs-has-values-in-pysimplegui
 ## REFERENCE FOR Isinstance https://www.w3schools.com/python/ref_func_isinstance.asp#:~:text=The%20isinstance()%20function%20returns,the%20types%20in%20the%20tuple.
## A more tedious way but easier to understand method to perform form validation: https://www.youtube.com/watch?v=gJLasS_-NX0&list=PLqK_fRVXlXeY89mOYRYGElWbGSwIMoDxC&index=7
    
    
# Event Loop to process "events" and get the "values" of the inputs

while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Clear':
        clear_input(window)
    if event == 'Submit': # If user clicks Submit
        if all(map(str.strip, [values[key] for key in input_key_list])): ## Same reference used as the input_key_list.
            df = df.append(values, ignore_index = True) ## NOTE: Can only append a dict if ignore_index=True
            df = df.drop('Submission Date', axis = 1)
            df.to_excel(OS_Excel, index = False)
            sg.popup('Data Saved!!')
            clear_input(window)
                 
### Python to check if all input values are placed: 
##Reference: 
#https://stackoverflow.com/questions/68602498/check-if-all-inputs-has-values-in-pysimplegui AND 
#https://www.w3schools.com/python/ref_func_all.asp AND 
#https://www.w3schools.com/python/ref_func_map.asp
#https://www.youtube.com/watch?v=gJLasS_-NX0&list=PLqK_fRVXlXeY89mOYRYGElWbGSwIMoDxC&index=6
            
        else:
            sg.popup('Form not completely filled up!')
        
window.close()