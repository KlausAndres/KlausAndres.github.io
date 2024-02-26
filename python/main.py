from StintAnalyzer import StintAnalyzer
from pyscript import display


from js import document, FileReader, window
from pyodide.ffi import create_proxy
import io


sta = StintAnalyzer()

OUTPUT_ID = 'output'
OUTPUT = document.getElementById('output')
IMPORT = document.getElementById('import')
LAPS_DF1_ID = 'laps_df1'
LAPS_DF2_ID = 'laps_df2'
INP_DEL_LAPS_DF1 = document.getElementById('inp_del_laps_df1')
INP_DEL_LAPS_DF2 = document.getElementById('inp_del_laps_df2')

def read_complete_1(event):
    process_1(event.target.result)


def read_complete_2(event):
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


def del_laps_df1(e):
    sta.delete_laps_df1(INP_DEL_LAPS_DF1.value.split())
    INP_DEL_LAPS_DF1.value = ''
    display(sta.get_laps_overview('df1'), target=LAPS_DF1_ID, append=False)


def del_laps_df2(e):
    sta.delete_laps_df2(INP_DEL_LAPS_DF2.value.split())
    INP_DEL_LAPS_DF2.value = ''
    display(sta.get_laps_overview('df2'), target=LAPS_DF2_ID, append=False)


def process_1(data):
    buffer = io.StringIO(data)
    sta.load_df1(buffer)


def process_2(data):
    buffer = io.StringIO(data)
    sta.load_df2(buffer)
    display(sta.get_laps_overview('df1'), target='laps_df1', append=False)
    display(sta.get_laps_overview('df2'), target='laps_df2', append=False)


def laptime(e):
    hide_import()
    show_output()
    fig = sta.get_laptime_graph()
    display(fig, target=OUTPUT_ID, append=False)

def speed(e):
    hide_import()
    show_output()
    fig = sta.get_speed_graph()
    display(fig, target=OUTPUT_ID, append=False)

def computer_performance(e):
    hide_import()
    show_output()
    fig = sta.get_computer_performance_graph()
    display(fig, target=OUTPUT_ID, append=False)

def general_conditions(e):
    hide_import()
    show_output()
    fig = sta.get_general_conditions_graph()
    display(fig, target=OUTPUT_ID, append=False)

def car_setup(e):
    hide_import()
    show_output()
    fig = sta.get_car_setup_graph()
    display(fig, target=OUTPUT_ID, append=False)

def fuel(e):
    hide_import()
    show_output()
    fig = sta.get_fuel_graph()
    display(fig, target=OUTPUT_ID, append=False)    

def tyre_pressure(e):
    hide_import()
    show_output()
    fig = sta.get_tyre_pressure_graph()
    display(fig, target=OUTPUT_ID, append=False)

def tyre_temp(e):
    hide_import()
    show_output()
    fig = sta.get_tyre_temperature_graph()
    display(fig, target=OUTPUT_ID, append=False)

def ride_height(e):
    hide_import()
    show_output()
    fig = sta.get_ride_height_graph()
    display(fig, target=OUTPUT_ID, append=False)

def brake(e):
    hide_import()
    show_output()
    fig = sta.get_brake_graph()
    display(fig, target=OUTPUT_ID, append=False)

def throttle(e):
    hide_import()
    show_output()
    fig = sta.get_throttle_graph()
    display(fig, target=OUTPUT_ID, append=False)

def how_to(e):
    hide_import()
    show_output()
    display(sta.get_speed_per_lap(window.innerWidth), target=OUTPUT_ID, append=False)
    display(sta.get_speed_comparision(window.innerWidth), target=OUTPUT_ID, append=True)
    display(sta.get_speed_track_map(window.innerWidth), target=OUTPUT_ID, append=True)
    
    figures = sta.get_constancy_comparision(window.innerWidth)
    
       
    display(figures[0], target=OUTPUT_ID, append=True)
    display(figures[1], target=OUTPUT_ID, append=True)





def import_stint(e):
    hide_output()
    show_import()

def load_demo_data(e):
    sta.load_df1("stint_1c.csv")
    sta.load_df2("stint_2c.csv")
    sta.delete_laps_df1([1])
    sta.delete_laps_df2([12, 13])
    display(sta.get_laps_overview('df1'), target='laps_df1', append=False)
    display(sta.get_laps_overview('df2'), target='laps_df2', append=False)

def show_import():
    IMPORT.style.display = "block";

def hide_import():
    IMPORT.style.display = "none";

def show_output():
    OUTPUT.style.display = "block";

def hide_output():
    OUTPUT.style.display = "none";

# main()
load_demo_data(0)




