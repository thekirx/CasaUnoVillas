# CasaUnoVillas

A concept website built for **Casa Uno Villas** — three private-pool villas in Purok 4,
Barangay Santo Domingo, Lubao, Pampanga.

## Deploying

Static site, no framework and no build step on the server. Vercel serves `public/`.

```bash
vercel          # preview
vercel --prod   # production
```

Or import the repo at [vercel.com/new](https://vercel.com/new) — `vercel.json` sets the
output directory, so no dashboard configuration is needed. Framework preset: **Other**.

## Layout

| Path | |
|---|---|
| `public/index.html` | the deployed page (~72 KB, photos referenced from `/img/`) |
| `public/img/` | 13 photographs, ~2 MB, cached immutably for a year |
| `src/template.html` | **the source** — edit this, never the generated files |
| `src/build.py` | regenerates both outputs from the template |
| `pitch/casa-uno-villas.html` | self-contained single file, photos inlined as data URIs |

Two outputs exist because they do different jobs: `public/index.html` is the deployable
site, while `pitch/casa-uno-villas.html` is one file you can email or open offline with
nothing else alongside it.

## Making changes

Edit `src/template.html`, then:

```bash
python3 src/build.py
```

That rewrites `public/index.html` and `pitch/casa-uno-villas.html`. Both are committed,
so **re-run the build and commit the result** — Vercel does not run it. Photos live in
`public/img/`; add one there and reference it as `{{IMG:filename-without-extension}}`.

## What the page does

Entirely front-end. There is no backend and no database.

- Availability calendar with blocked dates and range validation
- Live pricing — weekday/weekend nights, extra-guest charges, 50% deposit
- Direct-versus-Airbnb price comparison
- Photo gallery with lightbox
- Light and dark themes

## About the data

Villa capacities, bed and bath counts, review scores and the Airbnb comparison prices are
the property's own, checked August 2026. **Direct nightly rates are a proposed structure,
not published pricing.** Availability in the calendar is sample data.

The `#owner` section is a pitch addressed to the villa owners. Remove it before using this
as a live guest-facing site.
