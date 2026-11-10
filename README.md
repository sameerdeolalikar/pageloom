# PageLoom

PageLoom is a local page-composition editor for original posters, cards and workshop handouts. It provides editable text and vector shapes, layer ordering, position locks, keyboard nudging, zoom, clipping notices and measured SVG export. A Python/SQLite backend validates page geometry and saves revisioned documents while the browser manages composition and undo/redo.

This is a new local application prototype with original synthetic examples and no claimed user base. It shares a small original local-workspace foundation with other personal utility projects; its domain model and workflows are specific to this application. No external service, account or telemetry is required.

## Implemented baseline

Text/rectangle/ellipse layers; explicit text line breaks and clipping; layer order; position locks; pointer/keyboard moves; zoom; SVG export; JSON interchange; local revision storage; undo/redo.

## Run

Python 3.11+ is required; there are no Python runtime dependencies.

```sh
python3 server.py
# Open http://127.0.0.1:7433
```

Run from the repository root. `--port` changes the port; `--data PATH` chooses the SQLite library (default `.local-data/library.sqlite3`). Use the printed `127.0.0.1` address: Host, Origin and custom-header checks protect local mutations. This server is intended for local use, not internet hosting. Back up your library before experimenting with it.

## Test

```sh
python3 -m unittest discover -s tests -v
# In a separate terminal, run the server with a disposable --data path.
npm ci
npx playwright install chromium
npm run test:ui
```

Browser tests use Node.js 20+ and pinned Playwright. They create synthetic saved documents. Set `BASE_URL` for a custom test server and `UI_SCREENSHOTS` for screenshots outside application source. Chromium requires its normal OS libraries. No hosted CI or other-browser certification is claimed.

## Project structure

- `core.py`: normalization, constraints and domain analysis.
- `server.py`: loopback HTTP boundary and optimistic SQLite revisions.
- `web/`: interface, DOM/SVG rendering, dialogs and edit history.
- `examples/sample.json`: original fictional fixture.
- `tests/`: core regression cases and browser workflows.

## Scope and limits

This is a single-page SVG composition prototype, not a full typesetting system. Text overflow notices use approximate character widths, not font shaping. There is no rich text, image import, automatic wrapping, font embedding, rotation, pagination or PDF export yet. Position locks prevent direct dragging and nudging; the explicit editor can change or unlock an object. Print size requires independent calibration.

Layer text in JSON imports must be a string when supplied. Missing or empty text uses an em dash placeholder; malformed text values reject the import without replacing the current draft.

Documents have at most 150 entries; the library supports 100 documents. Request/import size is bounded to 256 KB. Undo/redo is per-tab memory, not durable history. Export drafts before closing; there is no automatic crash recovery yet. Optimistic revisions reject stale saves, but merging conflicts is future work.

## Planned development

[ROADMAP.md](ROADMAP.md) specifies approximately **74–110 hours** of proposed work with acceptance criteria. [QUALITY-PLAN.md](QUALITY-PLAN.md) describes representative review dimensions and transition cases. Estimates are future engineering effort, not completed hours or promised paid work. [CONTRIBUTING.md](CONTRIBUTING.md) explains contribution conventions.

## License

MIT. See [LICENSE](LICENSE).
