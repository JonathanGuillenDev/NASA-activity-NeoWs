import pandas as pd
import requests

response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-01&api_key=KniTOJi4GROISaZHQvWnjuf6GHpuA5g3YZfQYwPX")
data = response.json()

near_earth_objects = data['near_earth_objects']['2024-01-01']
df = pd.DataFrame(near_earth_objects)

df['name'] = df['name'].str.slice(1, -1)
df['date'] = df['close_approach_data'].apply(lambda x: x[0]['close_approach_date'])
df['date'] = pd.to_datetime(df['date'])
df['estimated_diameter_max'] = df['estimated_diameter'].apply(lambda x: x['feet']['estimated_diameter_max'])
df['estimated_diameter_min'] = df['estimated_diameter'].apply(lambda x: x['feet']['estimated_diameter_min'])
df['relative_velocity'] = df['close_approach_data'].apply(lambda x: x[0]['relative_velocity']['miles_per_hour'])
df['miss_distance'] = df['close_approach_data'].apply(lambda x: x[0]['miss_distance']['miles'])

df.drop(columns=['links', 'estimated_diameter','neo_reference_id', 'nasa_jpl_url','is_sentry_object', 'close_approach_data'], inplace=True)

df.to_csv("near_earth_objects.csv", index=False)