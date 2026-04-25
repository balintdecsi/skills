# Geospatial Data Sources

Free / openly licensed data sources used across `ceu-geospatial-ds` and broadly recommended for new projects. When pulling data, **document the CRS, source URL, download date, and licence** next to the load call.

---

## Vector — administrative boundaries, places, transport

| Source | What | URL |
|---|---|---|
| Natural Earth | World admin / cultural / physical layers at 110m, 50m, 10m. The `ne_110m_admin_0_countries` shapefile in the course is from here. Public domain. | <https://www.naturalearthdata.com/> |
| OpenStreetMap (OSM) | Global crowdsourced map: roads, POIs, buildings, landuse, admin boundaries. ODbL licence. | <https://www.openstreetmap.org/> |
| OSMnx | Pythonic OSM downloader — admin boundaries, POIs by tag, drivable graphs. Caches to disk by default. | <https://osmnx.readthedocs.io/> |
| Geofabrik | OSM extracts per country/region as `.osm.pbf` — much faster for bulk than Overpass. | <https://download.geofabrik.de/> |
| Eurostat GISCO | NUTS regions, EU country / regional / commune boundaries at multiple resolutions. | <https://ec.europa.eu/eurostat/web/gisco> |
| GADM | Global administrative areas (countries → districts), free for academic use. | <https://gadm.org/> |
| Vienna Open Data | `vienna_districts.geojson` (used in the course) and many city layers. CC BY 4.0. | <https://www.data.gv.at/> |
| US Census TIGER/Line | US states, counties, tracts, blocks, roads. Public domain. | <https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html> |

---

## Geocoding & addresses

| Source | What | URL / notes |
|---|---|---|
| Nominatim (OSM) | Free, ≤ 1 req/sec, requires a real `User-Agent`. ODbL. | <https://nominatim.openstreetmap.org/> |
| Photon | Faster OSM geocoder, also free. | <https://photon.komoot.io/> |
| Mapbox / Google / HERE | Commercial, paid, higher quality and SLA. | per provider |

For >100 addresses, batch with a rate limiter and cache to disk (see `snippets/geocode_with_cache.py`).

---

## Raster — population, satellite, elevation, climate

| Source | What | URL |
|---|---|---|
| GHSL (JRC Global Human Settlement Layer) | Population grids, built-up surface, settlement model, urban centres. The course uses `GHS_POP_E2030_GLOBE_R2023A_4326_30ss_V1_0.tif`. CC BY 4.0. | <https://ghsl.jrc.ec.europa.eu/datasets.php> |
| WorldPop | Population grids per country at ~100 m. CC BY 4.0. | <https://www.worldpop.org/> |
| Copernicus / Sentinel Hub | Free Sentinel-1 (radar), Sentinel-2 (optical), Sentinel-5P (atmosphere). | <https://www.copernicus.eu/> |
| Microsoft Planetary Computer | STAC catalog of Sentinel, Landsat, NAIP, ECMWF, MODIS — query with `pystac-client`. | <https://planetarycomputer.microsoft.com/> |
| NASA Earthdata | DEMs (SRTM 30 m / 90 m), MODIS, Landsat, GPM precipitation. | <https://www.earthdata.nasa.gov/> |
| OpenTopography | High-res DEMs (SRTM, ALOS, USGS 3DEP). | <https://opentopography.org/> |
| Copernicus DEM (GLO-30) | Global 30 m DEM. | <https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model> |
| ESA WorldCover | Global 10 m land cover (2020, 2021). | <https://worldcover2021.esa.int/> |
| ERA5 (Copernicus Climate) | Global hourly climate reanalysis since 1940. | <https://cds.climate.copernicus.eu/> |

---

## Hydrology / environment

| Source | What | URL |
|---|---|---|
| HydroSHEDS / HydroRIVERS | Global rivers, drainage basins, lakes (the `rivers_africa_37333` sample in the course is from here). CC BY 4.0. | <https://www.hydrosheds.org/> |
| OpenAQ | Global air-quality measurements (point data). | <https://openaq.org/> |
| Global Forest Change (Hansen) | Global tree cover and loss at 30 m, annual. | <https://glad.earthengine.app/view/global-forest-change> |

---

## Built-in / quick-start datasets

For prototyping without downloading anything:

```python
import geopandas as gpd
world  = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
cities = gpd.read_file(gpd.datasets.get_path("naturalearth_cities"))
nyc    = gpd.read_file(gpd.datasets.get_path("nybb"))         # NYC boroughs
```

The `geodatasets` package adds many more (Chicago crashes, US air-quality monitors, etc.):

```python
import geodatasets, geopandas as gpd
gpd.read_file(geodatasets.get_path("geoda.chicago_commpop"))
```

---

## Licence note

Most of the above are CC BY / ODbL / public domain — you must **attribute** in any publication. For commercial use, double-check; OSM derivatives may inherit ODbL share-alike terms.

---

## Format recommendation for outputs

For new files the project produces, prefer:

1. **GeoParquet** (`.parquet`, with `geo` metadata) — columnar, fast, supports modern types.
2. **GeoPackage** (`.gpkg`) — when a single-file SQLite is convenient and downstream tools need it.
3. **GeoJSON** (`.geojson`) — only for small files / web display; verbose, no schema.
4. **Shapefile** (`.shp`) — only when a legacy tool requires it. 10-character column-name limit, multi-file, no Unicode.

```python
gdf.to_parquet("output/cities.parquet")             # preferred
gdf.to_file("output/cities.gpkg",   driver="GPKG")  # convenient
gdf.to_file("output/cities.geojson", driver="GeoJSON")
```
