I tried to build a habitat map from citizen science data. Here's why it didn't work, and what real ecological ground-truth would actually require.

The plan sounded clean: pull butterfly observations from iNaturalist for Jaffna, attach a TESSERA satellite embedding to each one, project to 2D with UMAP, and see whether species cluster by habitat — a niche map built entirely from public data, no fieldwork required.

It didn't work, and the reasons turned out to be more interesting than a working result would have been.

**The data was thinner than it looked.** 192 research-grade butterfly observations for the whole Jaffna region sounds like a dataset until you check species-level counts: most species had one or two sightings. You can't detect clustering with n=1 — there's nothing to cluster against.

**Coordinates lie more than you'd expect.** Three different species turned up sharing an identical GPS point to ten decimal places — physically impossible for independent sightings. The actual cause: one observer's app snapped every upload from an outing to a single low-precision pin (`positional_accuracy: 244` meters, against TESSERA's 10-meter pixels). Not malicious, just how the data gets made. Filtering for this cost roughly a third of an already-small dataset.

**The UMAP told a true story, just not the one I wanted.** Points didn't cluster by species — they clustered by location, regardless of species. A Papilio demoleus sat next to a Danaus chrysippus sat next to a Delias eucharis, all from the same popular garden or lagoon trail. That's not "Jaffna butterflies have no habitat structure" — it's "iNaturalist shows you where people take photos, not where butterflies live." Different question entirely.

**Published field surveys exist for this exact area, and they're a different kind of data altogether.** A 2023 study on Mandaitivu Island's mangrove ecosystem ran 24 systematic site visits over eight months and recorded 13 butterfly species with real habitat context — mangrove vs. non-mangrove, not "wherever a photographer happened to be standing." A 2014 rapid survey by Asela et al. covered the wider Jaffna Peninsula and islets. Neither is citizen science; both involved someone walking a transect on purpose.

**Cross-referencing against GBIF didn't rescue it either.** Pulling every Papilionoidea record GBIF has for Sri Lanka (1,500 records across five families) and filtering to the Jaffna bounding box left **12 records**, 11 of them singleton species. Two independent public sources, combined, still can't support a real niche analysis for this specific region.

**Where this leaves the project:** the embedding-space idea isn't wrong, but citizen-science data can't carry it for Jaffna specifically — there simply aren't enough spatially-precise, species-repeated observations yet. What would actually work:

- Pull TESSERA embeddings at the *known* survey coordinates from the Mandaitivu and Asela studies, and test something narrower and answerable: does a mangrove-site embedding actually look different from a non-mangrove-site embedding? That's a real, testable claim with real ground truth behind it — I haven't done this yet, and the Asela paper's exact site coordinates aren't available online, so this piece is still open.
- Or: run an actual transect survey, systematic and repeated, the way every real butterfly-habitat study in Sri Lanka already does it.

Neither of those is worse than the original plan. They're just honest about what it actually takes to say something true about where butterflies live, instead of where people photograph them.
