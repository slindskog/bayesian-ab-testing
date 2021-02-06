import requests
import pandas as pd

# Get data
df = pd.read_csv("advertisement_clicks.csv")
a = df[df["advertisement_id"] == "A"]
b = df[df["advertisement_id"] == "B"]
a = a["action"].values
b = b["action"].values

print(f"a.mean: {a.mean()}")
print(f"b.mean: {b.mean()}")

i = 0
j = 0
count = 0
while i < len(a) and j < len(b):
    # Quit when there's no data left for either ad
    r = requests.get("http://localhost:8888/get_ad")
    r = r.json()
    if r["advertisement_id"] == "A":
        action = a[i]
        i += 1
    else:
        action = b[j]
        j += 1

    if action == 1:
        # Only click the ad if our dataset determines that we should
        requests.post(
            "http://localhost:8888/click_ad",
            data={"advertisement_id": r["advertisement_id"]},
        )

    # Log some stats
    count += 1
    if count % 50 == 0:
        print(f"Seen {count} ads, A: {i}, B: {j}")
