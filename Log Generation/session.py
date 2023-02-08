def session():

    global session_info
    
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

    return session_info