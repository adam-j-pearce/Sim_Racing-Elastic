import irsdk
import time
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers
import json
import csv
from _timetower import *

es = Elasticsearch(
    cloud_id="7cca989133cf49fbbe8251be0453787d:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGVjZjhmMDI4NzZlODRhMDhhNjk1YzM5YmNlODRiYTZlJGE4NDJiOWUwNGM3NDRiYzJiN2I5MTQ3OWExY2I3ZDk2",
    basic_auth=("remote_ingest","BigRedBus2023!")
)

es.info

# this is our State class, with some helpful variables
class State:
    ir_connected = False

# here we check if we are connected to iracing
# so we can retrieve some data

def driver_enter_car():

    global driver_check
    global inc_count
    global fuel_level
    global fuel_start_lap
    global driver_clean_lap
    global lap
    global driver_lap
    global driver_car_id
    global telemetry_array
    global count
        
    driver_check = True
    inc_count = ir['PlayerCarMyIncidentCount']
    fuel_level = ir['FuelLevel']
    fuel_start_lap = 0
    driver_clean_lap = True
    lap = ir['Lap']
    driver_lap = ir['Lap']
    driver_car_id = ir['PlayerCarIdx']
    telemetry_array = []
    count=0

def log_telemetry():

    global telemetry_info
    global telemetry_array
    
    telemetry_info={
        "session":logging.session(),
        "track":logging.track(),
        "driver":logging.driver(),
        "telemetry":logging.telemetry(),
        "fuel":logging.fuel(),
        "meta":logging.meta()
    }

    es.index(
    index='test-telemetry',
    document=json.dumps(telemetry_info)
    )
    telemetry_array.clear()

    return (telemetry_info)

def log_lap():

    global driver_check
    global inc_count
    global driver_clean_lap
    global lap
    global driver_lap
    global driver_car_id
    global lap_log

    if ir['DriverInfo']['DriverIncidentCount'] > inc_count or ir['OnPitRoad'] == True:
        if driver_clean_lap == True:
            print('Lap',ir['Lap'],'Invalidated')
            driver_clean_lap = False
            inc_count = ir['DriverInfo']['DriverIncidentCount']

    lap_log={
        "session":logging.session(),
        "track":logging.track(),
        "car":logging.car(),
        "driver":logging.driver(),
        "lap":logging.lap(),
        "fuel":logging.fuel(),
        "meta":logging.meta()
        }

    es.index(
        index='test-index',
        document=json.dumps(lap_log)
    )

class logging:

    def car():

        global driver_car_id

        car_name = ir['DriverInfo']['Drivers'][driver_car_id]['CarScreenName']
        car_class=""
        car_num = ir['DriverInfo']['Drivers'][driver_car_id]['CarNumber'] 
        power_adj = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassPowerAdjust']
        weight_pen = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassWeightPenalty']
        with open('car_list.csv', "r") as csv_file:
            car_list = csv.reader(csv_file, delimiter = ',')
            for row in car_list:
                if car_name in row[0]:
                    car_class = str(row[1])
    
        car_info={
            "name":car_name,
            "class":car_class,
            "number":car_num,
            "power_adj":power_adj,
            "weight_penalty":weight_pen
        }
        print(car_name)
        print(car_class)
        return car_info

    def fuel():

        global fuel_start_lap
        fuel_level = ir['FuelLevel']

        fuel={
            "start":fuel_start_lap,
            "end":fuel_level,
            "used":fuel_start_lap - fuel_level
        }

        return fuel


    def lap():

        global driver_check
        global inc_count
        global fuel_start_lap
        global driver_clean_lap
        global lap
        global driver_lap
        
        lap_time_s = ir['LapLastLapTime']
        lap_time= str(timedelta(seconds=lap_time_s))
        #takes current fuel level to calculate fuel usage for lap

        #generate the log
        lap={
            "number":driver_lap,
            "time_s":lap_time_s,
            "time":lap_time,
            "clean":driver_clean_lap,
        }
        
        #update variables ready for next lap to be completed.
        driver_lap = driver_lap + 1
        driver_clean_lap = True
        fuel_start_lap = ir['FuelLevel']

    def meta():

        time = ir['SessionTimeofDay']
        track_temp = ir['TrackTemp']

        meta_info = {
            "time":time,
            "track_temp":track_temp
        }

        return meta_info

    def telemetry():

        throttle = ir['Throttle']
        brake = ir['Brake']
        clutch = ir['Clutch']
        steering = ir['SteeringWheelAngle']
        rpm = ir['RPM']
        gear = ir['Gear']
        boost = ir['ManualBoost']
        p2p = ir['PushToPass']
        speed = ir['speed']
        lat_accel = ir['LatAccel']
        long_accel = ir['LongAccel']
        pitch = ir['Pitch']
        roll = ir['Roll']
        velocity_x = ir['VelocityX']
        velocity_y = ir['VelocityY']
        velocity_z = ir['VelocityZ']
        current_lap_time = ir['LapCurrentLapTime']
        lap_dist = ir['LapDist']
        lap_dist_pct = ir['LapDistPct']
        lap_number = ir['Lap']


        telemtry_log = {
            "input":{
                "throttle":throttle,
                "brake":brake,
                "clutch":clutch,
                "steering_angle":steering,
                "rpm":rpm,
                "gear":gear,
                "boost_active":boost,
                "p2p_active":p2p
            },
            "output":{
                "speed":speed,
                "lat_accel":lat_accel,
                "long_accel":long_accel,
                "pitch":pitch,
                "roll":roll,
                "velocity_x":velocity_x,
                "velocity_y":velocity_y,
                "velocity_z":velocity_z,  
            },
            "current_lap": {
                "number": lap_number,
                "time": current_lap_time,
                "distance": lap_dist,
                "percentage": lap_dist_pct
            }
        }

        return(telemtry_log)

    def track():
   
        track_name = ir['WeekendInfo']['TrackDisplayName']
        track_config = ir['WeekendInfo']['TrackConfigName']

        track_info = {
                "name":track_name,
                "configuration":track_config
            }

        return track_info

def check_iracing():

    global driver_check

    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')
        driver_check = False

def loop():

    timetower.loop

if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()
    timetower.initiate

    try:
        while True:
            check_iracing()
            if state.ir_connected:
                loop()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass