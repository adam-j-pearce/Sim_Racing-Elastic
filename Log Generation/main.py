import irsdk
import time
from datetime import datetime

driver_clean_lap = False
driver_lap = int(1)
inc_count = 0
fuel_level_start = 0

# this is our State class, with some helpful variables
class State:
    ir_connected = False

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')
        session()
        track()


def loop():

    global timestamp
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
    
    if ir['IsOnTrack'] == True:
        driver()
        log_lap()
        log_telemtry()

    print(ir['DriverInfo']['Drivers']['0'])

def session():
    global session_info
    session_type = ir['WeekendInfo']['EventType']
    session_id = ir['WeekendInfo']['SessionID']
    subsession_id = ir['WeekendInfo']['SubSessionID']
    season_id = ir['WeekendInfo']['SeasonID']
    official = ir['WeekendInfo']['Official']

    if official == "0":
        official = False
    else:
        official = True

    session_info = {
            "type":session_type,
            "id":session_id,
            "sub_id":subsession_id,
            "season":season_id,
            "official":official
        }

    return session_info

def track():
    global track_info
    track_name = ir['WeekendInfo']['TrackDisplayName']
    track_config = ir['WeekendInfo']['TrackConfigName']

    track_info = {
            "name":track_name,
            "configuration":track_config
        }

    return track_info

def driver():
    driver_car_id = ir['PlayerCarIdx']
    driver_name = ir['DriverInfo']['Drivers'][driver_car_id]['UserName']
    driver_id = ir['DriverInfo']['Drivers'][driver_car_id]['UserID']
    if ir['DriverInfo']['Drivers'][driver_car_id]['TeamName'] == 1:
        team = ir['DriverInfo']['Drivers'][driver_car_id]['TeamName']
    else: 
        team = 'n/a'
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

def log_lap():

    global driver_clean_lap
    global inc_count
    global driver_lap
    global fuel_level_start

    lap = ir['Lap']
    #firstly checks to see if user is the current driver, If not will skip.
    if ir['IsOnTrack'] == True:
        #If active driver will poll to check if driver is either in the pitlane or incurred incident points to see if lap is valid
        if ir['DriverInfo']['DriverIncidentCount'] > inc_count or ir['OnPitRoad'] == True:
            if driver_clean_lap == True:
                print('Lap',ir['Lap'],'Invalidated')
                driver_clean_lap = False
                inc_count = ir['DriverInfo']['DriverIncidentCount']

     #Check for when driver starts a new lap to record lap information.
    if lap > driver_lap:
        lap_time = ir['LapLastLapTime']
        #takes current fuel level to calculate fuel usage for lap
        fuel_level = ir['FuelLevel']

        #generate the log
        lap_log={
            "@timestamp":timestamp,
            "session":session_info,
            "track":track_info,
            "driver":driver(),
            "lap":{
                "number":driver_lap,
                "time":lap_time,
                "clean":driver_clean_lap
            },
            "fuel":{
                "at_start":fuel_level_start,
                "at_end":fuel_level,
                "used":fuel_level_start - fuel_level
            }
        }
        driver_lap = driver_lap + 1
        fuel_level_start = fuel_level
        driver_clean_lap = True
        print(lap_log)

        #update variables ready for next lap to be completed.

def log_telemtry():

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

    telemtry_log = {
        "@timestamp":timestamp,
        "session":session_info,
        "track":track_info,
        "driver":driver(),
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
        }
    }
    print(telemtry_log)

if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                loop()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass