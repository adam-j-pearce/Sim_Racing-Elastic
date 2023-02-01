import irsdk
import time

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
     
# our main loop, where we retrieve data
# and do something useful with it
def loop():

    driver_car_id = ir['PlayerCarIdx']

    car_name = ir['DriverInfo']['Drivers'][driver_car_id]['CarScreenName']
    car_class = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassShortName']
    car_num = ir['DriverInfo']['Drivers'][driver_car_id]['CarNumber'] 
    power_adj = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassPowerAdjust']
    weight_pen = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassWeightPenalty']
    
    car_info={
        "car": {
            "name":car_name,
            "class":car_class,
            "number":car_num,
            "power_adj":power_adj,
            "weight_penalty":weight_pen
        }
    }    
        
    driver_name = ir['DriverInfo']['Drivers'][driver_car_id]['UserName']
    driver_id = ir['DriverInfo']['Drivers'][driver_car_id]['UserID']
    if ir['DriverInfo']['Drivers'][driver_car_id]['TeamName'] == 1:
        team = ir['DriverInfo']['Drivers'][driver_car_id]['TeamName']
    else: 
        team = 'n/a'
    irating = ir['DriverInfo']['Drivers'][driver_car_id]['IRating']
    license = ir['DriverInfo']['Drivers'][driver_car_id]['LicString']
    
    driver_info = {
        "driver":{
            "name":driver_name,
            "id":driver_id,
            "team":team,
            "irating":irating,
            "license":license
        }
    }

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

    telemetry={
        "telemtry":{
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
        
    }

    session_type = ir['WeekendInfo']['EventType']
    session_id = ir['WeekendInfo']['SessionID']
    subsession_id = ir['WeekendInfo']['SubSessionID']
    season_id = ir['WeekendInfo']['SeasonID']
    official = ir['WeekendInfo']['Official']

    session_info = {
        "session":{
            "type":session_type,
            "id":session_id,
            "sub_id":subsession_id,
            "season":season_id,
            "official":official
        }
    }

    track_name = ir['WeekendInfo']['TrackDisplayName']
    track_config = ir['WeekendInfo']['TrackConfigName']

    track_info = {
        "track":{
            "name":track_name,
            "configuration":track_config
        }
    }

    print(session_info|track_info|driver_info|car_info|telemetry)


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
