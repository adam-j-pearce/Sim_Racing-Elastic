import irsdk

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