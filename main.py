import irsdk
import time
from time import gmtime,strftime
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers
import json
import csv

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
        "@timestamp":timestamp,
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
        "@timestamp":timestamp,
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

def log_timetower():

    driver_count=(len(ir['DriverInfo']['Drivers']))
    driver_array = [range(driver_count)]
    for x in range(driver_count):
        if ir['DriverInfo']['Drivers'][x]['UserName']:
            driver_array.append(ir['DriverInfo']['Drivers'][x]['UserName'])

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

    def driver():
    
        global driver_info

        driver_car_id = ir['PlayerCarIdx']

        driver_name = ir['DriverInfo']['Drivers'][driver_car_id]['UserName']
        driver_id = ir['DriverInfo']['Drivers'][driver_car_id]['UserID']
        if ir['DriverInfo']['Drivers'][driver_car_id]['TeamName'] == 1:
            team = ir['DriverInfo']['Drivers'][driver_car_id]['TeamName']
        else: 
            team = ''
        irating = ir['DriverInfo']['Drivers'][driver_car_id]['IRating']
        license = ir['DriverInfo']['Drivers'][driver_car_id]['LicString']
    
        driver_info = {
            "name":driver_name,
            "id":driver_id,
            "team":team,
            "irating":irating,
            "license":license
        }
        
        return driver_info

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

    def session():
   
        session = ir['WeekendInfo']['EventType']
        session_id = ir['WeekendInfo']['SessionID']
        subsession_id = ir['WeekendInfo']['SubSessionID']
        season_id = ir['WeekendInfo']['SeasonID']
        official = ir['WeekendInfo']['Official']

        if str(ir['WeekendInfo']['EventType']) == "Test":
            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
            session_id == "Testing-",timestamp

        if official == "0":
            official = False
        else:
            official = True

        session_info = {
                "type":session,
                "id":session_id,
                "sub_id":subsession_id,
                "season":season_id,
                "official":official
            }

        return session_info

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

    global timestamp
    global driver_check
    global driver_info
    global lap
    global driver_lap
    
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

    if ir['IsOnTrack'] == False:
        driver_check == False
    
    log_timetower()

    if ir['IsOnTrack'] == True:
        if driver_check == False:
            driver_enter_car()
    lap = ir['Lap']
    if lap > driver_lap and ir['LapLastLapTime'] > 0:
        log_lap()
    log_telemetry()


if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        while True:
            check_iracing()
            if state.ir_connected:
                loop()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass