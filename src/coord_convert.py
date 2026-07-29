"""
Coordinate conversion for UKBMS-style Easting/Northing data.

IMPORTANT LESSON THIS FILE ENCODES: don't assume Northern Ireland uses
the Irish National Grid just because that's administratively true.
Tested against Giant's Causeway (real coords ~55.24N, 6.51W): the
UKBMS 2023 site dataset records ALL UK countries (including NI) in
British National Grid (EPSG:27700). Always verify a CRS assumption
against a known point before trusting a bulk conversion.
"""

import pandas as pd
from pyproj import Transformer

BNG_TO_WGS84 = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)

# Countries confirmed (empirically, not assumed) to use British National
# Grid in the UKBMS 2023 site location dataset.
BNG_COUNTRIES = ("England", "Scotland", "Wales", "Northern Ireland")


def convert_bng_to_latlon(df, easting_col="Easting", northing_col="Northing",
                            country_col="Country"):
    """
    Convert Easting/Northing to lat/lon for rows in BNG_COUNTRIES.
    Rows outside that list (e.g. Channel Islands, Isle of Man — different
    local grids) get lat/lon = None rather than a silently wrong value.

    Always run the out-of-range sanity check after calling this —
    UK mainland is roughly lat 49-61, lon -9 to 2. Anything outside
    that after conversion means something's wrong upstream.
    """
    def convert_row(row):
        if row[country_col] in BNG_COUNTRIES:
            lon, lat = BNG_TO_WGS84.transform(row[easting_col], row[northing_col])
            return pd.Series({"lat": lat, "lon": lon})
        return pd.Series({"lat": None, "lon": None})

    df = df.copy()
    df[["lat", "lon"]] = df.apply(convert_row, axis=1)
    return df


def sanity_check_latlon(df, lat_col="lat", lon_col="lon",
                          lat_range=(49, 61), lon_range=(-9, 2)):
    """Returns rows with lat/lon outside plausible UK range — should be empty."""
    converted = df.dropna(subset=[lat_col, lon_col])
    out_of_range = converted[
        ~converted[lat_col].between(*lat_range) | ~converted[lon_col].between(*lon_range)
    ]
    print(f"Converted: {len(converted)}, out-of-range: {len(out_of_range)} (should be 0)")
    return out_of_range
