import irsdk
import csv
import datetime
import time

ir = irsdk.IRSDK()
ir.startup()

class logs():

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

    def driver(driver_car_id):

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

    def car(driver_car_id):

        car_class = ""
        car_num = ir['DriverInfo']['Drivers'][driver_car_id]['CarNumber']
        car_name = ir['DriverInfo']['Drivers'][driver_car_id]['CarScreenName']
        with open('car_list.csv', "r") as csv_file:
                car_list = csv.reader(csv_file, delimiter = ',')
                for row in car_list:
                    if car_name in row[0]:
                        car_class = str(row[1])
        power_adj = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassPowerAdjust']
        weight_pen = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassWeightPenalty']

        car = {
            "name":car_name,
            "class":car_class,
            "number":car_num,
            "power_adj":power_adj,
            "weight_penalty":weight_pen
        }

        return car

    def position(driver_class_id):

        pos_array = ir['CarIdxPosition']
        class_pos_array = ir['CarIdxClassPosition']
        pos = pos_array[driver_class_id]
        class_pos = class_pos_array[driver_class_id]

        position = {
            "overall":pos,
            "class":class_pos
        }

        return position

    def driver_lap(driver_car_id):

        best_lap_s_array = ir['CarIdxBestLapTime']
        last_lap_s_array = ir['CarIdxLastLapTime']
        lap_arrays = ir['CarIdxLapCompleted']
        lap = lap_arrays[driver_car_id]
        best_lap_s = best_lap_s_array[driver_car_id]
        last_lap_s = last_lap_s_array[driver_car_id]
        best_lap = time.strftime("%M:%S", time.gmtime(best_lap_s))
        last_lap = time.strftime("%M:%S", time.gmtime(last_lap_s))
        pointer = best_lap_s.find('.')
        best_lap = best_lap & best_lap_s[pointer::4]
        pointer = last_lap_s.find('.')
        last_lap = last_lap & last_lap_s[pointer::4]

        lap = {
            "number":lap,
            "time":{
                "seconds":last_lap_s,
                "formated":last_lap
            },
            "best":{
                "seconds":best_lap_s,
                "formated":best_lap
            },
        }

        return lap