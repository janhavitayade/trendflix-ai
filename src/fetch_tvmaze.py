import requests
import pandas as pd
from datetime import datetime

url = "https://api.tvmaze.com/shows"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    df = pd.DataFrame(data)

    print("\nFirst 5 Shows:\n")
    print(df[["id", "name", "language", "status"]].head())

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"data/tvmaze_shows_{timestamp}.csv"

    df.to_csv(filename, index=False)

    print(f"\nData saved to: {filename}")

else:
    print(f"Error: {response.status_code}")