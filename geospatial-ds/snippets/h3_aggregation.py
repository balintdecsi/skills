"""Aggregate a point-event dataset to H3 hex cells and produce a choropleth.

Pattern from `ceu-geospatial-ds/notebooks/5.3_spatial_indexing.ipynb`.

Why H3: hex cells have uniform area (within a resolution), reduce edge-vs-corner artefacts
of square grids, and nest hierarchically. For urban analytics use res 8–11; for regional 5–7.
See https://h3geo.org/docs/core-library/restable/.
"""

from __future__ import annotations

import geopandas as gpd
import h3
import pandas as pd
from shapely.geometry import Polygon


def points_to_h3(
    points: gpd.GeoDataFrame,
    resolution: int = 9,
    value_col: str | None = None,
    agg: str = "count",
) -> gpd.GeoDataFrame:
    """Bin points into H3 cells, return a GeoDataFrame of hex polygons with an aggregate column.

    Parameters
    ----------
    points : must be in EPSG:4326 (lat/lon).
    resolution : H3 resolution (0 = global, 15 = ~0.55 m edges).
    value_col : column to aggregate. If None and agg="count", just counts events per cell.
    agg : "count", "sum", "mean", "max", "min".
    """
    if points.crs is None or points.crs.to_epsg() != 4326:
        points = points.to_crs(4326)

    df = points.copy()
    df["lon"] = df.geometry.x
    df["lat"] = df.geometry.y
    df["h3"] = [
        h3.latlng_to_cell(lat, lng, resolution)
        for lat, lng in zip(df["lat"], df["lon"], strict=True)
    ]

    if agg == "count" or value_col is None:
        agg_df = df.groupby("h3").size().rename("value").reset_index()
    else:
        agg_df = df.groupby("h3")[value_col].agg(agg).rename("value").reset_index()

    agg_df["geometry"] = [
        Polygon([(lng, lat) for lat, lng in h3.cell_to_boundary(cell)])
        for cell in agg_df["h3"]
    ]
    return gpd.GeoDataFrame(agg_df, geometry="geometry", crs="EPSG:4326")


def plot_choropleth(
    hexes: gpd.GeoDataFrame,
    value_col: str = "value",
    title: str = "",
    cmap: str = "viridis",
):
    """Plot the hex grid with a basemap. Reprojects to Web Mercator for contextily."""
    import contextily as ctx
    import matplotlib.pyplot as plt

    web = hexes.to_crs(epsg=3857)
    ax = web.plot(
        column=value_col,
        cmap=cmap,
        legend=True,
        alpha=0.7,
        edgecolor="white",
        linewidth=0.2,
        figsize=(9, 9),
    )
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    ax.set_axis_off()
    if title:
        ax.set_title(title)
    plt.tight_layout()
    return ax
