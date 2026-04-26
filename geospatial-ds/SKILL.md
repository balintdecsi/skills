---
name: geospatial-ds
description: Best-practice suggestions for geospatial data science in Python — vector data with GeoPandas/Shapely, raster data with rasterio/rioxarray/xarray, OpenStreetMap via OSMnx, geocoding, H3 spatial indexing, basemaps with contextily, and spatial statistics with PySAL/esda/spreg. Use when working with shapefiles, GeoJSON, GeoTIFF, Parquet/GeoParquet, OSM data, coordinate reference systems (CRS), maps, hex grids, or spatial joins.
---

# Geospatial Data Science Best Practices

These are **suggestions**, not absolute rules. Patterns and tooling are based on the user's CEU MSBA course **Geospatial Data Science** (`ceu-geospatial-ds`) — adapt freely to context.

The full course material with worked notebooks, exercises, and solutions lives in `~/repos/ceu/ceu-geospatial-ds/notebooks/`. Topics covered there map directly to the structure of this skill: Shapely geometries → GeoPandas vector data → rasterio/rioxarray rasters → OSMnx + geocoding + H3 spatial indexing.

## When to Use

Auto-apply when the task involves:

- Reading or writing **shapefiles, GeoJSON, GeoPackage, GeoParquet, KML, or GeoTIFF**.
- Anything with `geopandas`, `shapely`, `rasterio`, `rioxarray`, `xarray`, `osmnx`, `h3`, `libpysal`, `esda`, `spreg`, `contextily`, `datashader`, `geopy`.
- Coordinate reference system (CRS) conversion, projections, EPSG codes.
- Spatial joins (point-in-polygon, nearest neighbour, distance-based).
- Map plots, basemaps, choropleths, hex-bin aggregations.
- OpenStreetMap downloads (admin boundaries, POIs, road graphs, buildings).
- Geocoding addresses ↔ coordinates.
- Spatial autocorrelation (Moran's I), spatial regression, hotspot detection.

## Default Stack (what `ceu-geospatial-ds` uses)

| Concern | Library |
|---|---|
| Geometry primitives | `shapely` |
| Vector data tables | `geopandas` |
| Raster (cell grids) | `rasterio` + `rioxarray` (xarray-aware wrapper) |
| N-D scientific arrays | `xarray`, `numpy` |
| OpenStreetMap downloads | `osmnx` |
| Geocoding (address ↔ point) | `geopy` (Nominatim, etc.) |
| Hex spatial index | `h3` (Uber's H3) |
| Basemaps (web tiles) | `contextily` |
| Big-point density rendering | `datashader` |
| Spatial weights / Moran's I | `libpysal`, `esda` |
| Spatial regression | `spreg` |
| Output formats | GeoParquet (default), GeoJSON, Shapefile (legacy) |

The full pinned dependency set is in `ceu-geospatial-ds/pyproject.toml`.

## Core Principles

1. **Always know your CRS.** Every GeoDataFrame has one; mixing them silently is the most common bug. Reproject explicitly with `to_crs(epsg=...)` before any distance/area calculation.
2. **Use a *projected* CRS for distances/areas, a geographic CRS only for storage / lat-lon math.** Web Mercator (`EPSG:3857`) is fine for visual map overlays but distorts areas — use a local equal-area projection (e.g. ETRS89-LAEA `EPSG:3035` for Europe, an appropriate UTM zone, or country-specific) for measurements.
3. **Prefer GeoParquet over Shapefile** for new files. Shapefile is legacy: 10-character column names, no proper Unicode, multi-file payload.
4. **Cache OSM and geocoder results to disk.** Both Nominatim and Overpass throttle. `osmnx` already caches by default — leave it on.
5. **Validate geometries early.** `gdf.is_valid.all()` should be `True`. Fix invalid ones with `geometry.buffer(0)` or `make_valid` before joins.
6. **Spatial joins inflate rows** the same way relational joins do — check row counts before/after.
7. **For aggregating events to areas, prefer H3 hex grids** over arbitrary admin polygons when the question is "where is the density?".

## Coordinate Reference Systems — the must-knows

| EPSG | Name | When |
|---|---|---|
| `4326` | WGS 84 lat/lon | Default for most input data, GeoJSON, GPS |
| `3857` | Web Mercator | Web tiles / contextily basemaps, **not for areas** |
| `3035` | ETRS89-LAEA Europe | Equal-area projection across Europe |
| `32633`, `32634`, … | UTM zones | Local distance/area work in metres |
| Country-specific | e.g. `23700` (HD72/EOV Hungary) | National grids when stakeholders expect them |

```python
gdf = gdf.set_crs(4326)        # only when CRS is missing and you KNOW it's lat/lon
gdf = gdf.to_crs(epsg=3035)    # reproject for area/distance in metres
```

If `gdf.crs is None`, do **not** call `.to_crs(...)` — call `set_crs(...)` first with the *known* source CRS.

## Vector Workflow Cheatsheet

```python
import geopandas as gpd
import shapely

gdf = gpd.read_file("data/ne_110m_admin_0_countries")        # shapefile, GeoJSON, GeoPackage
gdf = gpd.read_parquet("data/cities.parquet")                # GeoParquet — preferred

gdf.crs                                                      # what CRS am I in?
gdf = gdf.to_crs(epsg=3035)                                  # reproject
gdf["area_km2"] = gdf.geometry.area / 1e6                    # only meaningful in projected CRS
gdf["centroid"] = gdf.geometry.centroid

# Spatial join: point-in-polygon
points_with_country = gpd.sjoin(points, countries, how="left", predicate="within")

# Nearest-neighbour join (GeoPandas ≥ 0.10):
nearest = gpd.sjoin_nearest(points, lines, distance_col="dist_m")

# Write
gdf.to_parquet("output/cities.parquet")
```

For a fuller template see [snippets/vector_workflow.py](snippets/vector_workflow.py).

## Raster Workflow Cheatsheet

`rioxarray` gives an xarray-flavoured API on top of `rasterio` — use it by default.

```python
import rioxarray as rxr

raster = rxr.open_rasterio("data/GHS_POP_E2030_GLOBE_R2023A_4326_30ss_V1_0.tif", masked=True)
raster = raster.rio.reproject("EPSG:3035")

# Clip to a polygon
clipped = raster.rio.clip(admin_gdf.geometry, admin_gdf.crs)

# Zonal stats: total population per polygon
clipped.sum().item()

# Resample to coarser resolution
coarse = raster.rio.reproject(raster.rio.crs, resolution=1000)   # 1km cells
```

For batch zonal-stats (many polygons against one raster), see [snippets/zonal_stats.py](snippets/zonal_stats.py).

## OpenStreetMap with OSMnx

`osmnx` calls Overpass and Nominatim; both throttle, so let it cache.

```python
import osmnx as ox

# Boundary by place name
budapest_1 = ox.geocode_to_gdf("Budapest 1st district, Hungary")

# Points of interest inside that polygon (uses Map Features tags)
cafes = ox.features_from_polygon(
    budapest_1.geometry.iloc[0],
    tags={"amenity": "cafe"},
)

# Drivable street network
G = ox.graph_from_place("Budapest, Hungary", network_type="drive")
```

OSM tag reference: <https://wiki.openstreetmap.org/wiki/Map_features>. The `osmnx` user guide is the second most useful link: <https://osmnx.readthedocs.io>.

## H3 Hex Grids (when you need an aggregation grid)

```python
import h3
from shapely.geometry import Polygon

# Point → cell
cell = h3.latlng_to_cell(lat, lng, res=8)        # res 8 ≈ 0.7 km² hex

# Cell → polygon (lat,lng order from H3 → swap to lng,lat for Shapely)
poly = Polygon([(lng, lat) for lat, lng in h3.cell_to_boundary(cell)])

# Cover a polygon with hexes at a resolution
hex_ids = h3.geo_to_cells(admin_geojson, res=8)
```

Resolution guide: 8–11 for urban analytics, 5–7 for regional, 3–4 for global. See <https://h3geo.org/docs/core-library/restable/>.

## Geocoding (address ↔ coordinates)

Nominatim is free, unauthenticated, and **rate-limited to ~1 req/sec**. For >100 addresses, batch with rate limiting and cache aggressively.

```python
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geocoder = Nominatim(user_agent="my-project-name")          # set a real user agent
geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1.1)

df["location"] = df["address"].map(geocode)
df["lat"] = df["location"].map(lambda p: p.latitude  if p else None)
df["lng"] = df["location"].map(lambda p: p.longitude if p else None)
```

For high volume / commercial use, switch to a paid provider (Mapbox, Google, HERE) — Nominatim's terms forbid heavy use.

## Maps with Basemaps (contextily)

```python
import contextily as ctx
import matplotlib.pyplot as plt

ax = gdf.to_crs(epsg=3857).plot(figsize=(8, 8), alpha=0.6, edgecolor="black")
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
ax.set_axis_off()
plt.tight_layout()
```

**Always reproject to `EPSG:3857` before adding a `contextily` basemap** — the tile providers are in Web Mercator.

For 100k+ points, use `datashader` instead of matplotlib scatter.

## Spatial Statistics (PySAL family)

```python
from libpysal.weights import Queen
from esda.moran import Moran, Moran_Local

w = Queen.from_dataframe(gdf, use_index=False)
w.transform = "r"                               # row-standardise

global_moran = Moran(gdf["my_var"].values, w)
print(global_moran.I, global_moran.p_sim)       # global spatial autocorrelation

local = Moran_Local(gdf["my_var"].values, w)    # cluster + outlier per polygon
gdf["lm_q"] = local.q                           # 1=HH, 2=LH, 3=LL, 4=HL
gdf["lm_sig"] = (local.p_sim < 0.05).astype(int)
```

For spatial regression (lag / error / SARMA models): `spreg.OLS`, `spreg.ML_Lag`, `spreg.ML_Error`. Worth it when residuals show spatial autocorrelation — non-spatial OLS will be biased.

## Anti-Patterns to Flag

- **Doing distance / area calculations in `EPSG:4326`** (geographic CRS, units are degrees!).
- **Plotting GeoDataFrame in lat/lon then calling `ctx.add_basemap`** — basemap and data won't align.
- **Spatial-joining without checking row counts** — silent inflation.
- **Calling Nominatim in a tight loop** with no rate limiter or cache.
- **Reading Shapefiles as the default** for new outputs (write GeoParquet instead).
- **Setting CRS with `.set_crs(...)` to "fix" wrong coordinates** — `set_crs` only declares; it does not transform. To transform, use `.to_crs(...)`.
- **Buffering in degrees** because the CRS is `4326` — buffer 0.01° is ~1 km at the equator and ~700 m at 45° latitude. Reproject to metres first.
- **Using `geopandas.sjoin` with default `predicate="intersects"` when you mean `"within"`** — picks up touching polygons.
- **Loading a 10 GB GeoTIFF fully into memory** — use `rioxarray.open_rasterio(..., chunks=True)` (Dask-backed) and clip first.

## Code Snippets

In [snippets/](snippets/):

- `vector_workflow.py` — load → reproject → spatial-join → write GeoParquet template.
- `zonal_stats.py` — population/area/sum-of-raster per polygon, vectorised.
- `osm_pois.py` — pull POIs by tag inside an admin boundary, save as GeoParquet.
- `h3_aggregation.py` — bin point events to H3 hexes and produce a choropleth.
- `geocode_with_cache.py` — rate-limited geocoding with a JSON-on-disk cache.
- `moran_local.py` — global + local Moran's I with cluster-map plot.

## Data Sources Used in the Course (and good for projects)

The notebooks pull from these, all of which are free and well-suited for new projects:

| Source | What | URL |
|---|---|---|
| **Natural Earth** | Country / admin / cultural / physical vector layers (110m, 50m, 10m) | <https://www.naturalearthdata.com/> |
| **OpenStreetMap (via OSMnx)** | POIs, buildings, road graphs, admin boundaries by name | <https://www.openstreetmap.org/>, <https://osmnx.readthedocs.io/> |
| **Nominatim (OSM)** | Free geocoding, ≤1 req/sec | <https://nominatim.openstreetmap.org/> |
| **GHSL — Global Human Settlement Layer (JRC)** | Population grids (`GHS_POP_*`), built-up surface, settlement model. The course uses `GHS_POP_E2030_GLOBE_R2023A_4326_30ss_V1_0.tif`. | <https://ghsl.jrc.ec.europa.eu/datasets.php> |
| **HydroSHEDS / HydroRIVERS** | Global rivers and watersheds (the `rivers_africa_37333` sample in the course is from here) | <https://www.hydrosheds.org/> |
| **Vienna Open Data** | `vienna_districts.geojson` and many city-level layers | <https://www.data.gv.at/> |
| **Geofabrik** | OSM extracts per country/region as `.osm.pbf` (much faster than Overpass for bulk) | <https://download.geofabrik.de/> |
| **Copernicus / Sentinel Hub / Microsoft Planetary Computer** | Free satellite imagery (Sentinel-2 RGB / NDVI / land cover) | <https://www.copernicus.eu/>, <https://planetarycomputer.microsoft.com/> |
| **NASA Earthdata** | DEMs (SRTM), MODIS, Landsat | <https://www.earthdata.nasa.gov/> |
| **Eurostat GISCO** | NUTS administrative boundaries for EU at multiple resolutions | <https://ec.europa.eu/eurostat/web/gisco> |
| **WorldPop** | Population grids per country at ~100 m | <https://www.worldpop.org/> |
| **OpenAQ** | Global air-quality measurements (point data) | <https://openaq.org/> |
| **GeoPandas built-in datasets** | `naturalearth_lowres`, `naturalearth_cities`, `nybb` (NYC boroughs) for quick prototyping | `gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))` |

When pulling new data for a project, default to **GeoParquet** for storage and document the **CRS, source URL, download date, and licence** in a one-line comment next to the load call.

## Further Reference

Inspiration repo (full worked examples):

- `ceu-geospatial-ds/notebooks/` — chapters 2 (Shapely), 3 (vector + GeoPandas), 4 (raster + rioxarray), 5 (OSM, geocoding, H3 spatial indexing, urban analytics exercises).
- `ceu-geospatial-ds/assignments/` — end-to-end assignments combining vector + raster + OSM.

External documentation:

- [GeoPandas user guide](https://geopandas.org/en/stable/docs.html)
- [rioxarray docs](https://corteva.github.io/rioxarray/)
- [OSMnx user guide](https://osmnx.readthedocs.io/)
- [PySAL ecosystem](https://pysal.org/)
- [H3 docs](https://h3geo.org/docs/)
- [contextily docs](https://contextily.readthedocs.io/)
- A nice file-format comparison the course links to: <https://milanjanosov.substack.com/p/geospatial-file-formats>

Companion skills:

- **`analytics-project-setup`** — folder structure, settings, and AGENTS.md for projects that include geospatial components.
- **`ml-modeling`** — for predictive modelling on geospatial features (e.g. nearest-neighbour-derived features, spatial aggregations as ML inputs).
- **`statistical-modeling`** — for spatial regression (PySAL/spreg) and inferential analysis with geospatial data.
- **`data-warehousing`** — for ETL pipelines that include geospatial data sources.

---

*Suggestions, not gospel. When in doubt, **check the CRS first** — it's the answer to most "why is my map weird?" questions.*
