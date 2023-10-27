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


graph = Element("graph")
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
    plt.close('all')
    fig = sta.get_laptime_graph()
    graph.write(fig)

def speed():
    plt.close('all')
    fig = sta.get_speed_graph()
    graph.write(fig)

def computer_performance():
    plt.close('all')
    fig = sta.get_computer_performance_graph()
    graph.write(fig)

def general_conditions():
    plt.close('all')
    fig = sta.get_general_conditions_graph()
    graph.write(fig)

def car_setup():
    plt.close('all')
    fig = sta.get_car_setup_graph()
    graph.write(fig)

def fuel():
    plt.close('all')
    fig = sta.get_fuel_graph()
    graph.write(fig)    

def tyre_pressure():
    plt.close('all')
    fig = sta.get_tyre_pressure_graph()
    graph.write(fig)

def tyre_temp():
    plt.close('all')
    fig = sta.get_tyre_temperature_graph()
    graph.write(fig)

def ride_height():
    plt.close('all')
    fig = sta.get_ride_height_graph()
    graph.write(fig)

def brake():
    plt.close('all')
    fig = sta.get_brake_graph()
    graph.write(fig)

def throttle():
    plt.close('all')
    fig = sta.get_throttle_graph()
    graph.write(fig)

def how_to():
    pass

def import_stint():
    pass

main()



