# pip install pandas folium numpy
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMapWithTime
import os

os.chdir('/mnt/c/Users/alexa/Downloads')

CSV = "AIS_midlertidig.csv"

# change these if your CSV uses different names
MMSI, T, LAT, LON = "MMSI", "Time", "Latitude", "Longitude"

DAY = "2023-01-01"
GRID = 0.5  # degrees

chunks = pd.read_csv(CSV, usecols=[MMSI, T, LAT, LON], chunksize=500_000, on_bad_lines="skip")

seen = set()  # (hour, lat_bin, lon_bin, mmsi)
per_hour = [dict() for _ in range(24)]

for c in chunks:
    # parse "20230101_000005" as UTC
    ts = pd.to_datetime(c[T].astype(str), format="%Y%m%d_%H%M%S", errors="coerce", utc=True)
    ok_t = ts.notna()
    c = c[ok_t]
    ts = ts[ok_t]
    if c.empty:
        continue

    # keep only the requested day
    day_mask = (ts.dt.strftime("%Y-%m-%d") == DAY)
    c = c[day_mask]
    ts = ts[day_mask]
    if c.empty:
        continue

    lat = pd.to_numeric(c[LAT], errors="coerce")
    lon = pd.to_numeric(c[LON], errors="coerce")
    mmsi = pd.to_numeric(c[MMSI], errors="coerce")
    ok = lat.notna() & lon.notna() & mmsi.notna()
    if not ok.any():
        continue

    h = ts[ok].dt.hour.astype("int16")
    lat_bin = (lat[ok].astype("float32") / GRID).astype("int32")
    lon_bin = (lon[ok].astype("float32") / GRID).astype("int32")
    mmsi = mmsi[ok].astype("int64")

    tmp = pd.DataFrame({"h": h, "lb": lat_bin, "ob": lon_bin, "m": mmsi}).drop_duplicates()

    for r in tmp.itertuples(index=False):
        key = (int(r.h), int(r.lb), int(r.ob), int(r.m))
        if key in seen:
            continue
        seen.add(key)
        cell = (int(r.lb), int(r.ob))
        per_hour[int(r.h)][cell] = per_hour[int(r.h)].get(cell, 0) + 1

def center(b): return (b + 0.5) * GRID

heat_data = [
    [[center(lb), center(ob), cnt] for (lb, ob), cnt in per_hour[h].items()]
    for h in range(24)
]

all_pts = [p for hour in heat_data for p in hour]
m = folium.Map(location=[all_pts[0][0], all_pts[0][1]] if all_pts else [0, 0],
               zoom_start=8, tiles="CartoDB positron")

HeatMapWithTime(heat_data, index=[f"{DAY} {h:02d}:00" for h in range(24)],
                radius=4, auto_play=True, max_opacity=1, blur= 1).add_to(m)

m.save("ais_heatmap_time.html")
print("saved: ais_heatmap_time.html")