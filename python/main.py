from StintAnalyzer import StintAnalyzer
from pyscript import Element

import asyncio
import js
from js import document, FileReader
from pyodide.ffi import create_proxy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io

graph_1 = Element("graph_1")
sta = StintAnalyzer()

def read_complete(event):

    # event is ProgressEvent
    # content = document.getElementById("content");
    # content.innerText = event.target.result
    process(event.target.result)



async def process_file(x):
    fileList = document.getElementById('upload').files

    for f in fileList:
        # reader is a pyodide.JSProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete)

        #console.log("done")
        reader.onload = onload_event

        reader.readAsText(f)
    return


def main():
    
      
    # Create a Python proxy for the callback function
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("upload")
    e.addEventListener("change", file_event, False)

def process(data):
    buffer = io.StringIO(data)

    sta.load_df1(buffer)

    fig = sta.get_fuel_graph()
    graph_1.write(fig)    



main()



# sta = StintAnalyzer('stint_1_c.csv', 'stint_2_c.csv', df1_skip_laps=[1], df2_skip_laps=[12, 13])

# display(sta.get_laptime_graph(), target="graph_1")
# display(sta.get_tyre_pressure_graph(), target="graph_2")


# df1 = pd.read_csv('stint_1.csv', skiprows=8, nrows=150000)
# Element('output_1').write(df1)

# df2 = pd.read_csv('stint_2.csv', skiprows=8, nrows=150000)
# Element('output_2').write(df2)


# from StintAnalyzer import StintAnalyzer

# sta : StintAnalyzer = StintAnalyzer(df1_path='C:\Users\klaus\OneDrive\_DATA\Project\iRacing\StintAnalyzer\python\stint_1.csv', df2_path='C:\Users\klaus\OneDrive\_DATA\Project\iRacing\StintAnalyzer\python\stint_2.csv', df1_skip_laps=[1], df2_skip_laps=[12, 13])


# from StintPlaner import StintPlaner
# from pyscript import Element
# from pyscript import display
# from js import document

# # region -- PyScript Elements --
# race_duration = Element("race_duration")
# fuel_consumption = Element("fuel_consumption")
# fuel_reserve = Element("fuel_reserve")
# output = Element("output")
# graph = Element("graph")
# # endregion

# # region -- JavaScript Elements -- 
# js_race_duration = document.getElementById("race_duration")
# js_fuel_consumption = document.getElementById("fuel_consumption")
# js_fuel_reserve = document.getElementById("fuel_reserve")
# js_output = document.getElementById("output")
# # endregion

# # region -- Colors --
# ir_red = "#FD2826"
# ir_blue = "#1E4488"
# color_dict = {'ir_red': ir_red, 'ir_blue' : ir_blue}
# # endregion

# # set true if an error occurs
# error = False

# sp = StintPlaner()

# def compute():

#     if _validate_input():
#         output.write(sp.get_fuel_needed())
#         graph.clear()
#         display(sp.get_graph(), target="graph")


# def _validate_input() -> bool:    
#     # returns True if all input fields get a correct value

#     global error
#     error = False

#     # prepare the output-box for an error message
#     js_output.style.textAlign = 'left'
#     js_output.style.color = ir_red
    
    
#     #region -- verify race_duration --
#     value_race_duration = race_duration.value
#     if value_race_duration == "":
#         _mark_error(js_race_duration, "Hint: Race Duration is missing")
#     elif not value_race_duration.isdigit():
#         _mark_error(js_race_duration, "Hint: Race Duration is no positive whole number.")
#     else:
#         value_race_duration = int(value_race_duration)
#         # is the value inside the range
#         if value_race_duration <= 0:
#             _mark_error(js_race_duration, "Hint: Race Duration must be greater than 0.")
#         elif value_race_duration >= 1000:
#             _mark_error(js_race_duration, "Hint: Race Duration must be less than 1.000.")
#     # endregion


#     #region -- verify fuel_consumption --
#     value_fuel_consumption = fuel_consumption.value
#     if value_fuel_consumption == "":
#         _mark_error(js_fuel_consumption, "Hint: Fuel Consumption is missing.")
#     else:   
#         try:
#             float(value_fuel_consumption)
#             value_fuel_consumption = float(value_fuel_consumption)
#             if value_fuel_consumption <= 0:
#                 _mark_error(js_fuel_consumption, "Hint: Fuel Consumption must be greater than 0.")
#             elif value_fuel_consumption >=100:
#                 _mark_error(js_fuel_consumption, "Hint: Fuel Consumption must be less than 100.")
#         except ValueError:
#             _mark_error(js_fuel_consumption, "Hint: Fuel Consumption is no number.")
#     # endregion


#     #region -- verify fuel_reserve --
#     value_fuel_reserve = fuel_reserve.value
#     if value_fuel_reserve == "":
#         _mark_error(js_fuel_reserve, "Hint: Fuel Reserve is missing.")
#     else:   
#         try:
#             float(value_fuel_reserve)
#             value_fuel_reserve = float(value_fuel_reserve)
#             if value_fuel_reserve <= 0:
#                 _mark_error(js_fuel_reserve, "Hint: Fuel Reseve must be greater than 0.")
#             elif value_fuel_reserve >=100:
#                 _mark_error(js_fuel_reserve, "Hint: Fuel Reserve must be less than 100.")
#         except ValueError:
#             _mark_error(js_fuel_reserve, "Hint: Fuel Reserve is no number.")
#     # endregion


#     if not error:
#         # style output-box as normal
#         js_output.style.textAlign = 'center'
#         js_output.style.color = "black"
#         sp.set_race_duration(value_race_duration)
#         sp.set_fuel_consumption(float(fuel_consumption.value))
#         sp.set_fuel_reserve(float(fuel_reserve.value))
#         return True
#     else:
#         return False


# def _mark_error(_object : object, _message : str)-> None:
#     global error
#     error = True
#     _object.style.borderColor = ir_red
#     output.write(_message)


# def coloring_border(_id : str, _color : str) -> None:
#     # Set the border-color of an input-field to the color. Important during input error handling.
#     document.getElementById(_id).style.borderColor = color_dict[_color]
