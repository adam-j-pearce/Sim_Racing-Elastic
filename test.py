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
    driver_name = ir['DriverInfo']['Drivers'][driver_car_id]['UserName']
    driver_id = ir['DriverInfo']['Drivers'][driver_car_id]['UserID']
    car_name = ir['DriverInfo']['Drivers'][driver_car_id]['CarScreenName']
    car_class = ir['DriverInfo']['Drivers'][driver_car_id]['CarClassShortName']
    track_name = ir['WeekendInfo']['TrackDisplayName']
    track_config = ir['WeekendInfo']['TrackConfigName']
    event_type = ir['WeekendInfo']['EventType']
    session_id = ir['WeekendInfo']['SessionID']

    print(driver_name, driver_id, car_name, car_class, track_name, track_config, event_type, session_id)

    

   

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
