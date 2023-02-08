from session import *
from track import *
from driver import *
from datetime import datetime

def log_telemtry():

    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

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
        "session":session(),
        "track":track(),
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

    return(telemtry_log)