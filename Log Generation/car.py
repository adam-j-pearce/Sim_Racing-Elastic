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