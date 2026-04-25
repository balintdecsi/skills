"""Rate-limited geocoding via Nominatim with a JSON-on-disk cache.

Pattern from `ceu-geospatial-ds/notebooks/5.2_geocoding.ipynb`, hardened for batch use.

Nominatim usage policy: ≤ 1 request/second, real `User-Agent`, no bulk-geocoding-without-permission.
For large jobs (> a few thousand) switch to a paid provider (Mapbox / Google / HERE)
or self-host Nominatim.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


class CachedGeocoder:
    """Thin wrapper that caches address → (lat, lon) on disk."""

    def __init__(
        self,
        cache_path: str | Path = ".geocode_cache.json",
        user_agent: str = "my-project (contact@example.com)",
        min_delay_seconds: float = 1.1,
    ):
        self.cache_path = Path(cache_path)
        self.cache: dict[str, list[float] | None] = (
            json.loads(self.cache_path.read_text()) if self.cache_path.exists() else {}
        )
        geocoder = Nominatim(user_agent=user_agent)
        self._geocode = RateLimiter(
            geocoder.geocode,
            min_delay_seconds=min_delay_seconds,
            error_wait_seconds=5.0,
            max_retries=3,
            swallow_exceptions=False,
        )

    def __call__(self, address: str) -> tuple[float, float] | None:
        if address in self.cache:
            cached = self.cache[address]
            return tuple(cached) if cached else None
        loc = self._geocode(address)
        result = (loc.latitude, loc.longitude) if loc else None
        self.cache[address] = list(result) if result else None
        self._flush()
        return result

    def _flush(self) -> None:
        self.cache_path.write_text(json.dumps(self.cache))

    def geocode_series(self, addresses: pd.Series) -> pd.DataFrame:
        """Vectorised over a pandas Series. Returns a DataFrame with lat / lon columns."""
        results = [self(addr) for addr in addresses]
        return pd.DataFrame(
            {
                "lat": [r[0] if r else None for r in results],
                "lon": [r[1] if r else None for r in results],
            },
            index=addresses.index,
        )


if __name__ == "__main__":
    addresses = pd.Series(
        [
            "175 5th Avenue, New York, NY",
            "Budapest, Vadasz utca 15",
            "Vienna, Stephansplatz 1",
        ]
    )
    g = CachedGeocoder()
    print(g.geocode_series(addresses))
