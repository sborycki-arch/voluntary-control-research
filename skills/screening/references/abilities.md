# Abilities in scope (26) with search synonyms and crosswalk to the evidence map

Codes are used in ability_id across all schema files. This table carries no effect values. The pilot values (change, delta, strength_sd, band) live in the research bundle's evidence map (INPUTS/data/evidence.csv) and in the research document's evidence sections; they are rationale only and enter no analysis file (charter SC1). Population baselines used for the z scale live in schema/population_sd.csv (all rows pilot_unverified until re-extracted with provenance).

Crosswalk: `evidence_id` is the `id` column of INPUTS/data/evidence.csv and `key_sources` is its `sources` column, copied verbatim. The 26 abilities were matched to the 26 evidence.csv rows one-to-one by name (the ability names here are paraphrases of the evidence-map `feature` names, e.g. A01 drops "Swami Rama", A03 says "axillary" for "armpit"); evidence.csv carries no A-codes and this file is the only place the mapping is recorded. Key sources are the evidence map's starting references, not the review's search result; the methods paper and the PRISMA flow cite them as the pre-review knowledge base.

| ability_id | Ability | Synonyms for screening | evidence_id | key_sources |
|---|---|---|---|---|
| A01 | Heart-rate surge, direct | voluntary tachycardia, atrial flutter on command, yogic heart control | swami_rama (Heart-rate surge (Swami Rama)) | Green & Green 1977, Beyond Biofeedback (book, not peer-reviewed) |
| A02 | Hand-to-hand skin-temperature split | differential hand temperature, hypnotic temperature control | hand_split (Hand-to-hand temperature split) | Maslach, Marshall & Zimbardo 1972, Psychophysiology (case report; figures from their 1970 ONR report) |
| A03 | Core (axillary) temperature rise | g-Tummo, tummo, inner heat, meditation thermogenesis | core_temp (Core (armpit) temperature rise) | Kozhevnikov et al. 2013, PLoS ONE |
| A04 | Middle-ear muscle (tensor tympani) contraction | ear rumbling, voluntary tensor tympani, low-frequency hearing threshold shift | tensor_tympani (Middle-ear muscle (tensor tympani)) | Wickens et al. 2017 (n = 5, tympanometry); Röddiger et al. 2021; Hoyle et al. 2024 |
| A05 | Heart-rate oscillation via breathing (HRV biofeedback) | resonance breathing, slow-paced breathing, respiratory sinus arrhythmia amplification | hrv (Heart-rate oscillation (HRV) via breathing) | Lehrer & Gevirtz 2014; Goessl et al. 2017 meta |
| A06 | Pupil constriction/dilation, direct | voluntary miosis, voluntary mydriasis, pupil without accommodation | pupil_direct (Pupil constriction, direct) | Eberhardt et al. 2021, Int J Psychophysiol |
| A07 | Finger/toe skin warming | peripheral vasodilation, thermal biofeedback, hand warming | finger_temp (Finger/toe warming) | Benson et al. 1982, Nature |
| A08 | Pupil size via biofeedback | pupillometry training, pupil self-regulation | pupil_biofeedback (Pupil size via biofeedback) | Meissner et al. 2024, Nat Hum Behav (randomized 56 + 25) |
| A09 | Inflammatory response via breathing | endotoxin challenge, cytokine, Wim Hof, cyclic hyperventilation (main-session extraction only) | inflammation (Inflammatory response via breathing) | Kox et al. 2014, PNAS; Zwaag et al. 2022 |
| A10 | Pain relief by meditation | mindfulness analgesia, focused attention, pain unpleasantness | meditation_pain (Pain relief by meditation) | Zeidan et al. 2011, 2015, 2016 |
| A11 | Seizure frequency via skin-conductance feedback | GSR biofeedback epilepsy, electrodermal biofeedback | seizures (Seizure frequency via skin-conductance feedback) | Nagai et al. 2004, 2018; Nagai 2019 meta |
| A12 | Strength gain from imagined contractions | motor imagery strength, mental practice, kinesthetic imagery | strength_imagery (Strength from imagined contractions) | Paravlic et al. 2018 meta (ES 0.72); Ranganathan 2004; Clark 2014 |
| A13 | Pain relief by hypnosis | hypnotic analgesia, suggestibility | hypnotic_analgesia (Pain relief by hypnosis) | Montgomery et al. 2000 meta (933); Thompson et al. 2019 meta (3,632) |
| A14 | Heart rate, direct raising/lowering | voluntary heart-rate control without biofeedback | heart_rate (Heart rate, direct) | Manuck 1976 (n = 60); Belmaker 1972 |
| A15 | Muscle growth by internal focus | attentional focus hypertrophy, mind-muscle connection | mind_muscle (Muscle growth by internal focus) | Schoenfeld et al. 2018; Calatayud et al. 2016 |
| A16 | Blood pressure via slow breathing | device-guided breathing, RESPeRATE, paced breathing hypertension | blood_pressure (Blood pressure via slow breathing) | AHA statement, Brook et al. 2013 (IIa/B) |
| A17 | Stopping the heart | voluntary cardiac arrest claim, yogic heart stopping | heart_stop (Stopping the heart) | Wenger, Bagchi & Anand 1961, Circulation; Khalsa et al. 2015 review |
| A18 | Single motor units | voluntary motor-unit isolation, SMU control, EMG feedback | motor_unit (Single motor units) | Basmajian 1963, Science; Bräcklein et al. 2022, eLife |
| A19 | Piloerection on cue | voluntary goosebumps, VGP | goosebumps (Goosebumps on cue) | Katahira et al. 2020; Heathers et al. 2018 |
| A20 | Voluntary nystagmus | voluntary eye oscillation, ocular flutter on command | nystagmus (Voluntary nystagmus) | Zahn 1978 |
| A21 | Ear (auricular) muscle movement | ear wiggling, auricular motor control | ear_muscles (Ear muscles) | Code 1995 (n = 442); Strauss et al. 2020 |
| A22 | Single brain neurons (implant) | volitional control of single neurons, intracranial feedback | single_neurons (Single brain neurons (implant)) | Cerf et al. 2010, Nature |
| A23 | EEG rhythm self-regulation | alpha neurofeedback, SMR training, EEG biofeedback | eeg (EEG rhythms) | Kamiya 1968; Sterman & Egner 2006; Cortese 2016; Westwood 2025 |
| A24 | Regional brain activity (fMRI neurofeedback) | real-time fMRI self-regulation | fmri (Regional brain activity (fMRI)) | Thibault et al. 2018; Sulzer et al. 2013 |
| A25 | Pelvic-floor coordination | biofeedback dyssynergia, anorectal biofeedback | pelvic_floor (Pelvic-floor coordination) | Rao et al. 2007; Chiarioni et al. 2006 |
| A26 | Vagal output to the heart | cardiac vagal neurons, slow deep breathing microneurography | vagal (Vagal output to the heart) | Farmer et al. 2025, J Physiol; Macefield et al. 2026 |

Excluded by design as not deliberate: placebo analgesia via endogenous opioids; conditioned immune suppression (evidence.csv carries the same two exclusions).
