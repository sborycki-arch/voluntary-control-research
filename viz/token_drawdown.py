"""Cumulative effective-token drawdown for this session, stacked by source.

Effective tokens = input + 0.1*cache_read + 2*cache_write + 5*output.
Times shown in America/Regina (UTC-6).
"""
import json, glob, os, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

BASE = "/root/.claude/projects/-home-claude/ce0e7ea5-b8e0-5790-b959-8fc28808af3a"
TZ = dt.timezone(dt.timedelta(hours=-6))

SOURCES = [  # bottom -> top, fixed categorical order (validated)
    ("Main conversation",                 BASE + ".jsonl",                                  "#2a78d6"),
    ("Research agent: heart, temperature", BASE + "/subagents/agent-af76efc9602c9c8f4.jsonl", "#eb6834"),
    ("Research agent: muscles, eyes, ears", BASE + "/subagents/agent-ad975515ac1a22b9b.jsonl", "#1baf7a"),
    ("Research agent: brain, pain",       BASE + "/subagents/agent-a4590e4ae1cf8967e.jsonl", "#eda100"),
    ("Head agent",                        BASE + "/subagents/agent-a4b2b87fc9df0a35f.jsonl", "#e87ba4"),
]

def requests(path):
    seen = {}
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") != "assistant":
                continue
            m = d.get("message", {})
            u = m.get("usage")
            if not u:
                continue
            seen[d.get("requestId") or m.get("id")] = (d["timestamp"], u)
    out = []
    for ts, u in seen.values():
        t = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)
        e = (u.get("input_tokens", 0) + 0.1 * u.get("cache_read_input_tokens", 0)
             + 2 * u.get("cache_creation_input_tokens", 0) + 5 * u.get("output_tokens", 0))
        out.append((t, e))
    return sorted(out)

data = {name: requests(p) for name, p, _ in SOURCES}
t0 = min(r[0][0] for r in data.values() if r).replace(second=0, microsecond=0)
t1 = max(r[-1][0] for r in data.values() if r)
grid = []
t = t0
while t <= t1 + dt.timedelta(minutes=1):
    grid.append(t)
    t += dt.timedelta(seconds=20)

def cumulative(reqs):
    vals, i, acc = [], 0, 0.0
    for g in grid:
        while i < len(reqs) and reqs[i][0] <= g:
            acc += reqs[i][1]
            i += 1
        vals.append(acc)
    return vals

cums = [cumulative(data[name]) for name, _, _ in SOURCES]
totals = {name: sum(e for _, e in data[name]) for name, _, _ in SOURCES}
grand = sum(totals.values())

# ---- chart ----
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
plt.rcParams.update({"font.family": "Inter", "font.size": 10.5})
fig, ax = plt.subplots(figsize=(11, 5.6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

lower = [0.0] * len(grid)
for (name, _, color), cum in zip(SOURCES, cums):
    upper = [a + b for a, b in zip(lower, cum)]
    ax.fill_between(grid, lower, upper, color=color, alpha=0.16, linewidth=0, step="post")
    ax.step(grid, upper, where="post", color=color, linewidth=2, solid_joinstyle="round",
            label=f"{name}  ({totals[name]/1e6:.1f}M)")
    lower = upper

ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "0" if v == 0 else f"{v/1e6:.0f}M"))
ax.set_ylim(0, 12e6)
ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30], tz=TZ))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=TZ))
ax.set_xlim(grid[0], grid[-1] + dt.timedelta(minutes=14))
ax.grid(axis="y", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(AXIS)
ax.tick_params(colors=MUTED, length=0, labelsize=9.5)
ax.set_xlabel("Local time, Oct 3 (Saskatchewan, UTC−6)", color=MUTED, fontsize=9.5, labelpad=8)

# Selective annotations (text tokens only)
end_total = lower[-1]
ax.annotate(f"{grand/1e6:.1f}M total", xy=(grid[-1], end_total), xytext=(8, 0),
            textcoords="offset points", va="center", color=INK, fontsize=10.5, fontweight="semibold")
ax.text(dt.datetime(2026, 10, 3, 18, 8, tzinfo=TZ), 6.35e6, "Idle 17:00–19:20: nothing used",
        color=INK2, fontsize=9.5, ha="center")
ax.annotate("Resume after the break:\nwhole conversation reloaded (0.5M)",
            xy=(dt.datetime(2026, 10, 3, 19, 21, 13, tzinfo=TZ), 1.68e6),
            xytext=(dt.datetime(2026, 10, 3, 18, 40, tzinfo=TZ), 2.45e6),
            textcoords="data", color=INK2, fontsize=9.2, ha="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
ax.annotate("3 research agents\nlaunched 16:28", xy=(dt.datetime(2026, 10, 3, 16, 28, 20, tzinfo=TZ), 1.2e6),
            xytext=(dt.datetime(2026, 10, 3, 16, 13, tzinfo=TZ), 2.9e6), textcoords="data",
            color=INK2, fontsize=9.2, ha="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))

fig.text(0.065, 0.955, "Token drawdown this session", color=INK, fontsize=15, fontweight="semibold")
fig.text(0.065, 0.912, "Cumulative effective tokens by source  ·  cache reads ×0.1, cache writes ×2, output ×5  ·  through 19:43",
         color=INK2, fontsize=9.8)
leg = ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.99), frameon=False, fontsize=9.4,
                labelcolor=INK, handlelength=1.6)
fig.subplots_adjust(left=0.065, right=0.9, top=0.86, bottom=0.12)
out = "/mnt/user-data/outputs/token_drawdown.png"
fig.savefig(out, facecolor=SURFACE)
print(out)
for name, _, _ in SOURCES:
    print(f"{name}: {totals[name]:,.0f}")
print(f"TOTAL: {grand:,.0f}")
