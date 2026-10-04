"""Reconciled evidence dataset: voluntary control of body features.

strength_sd = |delta| / population SD (or a reported standardized effect size).
Elevation for the map = log2(1 + strength_sd).
"""
import json, math
from scipy.stats import spearmanr

CERT = {"Not supported": 0, "Low": 1, "Moderate": 2, "High": 3}
PREV = {"None": 0, "Single cases": 1, "Adepts": 2, "Rare": 3, "Minority": 4, "Most with training": 5}
BAND_MID = {"Small": 0.25, "Moderate": 0.75, "Large": math.sqrt(3), "Extreme": 3.0}  # percent-only placement

def band_from_sd(z):
    if z is None: return None
    if z == 0: return "None"
    if z < 0.5: return "Small"
    if z < 1: return "Moderate"
    if z <= 3: return "Large"
    return "Extreme"

B = {  # baselines (healthy adults at rest)
    "rhr":  dict(mean=65.5, sd=7.7, unit="bpm", src="Quer et al. 2020, PLoS ONE (n = 92,457)"),
    "sbp":  dict(mean=122, sd=17, unit="mmHg", src="NHANES 2001–08 (Wright et al. 2011, NHSR 35); SD derived from 5th–95th and IQR percentiles"),
    "axil": dict(mean=35.97, sd=0.48, unit="°C", src="Geneva et al. 2019, Open Forum Infect Dis (axillary)"),
    "asym": dict(mean=0.31, sd=0.25, unit="°C", src="Uematsu et al. 1988, J Neurosurg (hand, n = 56)"),
    "fing": dict(mean=27.16, sd=3.2, unit="°C", src="Sci Rep 2019 thermography, healthy controls at 23 °C room"),
    "pup":  dict(mean=4.03, sd=0.9, unit="mm", src="Schröder et al. 2018, Eur J Ophthalmol (photopic, n = 91)"),
    "hear": dict(mean=None, sd=5.0, unit="dB", src="Shahnaz & Ciocca 2026, Hear Res (250 Hz, n = 126)"),
}

def comp(delta, key):
    return round(abs(delta) / B[key]["sd"], 4)

D = [
 # ---- computed against a population SD ----
 dict(id="swami_rama", feature="Heart-rate surge (Swami Rama)", short="Swami Rama heart surge", system="Heart",
      certainty="Low", prevalence="Single cases", prev_value=None,
      change="Atrial flutter ~300 bpm for ~17 s", delta=300-65.5, unit="bpm", baseline="rhr",
      basis="computed", who="1 person", lever="Unknown",
      sources="Green & Green 1977, Beyond Biofeedback (book, not peer-reviewed)",
      note="Single demonstration; figures vary between accounts (300 bpm/17 s vs 306 bpm/16.2 s)."),
 dict(id="hand_split", feature="Hand-to-hand temperature split", short="Hand-to-hand temp split", system="Temperature",
      certainty="Low", prevalence="Single cases", prev_value=None,
      change="Up to 4 °C between matching sites on opposite hands within 2 min", delta=4.0-0.31, unit="°C", baseline="asym",
      basis="computed", who="3 hypnotic subjects", lever="Hypnosis",
      sources="Maslach, Marshall & Zimbardo 1972, Psychophysiology (case report; figures from their 1970 ONR report)",
      note="Best result among 3 subjects; 6 waking controls could not do it."),
 dict(id="core_temp", feature="Core (armpit) temperature rise", short="Core temp rise", system="Temperature",
      certainty="Low", prevalence="Adepts", prev_value=None,
      change="+2.2 °C largest individual rise; peak 38.3 °C", delta=2.2, unit="°C", baseline="axil",
      basis="computed", who="10 g-Tummo experts; Westerners partly", lever="Vase breathing + visualization",
      sources="Kozhevnikov et al. 2013, PLoS ONE",
      note="Best individual; group baseline 36.49 °C (SD 0.21)."),
 dict(id="tensor_tympani", feature="Middle-ear muscle (tensor tympani)", short="Middle-ear muscle", system="Ear",
      certainty="High", prevalence="Minority", prev_value=0.432,
      change="Hearing threshold +22 dB at 250 Hz during contraction", delta=22, unit="dB", baseline="hear",
      basis="computed", who="43% self-report (CI 36–50%)", lever="Direct",
      sources="Wickens et al. 2017 (n = 5, tympanometry); Röddiger et al. 2021; Hoyle et al. 2024",
      note="Prevalence from self-report; upper bound 55% (Hoyle 2024)."),
 dict(id="pupil_direct", feature="Pupil constriction, direct", short="Pupil, direct", system="Eye",
      certainty="Low", prevalence="Single cases", prev_value=None,
      change="−2.4 mm constriction (+0.8 mm dilation) with no light or focus change", delta=2.4, unit="mm", baseline="pup",
      basis="computed", who="1 documented person", lever="Direct",
      sources="Eberhardt et al. 2021, Int J Psychophysiol",
      note="Subject's baseline 4.96 mm; dilation alone = 0.9 SD."),
 dict(id="finger_temp", feature="Finger/toe warming", short="Finger/toe warming", system="Temperature",
      certainty="Moderate", prevalence="Single cases", prev_value=None,
      change="Up to +8.3 °C", delta=8.3, unit="°C", baseline="fing",
      basis="computed", who="3 monks (best result)", lever="g-Tummo meditation",
      sources="Benson et al. 1982, Nature",
      note="Smaller feedback-trained warming is widely taught; Raynaud's attacks not reduced by it (RTS 2000)."),
 dict(id="heart_rate", feature="Heart rate, direct", short="Heart rate", system="Heart",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="+3.4 bpm up; lowering not achieved", delta=3.4, unit="bpm", baseline="rhr",
      basis="computed", who="Group mean, typical adults", lever="Feedback",
      sources="Manuck 1976 (n = 60); Belmaker 1972",
      note="Hidden muscle tension alone can add >13 bpm."),
 dict(id="blood_pressure", feature="Blood pressure via slow breathing", short="Blood pressure", system="Heart",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="−4 mmHg systolic (device-guided breathing, net of placebo)", delta=4, unit="mmHg", baseline="sbp",
      basis="computed", who="Hypertensive adults", lever="Slow breathing",
      sources="AHA statement, Brook et al. 2013 (IIa/B)",
      note="TM −4.7 mmHg (0.28 SD); biofeedback alone −0.8 (n.s.)."),
 # ---- reported standardized effect sizes ----
 dict(id="pupil_biofeedback", feature="Pupil size via biofeedback", short="Pupil, biofeedback", system="Eye",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="Volitional up/down pupil control after 3 days", effect=2.0,
      basis="reported effect size", who="Trained participants", lever="Imagery / relaxation",
      sources="Meissner et al. 2024, Nat Hum Behav (randomized 56 + 25)",
      note="d ≈ 2.0 converted from ηp² 0.50 (group difference); mm change not reported in main text."),
 dict(id="strength_imagery", feature="Strength from imagined contractions", short="Strength by imagery", system="Muscle",
      certainty="High", prevalence="Most with training", prev_value=None,
      change="+35% finger, +13.5% elbow in 12 wk", effect=0.72,
      basis="reported effect size", who="Healthy adults", lever="Imagined contractions",
      sources="Paravlic et al. 2018 meta (ES 0.72); Ranganathan 2004; Clark 2014",
      note="Physical training does more (ES 0.42 in its favor)."),
 dict(id="hypnotic_analgesia", feature="Pain relief by hypnosis", short="Pain, hypnosis", system="Perception",
      certainty="High", prevalence="Most with training", prev_value=None,
      change="d 0.67 overall; 1.16 high-suggestibility, −0.01 low", effect=0.67,
      basis="reported effect size", who="Scales with suggestibility", lever="Hypnotic suggestion",
      sources="Montgomery et al. 2000 meta (933); Thompson et al. 2019 meta (3,632)",
      note="High suggestibles: pain −42% with direct suggestion (Thompson 2019)."),
 # ---- percent only (placed at band middle on the map) ----
 dict(id="hrv", feature="Heart-rate oscillation (HRV) via breathing", short="HRV oscillation", system="Heart",
      certainty="High", prevalence="Most with training", prev_value=None,
      change="Oscillation grows to many times its resting size", pct=None, pct_band="Extreme",
      basis="percent only", who="Most people", lever="Breathing ~5.5–6/min",
      sources="Lehrer & Gevirtz 2014; Goessl et al. 2017 meta",
      note="Magnitude described, not tabulated; plotted at the Extreme threshold as a lower bound."),
 dict(id="inflammation", feature="Inflammatory response via breathing", short="Inflammatory response", system="Immune",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="IL-6 −35%, TNF-α −32%, IL-10 +44% vs untrained", pct=-35, pct_band="Large",
      basis="percent only", who="Trained volunteers", lever="Hyperventilation + breath-hold",
      sources="Kox et al. 2014, PNAS; Zwaag et al. 2022",
      note="One research group; cytokines vary widely between people, so % may overstate SD units."),
 dict(id="meditation_pain", feature="Pain relief by meditation", short="Pain, meditation", system="Perception",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="Intensity −40%, unpleasantness −57% after 4×20 min", pct=-40, pct_band="Large",
      basis="percent only", who="Novices after 4 sessions", lever="Attention training",
      sources="Zeidan et al. 2011, 2015, 2016",
      note="Larger trial (2015): intensity −27% vs placebo −11%."),
 dict(id="seizures", feature="Seizure frequency via skin-conductance feedback", short="Seizure frequency", system="Brain",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="−43% mean; 45% had >50% fewer", pct=-43, pct_band="Large",
      basis="percent only", who="Drug-resistant epilepsy patients", lever="Skin-conductance feedback",
      sources="Nagai et al. 2004, 2018; Nagai 2019 meta",
      note="Mostly one group; controls rose +31% (usual care, not sham)."),
 dict(id="mind_muscle", feature="Muscle growth by internal focus", short="Muscle focus", system="Muscle",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="Biceps growth 12.4% vs 6.9% (+5.5 points)", pct=5.5, pct_band="Small",
      basis="percent only", who="Lifters", lever="Internal focus",
      sources="Schoenfeld et al. 2018; Calatayud et al. 2016",
      note="EMG gain only at 20–60% of max load."),
 # ---- none ----
 dict(id="heart_stop", feature="Stopping the heart", short="Stopping the heart", system="Heart",
      certainty="Not supported", prevalence="None", prev_value=None,
      change="Heart kept beating; brief slowing at most", effect=0.0,
      basis="none", who="No one shown", lever="Breath-hold under pressure (Valsalva)",
      sources="Wenger, Bagchi & Anand 1961, Circulation; Khalsa et al. 2015 review",
      note="ECG showed reduced QRS amplitude, not arrest."),
 # ---- on/off (z undefined) ----
 dict(id="motor_unit", feature="Single motor units", short="Single motor units", system="Muscle",
      certainty="High", prevalence="Most with training", prev_value=None,
      change="Fire one spinal motor neuron's unit in isolation", basis="on/off", who="Most, with training",
      lever="EMG feedback", sources="Basmajian 1963, Science; Bräcklein et al. 2022, eLife",
      note="Independent control limited by shared input."),
 dict(id="goosebumps", feature="Goosebumps on cue", short="Goosebumps", system="Skin",
      certainty="Moderate", prevalence="Rare", prev_value=0.028,
      change="Piloerection on cue, onset ~4 s", basis="on/off", who="~2.8%",
      lever="Head/neck tension", sources="Katahira et al. 2020; Heathers et al. 2018",
      note="Objective in 9 of 15."),
 dict(id="nystagmus", feature="Voluntary nystagmus", short="Voluntary nystagmus", system="Eye",
      certainty="High", prevalence="Minority", prev_value=0.08,
      change="22–30 Hz eye oscillation for 4–35 s", basis="on/off", who="~8%, familial",
      lever="Direct, often via convergence", sources="Zahn 1978", note="79% had relatives who could."),
 dict(id="ear_muscles", feature="Ear muscles", short="Ear wiggling", system="Ear",
      certainty="High", prevalence="Minority", prev_value=0.22,
      change="Move one ear (22%) or both (18%)", basis="on/off", who="~1 in 5",
      lever="Direct", sources="Code 1995 (n = 442); Strauss et al. 2020", note="Vestigial muscles."),
 # ---- not quantified ----
 dict(id="single_neurons", feature="Single brain neurons (implant)", short="Single neurons", system="Brain",
      certainty="High", prevalence="Most with training", prev_value=None,
      change="Raise or lower individual neurons' firing", basis="not quantified", who="Implant patients",
      lever="Implant + live feedback", sources="Cerf et al. 2010, Nature", note="Success rate not in abstract."),
 dict(id="eeg", feature="EEG rhythms", short="EEG rhythms", system="Brain",
      certainty="High", prevalence="Most with training", prev_value=None,
      change="Self-regulate alpha / SMR", basis="not quantified", who="Most; 15–50% don't learn",
      lever="Neurofeedback", sources="Kamiya 1968; Sterman & Egner 2006; Cortese 2016; Westwood 2025",
      note="ADHD benefit vanishes with blinded raters (SMD 0.04)."),
 dict(id="fmri", feature="Regional brain activity (fMRI)", short="Brain region (fMRI)", system="Brain",
      certainty="Moderate", prevalence="Most with training", prev_value=None,
      change="Self-regulate a target region; behavior effects rarely replicate", basis="not quantified",
      who="Many, not all", lever="Neurofeedback", sources="Thibault et al. 2018; Sulzer et al. 2013",
      note="deCharms 2005 pain effect matched by sham."),
 dict(id="pelvic_floor", feature="Pelvic-floor coordination", short="Pelvic floor", system="Muscle",
      certainty="High", prevalence="Most with training", prev_value=0.79,
      change="Dyssynergia corrected in 79% vs 4% sham", basis="not quantified", who="79% of patients",
      lever="Biofeedback", sources="Rao et al. 2007; Chiarioni et al. 2006", note="Binary outcome."),
 dict(id="vagal", feature="Vagal output to the heart", short="Vagal output", system="Heart",
      certainty="Low", prevalence="Most with training", prev_value=None,
      change="7 cardiac neurons recruited by slow deep breathing; conflicting result", basis="not quantified",
      who="Anyone breathing slowly (unconfirmed)", lever="Breathing",
      sources="Farmer et al. 2025, J Physiol; Macefield et al. 2026", note="One study, 7 units."),
]

for d in D:
    d["cert_level"] = CERT[d["certainty"]]
    d["prev_level"] = PREV[d["prevalence"]]
    if d["basis"] == "computed":
        b = B[d["baseline"]]
        d["strength_sd"] = comp(d["delta"], d["baseline"])
        d["baseline_text"] = f"SD {b['sd']} {b['unit']} — {b['src']}"
        d["band"] = band_from_sd(d["strength_sd"])
        d["plot_sd"] = d["strength_sd"]
    elif d["basis"] in ("reported effect size", "none"):
        d["strength_sd"] = d["effect"]
        d["baseline_text"] = "Standardized effect size from the source" if d["basis"] != "none" else "—"
        d["band"] = band_from_sd(d["strength_sd"])
        d["plot_sd"] = d["strength_sd"]
    elif d["basis"] == "percent only":
        d["strength_sd"] = None
        d["band"] = d["pct_band"]
        d["plot_sd"] = BAND_MID[d["pct_band"]]
        d["baseline_text"] = "Percent change only; placed at band middle" if d["id"] != "hrv" else "Described as many-fold; plotted at the Extreme threshold"
    else:
        d["strength_sd"] = None
        d["band"] = "On/off" if d["basis"] == "on/off" else None
        d["plot_sd"] = None
        d["baseline_text"] = "No SD at rest (full activation)" if d["basis"] == "on/off" else "Magnitude not reported"
    d["elev"] = None if d["plot_sd"] is None else round(math.log2(1 + d["plot_sd"]), 3)

# Spearman: demonstrated effects with SD-based or effect-size strength (exclude percent-only, none, on/off, n/q)
num = [d for d in D if d["basis"] in ("computed", "reported effect size")]
rho_c, p_c = spearmanr([d["cert_level"] for d in num], [d["strength_sd"] for d in num])
rho_p, p_p = spearmanr([d["prev_level"] for d in num], [d["strength_sd"] for d in num])
stats = dict(n=len(num), rho_certainty=round(rho_c, 2), p_certainty=round(p_c, 3),
             rho_prevalence=round(rho_p, 2), p_prevalence=round(p_p, 3))
print(json.dumps(stats))
import os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "evidence.json")
json.dump(dict(features=D, baselines=B, stats=stats), open(OUT, "w"), ensure_ascii=False, indent=1)

order = {"computed": 0, "reported effect size": 0, "percent only": 0, "none": 0, "on/off": 1, "not quantified": 2}
rows = sorted(D, key=lambda d: (order[d["basis"]], -(d["plot_sd"] if d["plot_sd"] is not None else -1)))
for d in rows:
    s = f"{d['strength_sd']:.2f}" if d["strength_sd"] is not None else ("% only" if d["basis"] == "percent only" else d["basis"])
    print(f"{d['short']:<28} {s:>14} {str(d['band']):<9} {d['certainty']:<13} {d['prevalence']:<18} plot={d['plot_sd']} elev={d['elev']}")
