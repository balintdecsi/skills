# CRS Cookbook

The single most common geospatial bug: silently mixing coordinate reference systems, or doing distance/area work in `EPSG:4326` and reporting nonsense numbers in degrees-squared.

This file is a focused reference for "what CRS should I use, and how do I switch?". Inspired by patterns across `ceu-geospatial-ds`.

---

## Pick the right CRS for the job

| Job | Use a CRS that is | Concrete example |
|---|---|---|
| Storing input data, GeoJSON, GPS | Geographic, lat/lon | `EPSG:4326` (WGS 84) |
| Web map / contextily basemap | Web Mercator | `EPSG:3857` |
| Distance, area, buffer in metres anywhere in Europe | Equal-area projected | `EPSG:3035` (ETRS89-LAEA) |
| Distance, area, buffer in metres locally | Local UTM zone | `EPSG:32633` (UTM 33N), `EPSG:32634`, … |
| Working with national authority data (HU, DE, UK, …) | National grid | `EPSG:23700` (HD72/EOV, Hungary), `EPSG:25832` (DE), `EPSG:27700` (UK) |
| Equal-area at global scale | World equal-area | `EPSG:6933` (NSIDC EASE-Grid 2.0 global) |

When in doubt, **reproject to a projected CRS in metres before any `.area`, `.length`, `.distance`, or `.buffer`**.

---

## The three CRS verbs

```python
gdf.crs                      # what CRS am I in?  (None = unknown)
gdf = gdf.set_crs(epsg=4326) # DECLARE the CRS — only when it is missing
                              # and you KNOW what it should be. Does NOT move points.
gdf = gdf.to_crs(epsg=3035)  # TRANSFORM coordinates to a new CRS. Moves points.
```

The classic mistake: someone has lat/lon coordinates labelled with the wrong CRS, and they call `.set_crs(...)` to "fix" it. That just relabels — it does not transform. To actually move the geometries, you need `.to_crs(...)` after `.set_crs(...)` declares the *true* source CRS.

---

## Picking a UTM zone automatically

```python
import geopandas as gpd

gdf_4326 = gdf.to_crs(4326)
utm = gdf_4326.estimate_utm_crs()      # returns a pyproj CRS for the data's centroid
gdf_m = gdf.to_crs(utm)
print(utm)                              # e.g. EPSG:32633 for central Europe
```

Use this when you don't want to hardcode a UTM zone and the data is roughly local.

---

## Checklist before any geometric calculation

```python
# 1. Confirm CRS is set and projected (not geographic)
assert gdf.crs is not None, "CRS not set"
assert gdf.crs.is_projected, f"CRS {gdf.crs} is geographic; reproject before geometry math"

# 2. Confirm units are metres (avoid feet, degrees)
assert gdf.crs.axis_info[0].unit_name in ("metre", "meter"), \
    f"Unexpected units: {gdf.crs.axis_info[0].unit_name}"
```

---

## Buffering correctly

`.buffer(d)` interprets `d` in the CRS's units.

```python
# Wrong: buffer 1 km becomes a buffer of 1000 degrees if you forget to reproject.
points_4326.buffer(1000)                      # BAD: units are degrees!

# Right: project to metres, buffer in metres, project back if needed.
points_m   = points_4326.to_crs(epsg=3035)
buffers_m  = points_m.buffer(1000)            # 1 km
buffers_4326 = buffers_m.to_crs(4326)
```

---

## Distances between points

```python
# In metres, properly:
gdf_m = gdf.to_crs(epsg=3035)
gdf_m["dist_to_centroid_m"] = gdf_m.distance(gdf_m.unary_union.centroid)

# Lat/lon great-circle (no reprojection needed) — for rough global distances:
from shapely.geometry import Point
from geopy.distance import geodesic
geodesic((lat1, lon1), (lat2, lon2)).meters
```

For long distances spanning continents, **geodesic** is more accurate than projecting; for local work (≤ a few hundred km), a projected CRS is faster and equivalent.

---

## Plotting with a basemap

`contextily` providers are all in Web Mercator (`EPSG:3857`). Reproject the data to match before adding the basemap:

```python
import contextily as ctx

ax = gdf.to_crs(epsg=3857).plot(figsize=(8, 8), alpha=0.6, edgecolor="black")
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
ax.set_axis_off()
```

If the data is in a *projected* CRS already (e.g. `EPSG:3035`), reprojecting again to `3857` for plotting is fine — the round-trip is small. **What you must not do** is leave the data in `EPSG:4326` and ask `contextily` to add a basemap. The tiles will load somewhere off-screen.
