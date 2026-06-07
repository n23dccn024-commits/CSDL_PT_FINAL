import requests
import pandas as pd
import os

def fetch_authentic_sensor_data():
    print("Dang ket noi Open-Meteo API de tai du lieu IoT (Khu vuc: Ha Noi)...")
    # Da thay doi toa do sang Ha Noi: latitude=21.0285 & longitude=105.8542
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=21.0285&longitude=105.8542&start_date=2023-01-01&end_date=2023-03-31&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        timestamps = data['hourly']['time']
        temps = data['hourly']['temperature_2m']
        humidities = data['hourly']['relative_humidity_2m']
        winds = data['hourly']['wind_speed_10m']

        records = []
        for i in range(len(timestamps)):
            if temps[i] is not None:
                records.append({
                    "timestamp": timestamps[i],
                    "temperature": int(temps[i]),
                    "humidity": humidities[i],
                    "wind_speed": winds[i]
                })

        os.makedirs("dataset", exist_ok=True)
        file_path = "dataset/iot_telemetry_data.csv"
        df = pd.DataFrame(records)
        df.to_csv(file_path, index=False)

        print(f"Thanh cong! Da luu {len(records)} ban ghi thoi tiet Ha Noi vao '{file_path}'.")
    except Exception as e:
        print(f"Loi ket noi mang: {e}")

if __name__ == "__main__":
    fetch_authentic_sensor_data()