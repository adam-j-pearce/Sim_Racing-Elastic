import irsdk
import csv
from elasticsearch import Elasticsearch, helpers
import configparser
import json
import time
from _log import logs

ir = irsdk.IRSDK()
ir.startup()

class timetower():

    def initiate():
        
        check_array = []
        return check_array

    def loop(check_array):

        for x in range(len(ir['DriverInfo']['Drivers'])):
            car_num = (ir['DriverInfo']['Drivers'][x]['CarNumber'])
            lap_array = (ir['CarIdxLapCompleted'])
            lap = lap_array[x]
            pit_array = (ir['CarIdxOnPitRoad'])
            pit = pit_array[x]
            tuple_check = (car_num,lap,pit)

            if tuple_check not in check_array:
                check_array.append(tuple_check)
                driver = x
                timetower.generate_log(driver)
                print(check_array)
                break

    def generate_log(driver):
        if (ir['DriverInfo']['Drivers'][driver]['UserName']):
            name=(ir['DriverInfo']['Drivers'][driver]['UserName'])
        if (ir['DriverInfo']['Drivers'][driver]['CarScreenName']):
            car=(ir['DriverInfo']['Drivers'][driver]['CarScreenName'])
        if (ir['DriverInfo']['Drivers'][driver]['IRating']):
            irating=(ir['DriverInfo']['Drivers'][driver]['IRating'])
        if (ir['DriverInfo']['Drivers'][driver]['CarNumber']):
            car_num=(ir['DriverInfo']['Drivers'][driver]['CarNumber'])
        if ir['DriverInfo']['Drivers'][driver]['CarScreenName']:
            car_name=ir['DriverInfo']['Drivers'][driver]['CarScreenName']
            with open('car_list.csv', "r") as csv_file:
                car_list = csv.reader(csv_file, delimiter = ',')
                for row in car_list:
                    if car_name in row[0]:
                        car_class=(str(row[1]))
        team=(ir['DriverInfo']['Drivers'][driver]['TeamName'])
        best_lap_s_array = (ir['CarIdxBestLapTime'])
        last_lap_s_array = (ir['CarIdxLastLapTime'])
        lap_arrays = (ir['CarIdxLapCompleted'])
        pit_arrays = (ir['CarIdxOnPitRoad'])
        pos_array = (ir['CarIdxPosition'])
        class_pos_array = (ir['CarIdxClassPosition'])

        lap = lap_arrays[driver]
        if lap == "-1":
            lap =""
        best_lap_s = best_lap_s_array[driver]
        if best_lap_s == "-1":
            best_lap_s ="" 
        last_lap_s = last_lap_s_array[driver]
        if last_lap_s == "-1":
            last_lap_s =""
        pit = pit_arrays[driver]
        pos = pos_array[driver]
        class_pos = class_pos_array[driver]
    
        log = {
            "session":logs.session,
            "driver":logs.driver,
            "car":logs.car,
            "position":logs.position,
            "lap":logs.driver_lap,
            "pit":pit,
        }
        es.index(
        index='test-time_tower',
        document=json.dumps(log)
        )

config = configparser.ConfigParser()
config.read('example.ini')

es = Elasticsearch(
    cloud_id="7cca989133cf49fbbe8251be0453787d:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGVjZjhmMDI4NzZlODRhMDhhNjk1YzM5YmNlODRiYTZlJGE4NDJiOWUwNGM3NDRiYzJiN2I5MTQ3OWExY2I3ZDk2",
    basic_auth=("remote_ingest","BigRedBus2023!")
)

es.info

check_array = timetower.initiate()
try:
    while True:
        driver = timetower.loop(check_array)
        time.sleep(1)
except: KeyboardInterrupt
pass