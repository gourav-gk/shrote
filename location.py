import gpsd


def get_gps_data():
    # Connect to the GPSD daemon
    gpsd.connect()

    # Get the current GPS data
    packet = gpsd.get_current()

    if packet.mode < 2:
        print("Waiting for GPS fix...")
        return None

    latitude = packet.lat
    longitude = packet.lon
    altitude = packet.alt

    return {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude
    }


try:
    while True:
        gps_data = get_gps_data()
        if gps_data:
            print(
                f"Latitude: {gps_data['latitude']}, Longitude: {gps_data['longitude']}, Altitude: {gps_data['altitude']}")
except KeyboardInterrupt:
    print("GPS data reading stopped.")