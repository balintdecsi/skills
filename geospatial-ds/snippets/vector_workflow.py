"""End-to-end vector workflow template: load → reproject → spatial-join → save.

Pattern from `ceu-geospatial-ds/notebooks/3.*`. Adapt column names and CRS to context.
"""

from pathlib import Path

import geopandas as gpd

DATA_IN = Path("data")
DATA_OUT = Path("output")
DATA_OUT.mkdir(exist_ok=True)


def load_layers() -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Read country polygons and a points layer; declare CRS if missing."""
    countries = gpd.read_file(DATA_IN / "ne_110m_admin_0_countries")
    if countries.crs is None:
        countries = countries.set_crs(epsg=4326)

    points = gpd.read_parquet(DATA_IN / "cities.parquet")
    if points.crs is None:
        points = points.set_crs(epsg=4326)
    return countries, points


def reproject_to_metres(
    gdf: gpd.GeoDataFrame, epsg: int = 3035
) -> gpd.GeoDataFrame:
    """Reproject to a *projected* CRS so .area / .length / .distance are in metres."""
    return gdf.to_crs(epsg=epsg)


def attach_country(
    points: gpd.GeoDataFrame, countries: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Point-in-polygon spatial join. Both inputs must share the same CRS."""
    assert points.crs == countries.crs, (points.crs, countries.crs)
    n_before = len(points)
    joined = gpd.sjoin(
        points,
        countries[["NAME", "geometry"]],
        how="left",
        predicate="within",
    )
    if len(joined) != n_before:
        raise RuntimeError(
            f"Spatial join inflated rows: {n_before} → {len(joined)}. "
            "Investigate overlapping polygons before continuing."
        )
    return joined.rename(columns={"NAME": "country_name"}).drop(columns=["index_right"])


def main() -> None:
    countries, points = load_layers()

    countries_m = reproject_to_metres(countries)
    points_m = reproject_to_metres(points)

    countries_m["area_km2"] = countries_m.geometry.area / 1e6
    points_with_country = attach_country(points_m, countries_m)

    points_with_country.to_parquet(DATA_OUT / "cities_with_country.parquet")
    countries_m.to_parquet(DATA_OUT / "countries_eq_area.parquet")

    print(f"Wrote {len(points_with_country):,} points and {len(countries_m):,} polygons.")


if __name__ == "__main__":
    main()
