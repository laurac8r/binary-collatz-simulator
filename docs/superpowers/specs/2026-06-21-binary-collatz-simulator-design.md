# Binary Collatz Simulator — Design

**Date:** 2026-06-21
**Status:** Approved (design gate passed)

## Summary

A terminal (TUI) visualizer of the Collatz conjecture. Given a starting integer
`n`, it generates the hailstone sequence (`n/2` when even, `3n+1` when odd, until
`1`) and animates each number as a row of filled/empty binary cells (`█`/`·`),
place-value aligned so the right-shift of an even step and the leftward growth of
a `3n+1` step are visually obvious. A persistent stats bar and a tabbed view
(binary stream + altitude sparkline) frame the "always reaches 1" story.

Built in Python (3.11+) on the [Textual](https://textual.textualize.io/)
framework, with a strict separation between pure logic and UI.

## Goals

- Make the binary mechanics of Collatz visible and intuitive.
- Auto-play with playback controls (pause, step, speed).
- Keep the math engine pure and fully unit-testable, independent of the UI.
- Stay small — a fun project, not a platform.

## Non-Goals (YAGNI)

- No save/export of sequences.
- No multi-number comparison or batch mode.
- No web / GUI mode, no backend server.
- No config files or persistence.

## Architecture

A `uv`-managed Python package with a clean split between pure logic (engine +
renderer) and the Textual UI. The engine and renderer never import Textual, so
the math and formatting are testable without a terminal.

```
binary-collatz-simulator/
├── pyproject.toml            # uv; deps: textual; dev: pytest, pytest-asyncio
├── src/binary_collatz/
│   ├── __init__.py
│   ├── engine.py             # pure Collatz logic — no I/O, no Textual
│   ├── render.py             # pure string formatting (cells, sparkline, rows)
│   ├── app.py                # Textual App: tabs, timer loop, controls
│   └── __main__.py           # `python -m binary_collatz [N]` entry
└── tests/
    ├── test_engine.py
    └── test_render.py
```

## Components

### `engine.py` (pure)

- `Op` enum:
  - `EVEN` — `n → n // 2` (a binary right-shift / drop trailing zero).
  - `ODD` — `n → 3 * n + 1`.
- `Step` (frozen dataclass):
  - `index: int` — 0-based position in the sequence.
  - `value: int` — the number at this step.
  - `op: Op | None` — the operation that *produced* this value; `None` for the
    starting number (`index == 0`).
  - `bits: str` — binary digits of `value` (no `0b` prefix), e.g. `"11010"`.
- `iterate(n: int) -> Iterator[Step]` — lazy generator yielding each `Step` from
  the start `n` until and including `1`. Laziness matters: the UI pulls exactly
  one step per timer tick. Raises `ValueError` for `n <= 0`.
- `Summary` (frozen dataclass): `total_steps: int` (stopping time), `peak: int`
  (max altitude reached), `peak_step: int`.
- `summarize(n: int) -> Summary` — computes the summary independently of the UI.

Sequence convention: `total_steps` is the number of operations applied to reach
`1`. So `n = 1` → `total_steps == 0`; `n = 6` → `8`; `n = 27` → `111` with
`peak == 9232`.

### `render.py` (pure)

No Textual types — plain strings, so it is unit-testable.

- `cells(value: int, width: int) -> str` — renders `value`'s binary form as
  `█` (1) and `·` (0), **place-value aligned**: the units bit is fixed on the
  right and padded to `width` columns, so wider numbers extend leftward and the
  same column always means the same power of two.
- `sparkline(values: list[int], *, log: bool = True) -> str` — maps values to
  `▁▂▃▄▅▆▇█`. Log-scaled by default so a wide dynamic range (e.g. `1 → 9232`)
  stays legible as the jagged hailstone curve.

### `app.py` (Textual UI)

- **Persistent stats bar** (top, visible on both tabs):
  `start N · step · current · peak (altitude) · stopping time`. The stopping
  time fills in once the sequence lands on `1`.
- **`TabbedContent` with two tabs:**
  - **Binary** — a scrolling log; each row is `cells | decimal | op-label`, with
    `EVEN` (`/2`) and `ODD` (`3n+1`) color-coded. Auto-scrolls to the newest
    row. Rows right-aligned to a running max bit-width; horizontal scroll if a
    sequence becomes very wide.
  - **Curve** — a full-size altitude sparkline (value over time), log-scaled.
- **Footer** — key-binding hints.

### `__main__.py`

`python -m binary_collatz [N]`. With an argument, starts immediately. Without
one, the app prompts for a starting number.

## Data Flow

1. The app holds an `iterate(n)` generator and a growing `value_history` list.
2. A Textual timer (`set_interval`) ticks at the current playback speed.
3. Each tick pulls the next `Step`, appends a rendered row to the Binary log and
   a point to the curve, and refreshes the stats bar.
4. On `StopIteration` (value reached `1`), the timer stops and the stats bar
   shows the final stopping time.
5. Controls mutate the timer interval or pause it; `i`/`r` reset the generator
   and history with a new `n`.

## Controls (key bindings)

- `space` — pause / resume
- `→` — step one (when paused)
- `+` / `-` — faster / slower playback
- `r` — random start
- `i` — enter a new starting number (inline input field)
- `tab` — switch tabs
- `q` — quit

## Edge Cases

- `n = 1` — already landed; show the single row, stopping time `0`.
- `n <= 0` or non-integer input — inline validation error, no crash; engine
  raises `ValueError`, UI surfaces it without terminating.
- Large `n` — Python ints are unbounded. Wide rows handled by horizontal scroll;
  long sequences by the scrollable log; large peaks kept readable by sparkline
  log-scaling.

## Testing

- `test_engine.py` (pytest, parametrized):
  - Known sequences: `27` → 111 steps & peak 9232; `6` → 8 steps; `1` → 0 steps;
    powers of two → straight descent to 1.
  - `iterate`/`summarize` raise `ValueError` on `n <= 0`.
  - `Step.op` is `None` only at `index == 0`; matches parity thereafter.
- `test_render.py`:
  - `cells()` output and alignment width for known values (e.g. `26` →
    `"██·█·"` at its natural width; padded correctly at a larger width).
  - `sparkline()` mapping is monotonic and length-correct; log vs linear scaling
    behave as specified.
- UI: one lightweight smoke test via Textual's `run_test()` Pilot harness — the
  app mounts, ticks a few steps, and lands on `1`. Heavy snapshot testing is out
  of scope.

Tooling: `uv run ruff check`, `uv run ruff format`, `uv run pytest` (88-char
line limit, full type hints).