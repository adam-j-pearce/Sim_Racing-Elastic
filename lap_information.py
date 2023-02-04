def driver_lap():
    #firstly checks to see if user is the current driver, If not will skip.
    if ir['IsOnTrack'] == True:
        #If active driver will poll to check if driver is either in the pitlane or incurred incident points to see if lap is valid
        if ir['DriverInfo']['DriverIncidentCount'] > inc_count or ir['OnPitRoad'] == True:
            print('Lap',ir['Lap'],'Invalidated')
            driver_clean_lap = 'False'
            inc_count = ir['DriverInfo']['DriverIncidentCount']

    #Check for when driver starts a new lap to record lap information.
    if ir['Lap'] > driver_lap:
        lap_time = ir['LapLastLapTime']
        #takes current fuel level to calculate fuel usage for lap
        fuel_level = ir['FuelLevel']

        #generate the log
        lap_log={
            "@timestamp":timestamp
            "session":session(),
            "track":track(),
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
        driver_lap = ir['lap']
        fuel_level_start = fuel_level