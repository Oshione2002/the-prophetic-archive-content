# Content publication status

The archive splitting and JSON generation have been completed locally for the currently supplied source set and passed validation.

Processed totals:

- Prophetic Scrolls: 320 unique Scroll numbers, 325 physical JSON documents; multipart Scrolls are 7, 11, 15, 23 and 320.
- Special Writings: 141 JSON documents.
- Translation Alerts: Introduction plus 61 numbered Alerts.
- Monthly Letters: 199 JSON documents.
- Preliminary Pages before Scroll 1: not yet available because their source file has not been supplied.

## What is currently committed

This repository contains the production catalogue/manifests, validation/processing notes, and authentic representative structured-content files covering the main data shapes required for implementation:

- normal paragraph-based Scroll
- multipart Scroll
- Special Writing
- numbered Translation Alert
- Monthly Letter

The remaining generated per-document JSON and large PDF/scan assets are prepared separately for bulk publication. Codex must not fabricate missing archive documents. It should use the committed authentic files as fixtures and keep all content loading driven by the catalogue/manifests so the full dataset can be dropped in without changing app code.

Large Clean PDFs and Original Scans should be distributed as release/static assets rather than normal Git history.
