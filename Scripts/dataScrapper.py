import fastf1 as ff1
import pandas as pd


ff1.Cache.enable_cache('cache')

year = 2023
gp_name = 'Bahrain'
session_type = 'FP1'

# Load the race session
session = ff1.get_session(year, gp_name, session_type)
session.load()

# Get weather data
weather_data = session.weather_data

# Loop through drivers and get lap data for each driver
for driver in session.drivers:
    driver_data = session.laps.pick_driver(driver)

    # Create an empty list to store lap data
    lap_data_list = []

    for lap in driver_data.itertuples():
        lap_data = {
            'Driver': lap.Driver,
            'LapNumber': lap.LapNumber,
            'LapTime': lap.LapTime.total_seconds() if lap.LapTime is not pd.NaT else None,
            'Compound': lap.Compound,
            'Stint': lap.Stint,
            'TrackStatus': lap.TrackStatus,
            'AirTemperature': weather_data['AirTemp'][lap.LapNumber - 1],
            'TrackTemperature': weather_data['TrackTemp'][lap.LapNumber - 1],
            'Humidity': weather_data['Humidity'][lap.LapNumber - 1],
            'Pressure': weather_data['Pressure'][lap.LapNumber - 1],
            'WindSpeed': weather_data['WindSpeed'][lap.LapNumber - 1],
            'WindDirection': weather_data['WindDirection'][lap.LapNumber - 1]
        }
        lap_data_list.append(lap_data)

    # Convert the list of dictionaries to a DataFrame
    lap_df = pd.DataFrame(lap_data_list)

    # Clean the driver's name to avoid invalid characters in the filename
    clean_driver_name = driver.replace('/', '_').replace('\\', '_')

    # Save the DataFrame to a CSV file with the driver's name
    lap_df.to_csv(f'LapData_DriverNumber_{clean_driver_name}_{session.name}.csv', index=False)

print('Lap data for each driver has been saved to individual CSV files.')
