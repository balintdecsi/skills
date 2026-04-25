"""Zonal statistics: aggregate raster values inside polygons.

Two implementations:

1. `zonal_stats_rioxarray` — clip-per-polygon. Simple, works with any rioxarray DataArray.
2. `zonal_stats_rasterstats` — uses the `rasterstats` package, faster for many polygons.

Inspired by the GHSL population workflow in `ceu-geospatial-ds/notebooks/4.*`.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import rioxarray as rxr
import xarray as xr


def zonal_stats_rioxarray(
    raster_path: str | Path,
    polygons: gpd.GeoDataFrame,
    stats: tuple[str, ...] = ("sum", "mean", "min", "max"),
) -> gpd.GeoDataFrame:
    """Compute summary stats per polygon by clipping the raster to each one.

    Both raster and polygons are first reprojected to a common projected CRS
    (the polygons') so areas/distances are meaningful. Pure rioxarray, no extra deps.
    """
    raster = rxr.open_rasterio(raster_path, masked=True).squeeze()

    if polygons.crs is None:
        raise ValueError("polygons.crs is None — set it before calling zonal_stats")
    raster = raster.rio.reproject(polygons.crs.to_string())

    out = polygons.copy()
    for stat in stats:
        out[f"raster_{stat}"] = np.nan

    for idx, geom in polygons.geometry.items():
        try:
            clipped: xr.DataArray = raster.rio.clip([geom], polygons.crs, drop=True)
        except Exception:
            continue
        values = clipped.values
        values = values[~np.isnan(values)]
        if values.size == 0:
            continue
        for stat in stats:
            out.loc[idx, f"raster_{stat}"] = float(getattr(np, stat)(values))
    return out


def zonal_stats_rasterstats(
    raster_path: str | Path,
    polygons: gpd.GeoDataFrame,
    stats: tuple[str, ...] = ("sum", "mean", "min", "max"),
) -> gpd.GeoDataFrame:
    """Faster alternative using the `rasterstats` package (`pip install rasterstats`)."""
    from rasterstats import zonal_stats as _zs

    records = _zs(
        polygons.geometry,
        str(raster_path),
        stats=list(stats),
        all_touched=False,
        geojson_out=False,
    )
    out = polygons.copy()
    for stat in stats:
        out[f"raster_{stat}"] = [r.get(stat) for r in records]
    return out
