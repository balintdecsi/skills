"""Pull POIs from OpenStreetMap inside an admin boundary and save as GeoParquet.

Pattern from `ceu-geospatial-ds/notebooks/5.1_osm.ipynb`.

`osmnx` caches HTTP responses to disk by default — leave it on. Re-runs are fast and
won't hammer the Overpass / Nominatim servers.

OSM tag reference: https://wiki.openstreetmap.org/wiki/Map_features
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import osmnx as ox

OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)


def pois_in_place(
    place_query: str,
    tags: dict[str, str | bool | list[str]],
) -> gpd.GeoDataFrame:
    """Geocode a place name to a polygon, then return all OSM features matching tags inside it.

    Examples
    --------
    >>> pois_in_place("Budapest 1st district, Hungary", {"amenity": "cafe"})
    >>> pois_in_place("Vienna, Austria",                {"shop": True})        # any shop
    >>> pois_in_place("Berlin, Germany",                {"leisure": ["park", "garden"]})
    """
    boundary = ox.geocode_to_gdf(place_query)
    polygon = boundary.geometry.iloc[0]
    pois = ox.features_from_polygon(polygon, tags=tags)
    if pois.crs is None:
        pois = pois.set_crs(4326)
    return pois


def save_pois(pois: gpd.GeoDataFrame, name: str) -> Path:
    """Drop unhashable list-valued columns OSM sometimes returns, then write GeoParquet."""
    list_cols = [
        c for c in pois.columns
        if pois[c].apply(lambda v: isinstance(v, list)).any()
    ]
    if list_cols:
        pois = pois.copy()
        pois[list_cols] = pois[list_cols].astype(str)
    path = OUT_DIR / f"{name}.parquet"
    pois.to_parquet(path)
    return path


if __name__ == "__main__":
    cafes = pois_in_place(
        "Budapest 1st district, Hungary",
        tags={"amenity": "cafe"},
    )
    print(f"Found {len(cafes):,} cafes.")
    save_pois(cafes, "budapest_1_cafes")
