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
    print(session_info)

def track():
    track_name = ir['WeekendInfo']['TrackDisplayName']
    track_config = ir['WeekendInfo']['TrackConfigName']

    track_info = {
        "track":{
            "name":track_name,
            "configuration":track_config
        }
    }

    #check for new lap and reset clean_lap, will print new lap number, for self only.
    if ir['Lap'] > lap:
        print('Lap',ir['Lap'],'started')
        lap = ir['Lap']
        clean_lap = 'True'
        lap_time = ir['LapLastLapTime']
        fuel_lap_start = ir['FuelLevel']

        print('last lap:',lap_time)

    #will mark lap as invalid if incident count increases on lap.
    if ir['DriverInfo']['DriverIncidentCount'] > inc_count or ir['OnPitRoad'] == True:
        print('Lap Invalidated')
        clean_lap = 'False'
        inc_count = ir['DriverInfo']['DriverIncidentCount']

def fuel():

    fuel_level = ir['FuelLevel']
    fuel_used_lap = fuel_level - fuel_start_lap
    fuel_info ={
        "fuel":{
            "level":fuel_level,
            "used":fuel_used_lap
        }
    }