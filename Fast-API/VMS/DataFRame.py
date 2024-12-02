import requests
import pandas as pd

try:
    # Fetch data from the volunteers API
    volunteers_api = requests.get("http://localhost:8000/volunteers/volunteers/")
    volunteers_api.raise_for_status()  # Raise an error for HTTP issues
    volunteers_data = volunteers_api.json()  # Convert response to JSON

    # Fetch data from the events API
    events_api = requests.get("http://localhost:8000/events/events/")
    events_api.raise_for_status()  
    events_data = events_api.json()  

    # Convert JSON data (list) directly to Pandas DataFrames
    volunteers_df = pd.DataFrame(volunteers_data)  
    events_df = pd.DataFrame(events_data)  

    merged_df = pd.merge(volunteers_df, events_df, how="inner", left_on="volunteer_id", right_on="event_id")

    #2. Describing the merged dataframe
    print("Merged Data Shape:")
    print(f"Rows: {merged_df.shape[0]}, Columns: {merged_df.shape[1]}")
    print(f"{merged_df.describe()}")
    print(f"{merged_df.info()}")

    #3. Find and replace null values
    print(merged_df.isnull().sum())

    #3. Replace null values
    merged_df.fillna({'name': 'Unknown', 'email': 'Unknown', 'event_name': 'Unknown', 'location': 'Unknown'}, inplace=True)

    #4. Basic DAta Processing 
    merged_df = pd.get_dummies(merged_df, columns=['skills', 'description'], drop_first=True)
    merged_df.drop_duplicates(inplace=True)

    #5. Creating new features
    merged_df['event_datetime'] = pd.to_datetime(merged_df['date'] + ' ' + merged_df['time'], errors='coerce', dayfirst=False)

    bins = [0, 30, 45, 60, 100]  
    labels = ['18-30', '31-45', '46-60', '60+']  
    merged_df['age_category'] = pd.cut(merged_df['age'], bins=bins, labels=labels, right=False)

    print(f"{merged_df.info()}")

except requests.exceptions.RequestException as e:
    print(f"HTTP Request error: {e}")
except Exception as e:
    print(f"Error: {e}")
