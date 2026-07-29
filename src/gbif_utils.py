"""
Reusable GBIF occurrence-pull function.

Pulls one family at a time and VERIFIES the 'family' field of the actual
response matches what was requested — GBIF silently collapses repeated
familyKey= params to a single value with no error, so never trust a
multi-family query without checking the results.
"""

import requests
import pandas as pd
import time

PAPILIONOIDEA_FAMILY_KEYS = {
    "Hesperiidae": 6953,
    "Papilionidae": 9417,
    "Pieridae": 5481,
    "Nymphalidae": 7017,
    "Lycaenidae": 5473,
    "Riodinidae": 1933999,
}


def pull_gbif_butterflies(country_code, family_keys=None, limit=300, sleep_secs=1):
    """
    Pull GBIF butterfly occurrences for a country, one family at a time,
    verifying each response actually matches the requested family.

    Parameters
    ----------
    country_code : str
        ISO 3166-1 alpha-2 code, e.g. 'LK', 'GB'.
    family_keys : dict, optional
        {family_name: gbif_key}. Defaults to all Papilionoidea families.
    limit : int
        Max records per family per request (GBIF caps this — check
        data['count'] vs len(results) to see if you're truncating).
    sleep_secs : int
        Delay between requests, polite to GBIF's API.

    Returns
    -------
    pd.DataFrame of verified records across all requested families.
    """
    family_keys = family_keys or PAPILIONOIDEA_FAMILY_KEYS
    base_url = "https://api.gbif.org/v1/occurrence/search"
    all_records = []

    for expected_family, key in family_keys.items():
        params = {
            "country": country_code,
            "familyKey": key,
            "hasCoordinate": "true",
            "hasGeospatialIssue": "false",
            "limit": limit,
        }
        resp = requests.get(base_url, params=params)
        data = resp.json()
        results = data.get("results", [])
        total_available = data.get("count", 0)

        families_returned = set(r.get("family") for r in results)
        ok = families_returned == {expected_family} or len(results) == 0
        status = "OK" if ok else f"MISMATCH — got {families_returned}"
        print(f"{expected_family} (key={key}): {len(results)}/{total_available} "
              f"available — {status}")

        if total_available > limit:
            print(f"  -> NOTE: truncated at {limit} of {total_available} available.")

        if not ok:
            print(f"  -> SKIPPED: key {key} does not map to {expected_family}.")
            continue

        all_records.extend(results)
        time.sleep(sleep_secs)

    df = pd.json_normalize(all_records)
    print(f"\nTotal verified records: {len(df)}")
    return df
