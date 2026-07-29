# Butterfly Embedding-Space Field Guide

Testing whether TESSERA satellite embeddings can reveal real ecological
habitat structure from butterfly observation data — first attempted for
Jaffna, Sri Lanka (citizen-science iNaturalist data), then UK Butterfly
Monitoring Scheme (UKBMS/WCBS) sites as a data-richer follow-up.

## Status (as of this session)

**Jaffna:** Pipeline built and run end-to-end. Result: UMAP clusters
reflected *where observations were made* (popular parks/trails), not
species habitat niche — a real, documented finding, not a failure. Full
writeup in `outputs/writeups/jaffna_butterfly_habitat_post.md`. Interactive
field guide in `outputs/figures/jaffna_butterfly_field_guide.html`.

**UK (UKBMS/WCBS):** In progress. ~5,995 systematically-monitored sites,
converted from British National Grid to lat/lon (see `notebooks/02` for
the Northern Ireland grid gotcha). Next step: sample TESSERA embeddings
for year 2022 (2,972 active sites that year), then compare UKBMS
(deliberately-chosen habitat) vs WCBS (randomly-sampled) cluster
separation — the actual test of whether TESSERA carries habitat signal.

## Structure

- `data/raw/` — untouched downloads. Never edit these directly.
- `data/interim/` — cleaned/converted but not analysis-ready (e.g. coordinate conversions).
- `data/processed/` — final, embedding-attached, ready for UMAP.
- `notebooks/eda.ipynb` — pull, clean, and explore the site/occurrence data
  (GBIF pull, BNG→lat/lon conversion, coordinate sanity checks).
- `notebooks/embeddings.ipynb` — sample TESSERA embeddings at each site's
  lat/lon and attach them to the site dataframe.
- `src/` — reusable functions (GBIF verified-pull, coordinate conversion).
- `outputs/` — figures and writeups meant to be shared or published.

## Key lessons encoded in this codebase

1. **Verify filters actually filtered** — GBIF silently collapsed a
   multi-family query to one family with no error. Always check the
   actual field you filtered on, in the actual response.
2. **Don't assume a CRS/grid system — test it** against a known point.
3. **Check year/coverage on a small sample first** before running a slow
   operation (TESSERA sampling, API pulls) on a full dataset.
4. **NaN isn't always a data-quality problem** — sometimes it's structural
   (e.g. WCBS squares having no assigned site name).
5. **A cluster in UMAP means "similar embedding," not "shared ecology"** —
   rule out sampling bias / observer behavior / location proximity before
   drawing an ecological conclusion.
