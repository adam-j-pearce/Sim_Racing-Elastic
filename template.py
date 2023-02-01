driver_car_id = ir['PlayerCarIdx']

def car():
    car_name = ir['DriverInfo']['Drivers'][driver_car_id]['CarScreenName']
    car_class = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassShortName']
    car_num = ir['DriverInfo']['Drivers'][driver_car_id]['CarNumber'] 
    power_adj = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassPowerAdjust']
    weight_pen = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassWeightPenalty']
    
    car_info={
        car: {
            "name":car_name,
            "class":car_class,
            "number":car_num,
            "power_adj":power_adj,
            "weight_penalty":weight_pen
        }
    }    
        
def driver():
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

def session():
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

def track():
    track_name = ir['WeekendInfo']['TrackDisplayName']
    track_config = ir['WeekendInfo']['TrackConfigName']

    track_info = {
        "track":{
            "name":track_name,
            "configuration":track_config
        }
    }

