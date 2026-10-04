"""Build viz/terrain.html (the 3D evidence map) from data/evidence.json and viz/terrain_template.html.

Usage:  python viz/build_terrain.py
Output: viz/terrain.html  (publishable as a claude.ai artifact; loads Plotly 2.35.2 from cdn.jsdelivr.net)
        viz/terrain_standalone.html  (same page wrapped as a full HTML document for opening in a browser)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

d = json.load(open(os.path.join(ROOT, "data", "evidence.json")))
keep = ["id", "feature", "short", "system", "certainty", "prevalence", "prev_value", "change", "basis", "who",
        "lever", "sources", "note", "cert_level", "prev_level", "strength_sd", "band", "plot_sd", "elev",
        "baseline_text", "pct"]
feats = [{k: f.get(k) for k in keep} for f in d["features"]]
payload = json.dumps({"features": feats, "baselines": d["baselines"], "stats": d["stats"]}, ensure_ascii=False)

tpl = open(os.path.join(HERE, "terrain_template.html"), encoding="utf-8").read()
assert tpl.count("/*DATA*/") == 1, "template must contain exactly one /*DATA*/ marker"
page = tpl.replace("/*DATA*/", payload)
open(os.path.join(HERE, "terrain.html"), "w", encoding="utf-8").write(page)

standalone = ('<!doctype html><html><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>'
              + page + "</body></html>")
open(os.path.join(HERE, "terrain_standalone.html"), "w", encoding="utf-8").write(standalone)
print(f"built terrain.html ({len(page):,} bytes) with {len(feats)} features")
