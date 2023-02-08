def track():
    global track_info
    track_name = ir['WeekendInfo']['TrackDisplayName']
    track_config = ir['WeekendInfo']['TrackConfigName']

    track_info = {
            "name":track_name,
            "configuration":track_config
        }

    return track_info