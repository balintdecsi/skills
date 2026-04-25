"""Global + Local Moran's I — spatial autocorrelation in 30 lines.

Pattern from PySAL / `esda`. When residuals from a non-spatial regression show
significant Moran's I, switch to a spatial regression (`spreg.ML_Lag`, `spreg.ML_Error`).

Cluster code (`local.q`):
    1 = HH (high value, high neighbours)
    2 = LH (low value,  high neighbours)  — outlier
    3 = LL (low value,  low neighbours)
    4 = HL (high value, low neighbours)   — outlier
"""

from __future__ import annotations

import geopandas as gpd
from esda.moran import Moran, Moran_Local
from libpysal.weights import Queen


def moran_global(gdf: gpd.GeoDataFrame, value_col: str, permutations: int = 999) -> Moran:
    """Global Moran's I with a permutation-based p-value."""
    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = "r"
    return Moran(gdf[value_col].values, w, permutations=permutations)


def moran_local(
    gdf: gpd.GeoDataFrame,
    value_col: str,
    permutations: int = 999,
    sig: float = 0.05,
) -> gpd.GeoDataFrame:
    """Attach local Moran's I quadrant + significance flag to each polygon."""
    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = "r"
    local = Moran_Local(gdf[value_col].values, w, permutations=permutations)

    out = gdf.copy()
    out["lm_I"] = local.Is
    out["lm_q"] = local.q
    out["lm_p"] = local.p_sim
    out["lm_sig"] = (local.p_sim < sig).astype(int)
    out["lm_label"] = out.apply(
        lambda r: {1: "HH", 2: "LH", 3: "LL", 4: "HL"}[r["lm_q"]] if r["lm_sig"] else "ns",
        axis=1,
    )
    return out


def plot_lisa_clusters(gdf_with_lisa: gpd.GeoDataFrame, ax=None):
    """Quick LISA cluster map. Expects the output of moran_local()."""
    import matplotlib.pyplot as plt

    colors = {"HH": "#d7191c", "LL": "#2c7bb6", "HL": "#fdae61", "LH": "#abd9e9", "ns": "#f0f0f0"}
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 9))
    for label, color in colors.items():
        sub = gdf_with_lisa[gdf_with_lisa["lm_label"] == label]
        if len(sub):
            sub.plot(ax=ax, color=color, edgecolor="white", linewidth=0.2, label=label)
    ax.legend(loc="lower left")
    ax.set_axis_off()
    ax.set_title("Local Moran's I clusters")
    return ax


if __name__ == "__main__":
    nyc = gpd.read_file(gpd.datasets.get_path("nybb"))
    nyc["area"] = nyc.geometry.area
    res = moran_global(nyc, "area")
    print(f"Global Moran's I = {res.I:.3f}, p = {res.p_sim:.3f}")
