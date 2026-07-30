# Butterfly Embedding-Space Field Guide

Does a TESSERA satellite embedding know good butterfly habitat when it sees
it? Tested against the UK Butterfly Monitoring Scheme (UKBMS/WCBS) site
network — 2,921 sites, each represented by a 128-dimensional embedding
sampled at its location for 2022.

**Live interactive figure:** https://s19835.github.io/tessera-embeddings-habitat/
**Plain-language version (no ML/satellite background needed):** https://s19835.github.io/tessera-embeddings-habitat/story.html

## The question, and why it's asked this way

The original goal was species-level: given a sighting, can the embedding at
that spot tell you which habitat *that species* prefers? That question
turned out to be unanswerable with the data available — too few
observations per species, and imprecise coordinates. So the question was
demoted to the more basic one underneath it: can the embedding tell good
habitat from random land *at all*? UKBMS gives this split for free —
UKBMS sites are transects volunteers chose because they're known good
habitat; WCBS sites are 1 km squares picked completely at random, with no
habitat preference. If the embedding carries no habitat signal, it
shouldn't be able to tell the two groups apart.

## Result

A logistic-regression classifier trained on the raw 128-dim embeddings
(no coordinates) separates UKBMS from WCBS sites:

| Metric | Value |
|---|---|
| Sites (UKBMS / WCBS) | 2,921 total — 2,015 / 906 |
| Majority-class baseline | 69.0% |
| 5-fold CV accuracy | 76.1% (± 1.5%) |
| Permutation test | p = 0.0099 (100 permutations, mean permuted score 66.5%) |
| Lat/lon-only control accuracy | 69.0% — exactly baseline |

Read together: the embedding beats blind guessing by 7.1 points, the gap
isn't chance (permutation test), and it isn't just encoding geography
either (a classifier given only latitude/longitude scores no better than
always guessing the majority class).

The same evidence looked at in 2D (UMAP projection of the 128-dim
embeddings) is far less clean — the two groups' centroids sit almost on
top of each other (centroid distance 2.72 vs. average within-group spread
2.77, ratio 0.98). That's expected: squeezing 128 dimensions down to 2 for
visualization throws away most of what a classifier can use in the full
space. The 2D picture is illustrative, not the actual test.

## Structure

- `data/raw/` — untouched downloads. Never edit these directly.
- `data/processed/` — cleaned, embedding-attached, UMAP-projected. One-way
  pipeline from `raw/`.
- `notebooks/eda.ipynb` — pull, clean, and explore the UKBMS/WCBS site data
  (GBIF pull, British National Grid → lat/lon conversion, coordinate sanity
  checks).
- `notebooks/embeddings.ipynb` — sample TESSERA embeddings at each site's
  lat/lon for 2022 and attach them to the site dataframe.
- `notebooks/umap.ipynb` — UMAP projection, then the actual hypothesis
  test: logistic-regression separability of UKBMS vs. WCBS on the raw
  embeddings, validated with a permutation test and a lat/lon-only control.
- `src/` — reusable functions (GBIF verified-pull, coordinate conversion)
  plus the fitted UMAP reducer and classifier saved from `umap.ipynb`.
- `outputs/figures/habitat_embedding_map.html` — the interactive figure,
  also published via GitHub Pages (`docs/`) at the link above.
- `outputs/figures/story.html` — plain-language public companion page (same
  finding, no ML/satellite background assumed), also published via
  GitHub Pages (`docs/story.html`).

## Key lessons encoded in this codebase

1. **Verify filters actually filtered** — GBIF silently collapsed a
   multi-family query to one family with no error. Always check the
   actual field you filtered on, in the actual response.
2. **Don't assume a CRS/grid system — test it** against a known point.
   Northern Ireland uses British National Grid too, not the Irish National
   Grid — confirmed against Giant's Causeway, not assumed.
3. **Check year/coverage on a small sample first** before running a slow
   operation (TESSERA sampling, API pulls) on a full dataset.
4. **NaN isn't always a data-quality problem** — sometimes it's structural
   (e.g. WCBS squares having no assigned site name, or a point falling in
   a TESSERA tile with no coverage).
5. **A cluster in UMAP means "similar embedding," not "shared ecology"** —
   rule out sampling bias, observer behavior, and location proximity
   before drawing an ecological conclusion.
6. **Separability isn't habitat signal until geography is ruled out** — a
   classifier that separates two groups on embeddings needs a lat/lon-only
   control to check it isn't just encoding location.
