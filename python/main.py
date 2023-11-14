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

from pyscript import display


output = Element("output")
laps_df1 = Element("laps_df1")
laps_df2 = Element("laps_df2")
sta = StintAnalyzer()
inp_del_laps_df1 = Element("inp_del_laps_df1")
inp_del_laps_df2 = Element("inp_del_laps_df2")

def read_complete_1(event):

    # event is ProgressEvent
    # content = document.getElementById("content");
    # content.innerText = event.target.result
    process_1(event.target.result)


def read_complete_2(event):

    # event is ProgressEvent
    # content = document.getElementById("content");
    # content.innerText = event.target.result
    process_2(event.target.result)




async def process_file_1(x):
    fileList_1 = document.getElementById('upload_1').files

    for f in fileList_1:
        # reader is a pyodide.JSProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete_1)

        #console.log("done")
        reader.onload = onload_event

        reader.readAsText(f)
    return


async def process_file_2(x):
    fileList_2 = document.getElementById('upload_2').files

    for f in fileList_2:
        # reader is a pyodide.JSProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete_2)

        #console.log("done")
        reader.onload = onload_event

        reader.readAsText(f)
    return


def main():
    
      
    # Create a Python proxy for the callback function
    file_event_1 = create_proxy(process_file_1)
    file_event_2 = create_proxy(process_file_2)

    # Set the listener to the callback
    e1 = document.getElementById("upload_1")
    e1.addEventListener("change", file_event_1, False)
    
    e2 = document.getElementById("upload_2")
    e2.addEventListener("change", file_event_2, False)


def del_laps_df1():
    sta.delete_laps_df1(inp_del_laps_df1.value.split())
    inp_del_laps_df1.clear()
    laps_df1.clear()
    laps_df1.write(sta.get_laps_overview('df1'))
    
def del_laps_df2():
    sta.delete_laps_df2(inp_del_laps_df2.value.split())
    inp_del_laps_df2.clear()
    laps_df2.clear()
    laps_df2.write(sta.get_laps_overview('df2'))


def process_1(data):
    buffer = io.StringIO(data)
    sta.load_df1(buffer)


def process_2(data):
    buffer = io.StringIO(data)
    sta.load_df2(buffer)
    laps_df1.write(sta.get_laps_overview('df1'))
    laps_df2.write(sta.get_laps_overview('df2'))


def laptime():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_laptime_graph()
    output.write(fig)

def speed():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_speed_graph()
    output.write(fig)

def computer_performance():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_computer_performance_graph()
    output.write(fig)

def general_conditions():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_general_conditions_graph()
    output.write(fig)

def car_setup():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_car_setup_graph()
    output.write(fig)

def fuel():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_fuel_graph()
    output.write(fig)    

def tyre_pressure():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_tyre_pressure_graph()
    output.write(fig)

def tyre_temp():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_tyre_temperature_graph()
    output.write(fig)

def ride_height():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_ride_height_graph()
    output.write(fig)

def brake():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_brake_graph()
    output.write(fig)

def throttle():
    hide_import()
    show_output()
    plt.close('all')
    fig = sta.get_throttle_graph()
    output.write(fig)

def how_to():
    hide_import()
    show_output()
    output.write("I describe in detail how everything works")

def import_stint():
    hide_output()
    show_import()

def load_demo_data():
    sta.load_df1("stint_1c.csv")
    sta.load_df2("stint_2c.csv")
    sta.delete_laps_df1([1])
    sta.delete_laps_df2([12, 13])
    laps_df1.write(sta.get_laps_overview('df1'))
    laps_df2.write(sta.get_laps_overview('df2'))


def show_import():
    document.getElementById("import").style.display = "inline";

def hide_import():
    document.getElementById("import").style.display = "none";

def show_output():
    document.getElementById("output").style.display = "inline";

def hide_output():
    document.getElementById("output").style.display = "none";



main()



