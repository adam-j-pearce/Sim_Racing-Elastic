import irsdk
ir = irsdk.IRSDK()
ir.startup()
#why dopes this not work?
def session_log():
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
    

def something():
    print('hello')

class session_info():
    session_type = "1"
    session_id = "2"
    subsession_id = "3"
    season_id = "4"
    official = "0"

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