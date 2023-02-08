from session import *
from track import *
from driver import *
from datetime import datetime

def log_lap():

    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

    global driver_clean_lap
    global inc_count
    global driver_lap
    global fuel_level_start

    lap = ir['Lap']
    #checks to see if user is the current driver, If not will skip.
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
            driver_lap={
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
            
            #update variables ready for next lap to be completed.
            driver_lap = driver_lap + 1
            fuel_level_start = fuel_level
            driver_clean_lap = True
        
            return(driver_lap)