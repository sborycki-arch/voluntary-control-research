# Voluntary Body Control Research Project

Oct 3, 2026 · @Sean Borycki

## Summary

People can deliberately change at least 20 features of their own bodies that textbooks treat as involuntary, but the biggest changes on record come from the fewest people and the weakest evidence. This project documents that evidence base with primary citations, puts every effect on one scale (standard deviations from the healthy-adult mean), and sets out a two-phase study to turn the finding into a publishable paper.

The review catalogued 26 abilities. Ten reach High certainty (objectively measured, independently replicated, mechanism known). Across the 11 abilities with a computable effect size, strength correlates negatively with certainty (Spearman ρ = −0.60, p ≈ 0.05) and with how many people can do it (ρ = −0.81, p = 0.002). Every High-certainty ability works through a lever: feedback, breathing, skeletal-muscle tension, imagery or suggestion. The one Extreme response that is also High certainty and common is voluntary contraction of the tensor tympani muscle of the middle ear, which about 43% of people report and which raises the 250 Hz hearing threshold by 22 dB. No documented case exists of one mind reaching another person's nerves without hardware.

The proposed study has two phases. Phase 1 is a registered systematic review that formalises the three-axis framework (certainty × strength × prevalence) under PRISMA 2020. Phase 2 is a primary study of lever-free voluntary control of involuntary effectors (tensor tympani, piloerection, pupil, voluntary nystagmus): a topic-blind population survey (target n = 2,000) followed by objective laboratory verification, familial aggregation, and co-occurrence analysis. Section 12 gives the protocol.

## Background and rationale

The research question is which features of their own bodies people can change on purpose, how large those changes are against normal between-person variation, and how strong the evidence is. The autonomic nervous system and the innate immune system are still described in the primary literature as "systems that cannot be voluntarily influenced" \[1\], yet controlled studies now document deliberate changes in adrenaline release, cytokine response, skin and core temperature, pupil size, pain perception, single motor units and single cortical neurons. The question began as whether any individual has been documented inducing a direct mind-to-nerve connection; the answer required a full survey.

**Scope.** An ability is included when a person initiates the change in their own body and the change was measured objectively or by a validated rating. Indirect levers count (paced breathing, skeletal-muscle tension, imagery, hypnotic suggestion, instrument feedback), because the lever is itself part of the finding. Three things are excluded from scoring and handled descriptively: effects the person does not initiate (placebo analgesia given by others, classically conditioned immune responses); links that run through implanted or external hardware to a machine or another person; and clinical benefit as such, since the certainty rating asks only whether the control exists.

**Why it is publishable.** No existing review places these abilities on one scale. Reviews exist per modality: HRV biofeedback \[26\], EEG neurofeedback \[57, 61, 62\], real-time fMRI neurofeedback \[68, 69\], hypnotic analgesia \[70, 71\], motor imagery \[49\]. Putting them on a common scale produces a result none of them can: response strength falls as evidence quality and prevalence rise. That inverse pattern, the lever versus lever-free distinction, and the single well-evidenced exception (the tensor tympani) each generate a testable hypothesis. The subject also sits at the centre of current public interest in breathwork, cold exposure and biofeedback, where the strongest claims rest on the thinnest evidence.

**Conventions.** Certainty, strength and prevalence are rated with the rubrics in the next section. Numbers in this document were read in the cited source unless the Verification section marks them otherwise. Reference numbers in brackets point to the list at the end.

## Rating rubrics and computation

Every ability carries three ratings, defined here before use so the scores can be audited.

**Certainty** rates whether the control exists, not whether it is clinically useful.

- High: objectively measured; replicated by independent groups or a meta-analysis; mechanism understood.
- Moderate: objectively measured in controlled studies, but small samples or mostly one research group.
- Low: one study, a handful of subjects, or not peer-reviewed.
- Not supported: tested and not shown.

**Strength versus the mean** is the demonstrated change divided by the between-person standard deviation of that variable in healthy adults at rest:

```latex
z = \frac{\lvert \Delta \rvert}{SD_{\text{population}}}
```

Where a source reports a standardized effect size (Cohen's d, Hedges' g, SMD), that value replaces z. A partial eta-squared is converted with d = 2·√(ηp² / (1 − ηp²)), so ηp² = 0.50 gives d = 2.0. Bands: None (no change shown); Small (< 0.5); Moderate (0.5 to 1); Large (1 to 3); Extreme (> 3). When neither an SD nor an effect size is obtainable, the percent change is banded instead (Small < 10%, Moderate 10 to 30%, Large 30 to 60%, Extreme > 60%) and marked "percent only". On/off means an effector that is silent at rest switches on, so z is undefined. Not quantified means the control was shown but its size was not reported. The map draws elevation as log2(1 + z).

**Prevalence** records who has been shown to do it: None; Single cases (3 or fewer documented people); Adepts (a small expert group, rate not measured); Rare (under 5%, measured); Minority (5 to 50%, measured); Most with training (group studies in which trained participants as a group achieve it).

**Population baselines.** The SDs below are between-person values in healthy adults; each strength score divides by one of them.

| Variable | Mean ± SD | Source and sample |
| --- | --- | --- |
| Resting heart rate | 65.5 ± 7.7 bpm | Quer et al. 2020 \[86\]; 92,457 adults, wearable, all monitored days |
| Systolic blood pressure | 122 mmHg; SD ≈ 17 (derived: 15.6 from the interquartile range 110 to 131, 17.9 from the 5th to 95th percentile span 98 to 157) | Wright et al. 2011 \[87\]; NHANES 2001 to 2008, adults 18+ |
| Axillary (core) temperature | 35.97 ± 0.48 °C | Geneva et al. 2019 \[88\]; 551 measurements, 5 studies |
| Left to right hand skin-temperature difference | 0.31 ± 0.25 °C | Uematsu et al. 1988 \[89\]; n = 56, hand dorsum |
| Fingertip skin temperature at 23 °C room | 27.16 ± 3.2 °C | Gatt et al. 2019 \[90\]; 51 healthy controls, 510 finger readings |
| Pupil diameter, photopic (16 lux) | 4.03 ± 0.9 mm | Schröder et al. 2018 \[91\]; 91 normal eyes |
| Hearing threshold at 250 Hz | SD ≈ 5 dB (model estimate about 4 dB) | Shahnaz & Ciocca 2026 \[92\]; 126 young adults with typical hearing |

Two studies report their own baselines, which the notes carry: Kozhevnikov's practitioners started at 36.49 °C (SD 0.21) \[4\], and Eberhardt's subject had a 4.96 mm pupil at trial onset \[39\]. Scores use the population SD throughout so that abilities stay comparable; dividing the 2.2 °C core rise by the within-study SD would give 10.5 instead of 4.6.

**Correlation.** Spearman's ρ is computed over the 11 abilities whose strength is a computed z or a reported effect size; percent-only, on/off, not-quantified and not-supported rows are excluded because they have no comparable magnitude. Certainty is coded 0 to 3 and prevalence 0 to 5 in the orders listed above.

## Evidence: cardiovascular and autonomic

Deliberate heart-rate control without a breathing or muscle lever is small (+3.4 bpm); with a breathing lever, heart-rate oscillation and blood pressure change reliably; no one has stopped their heart.

**Heart rate, direct control.** Manuck (1976) \[17\] tested 60 subjects, 15 per condition (no controls; paced breathing; chin-EMG feedback; both), each doing 10 increase and 10 decrease trials of 60 s. Subjects produced significant increases (mean +3.4 bpm) but no decreases (−0.3 bpm), and the size did not differ with somatic restraint. Belmaker, Proctor and Feather (1972) \[18\], n = 11, showed hidden muscle tension alone raised heart rate by more than 13 bpm, and that muscle mediation "cannot be ruled out by absence of change in respiratory pattern or electromyogram". The classic operant demonstrations are Engel and Hansen (1966) \[19\] for slowing, Engel and Chism (1967) \[20\] for speeding, and Brener and Hothersall (1966) \[21\] with augmented feedback; their bpm figures were not read. Rating: Moderate certainty; 0.44 SD (3.4 / 7.7), Small; Most with training.

**Heart-rate oscillation through resonance breathing.** Lehrer and Gevirtz (2014) \[27\] describe the largest heart-rate oscillations at about 0.1 Hz (6 breaths/min), later refined to about 0.09 Hz (5.5 breaths/min), with heart rate and blood pressure oscillating 180° out of phase and the amplitude growing "to many times the amplitude at rest". Lin, Tai and Fan (2014) \[93\] found 5.5 breaths/min with a 5:5 inhale-to-exhale ratio produced higher SDNN and low-frequency power than other patterns (values not read). Clinical meta-analyses: Goessl, Curtiss and Hofmann (2017) \[26\], 24 studies and 484 participants, within-group Hedges' g 0.81 and between-group g 0.83 for stress and anxiety; Lehrer et al. (2020) \[28\], 58 studies, effects larger against inactive than active controls but significant for both; Pizzoli et al. (2021) \[29\], 14 RCTs and 794 participants, depressive symptoms g 0.38 \[0.16, 0.60\]. Rating: High certainty; magnitude described as many-fold but not tabulated (percent only, Extreme); Most with training.

**Blood pressure.** The American Heart Association statement by Brook et al. (2013) \[30\] grades the approaches: device-guided slow breathing Class IIa, Level B, "on the order of 4/3 mm Hg, accounting for the placebo effect"; Transcendental Meditation IIb/B, −4.7/−3.2 mm Hg; biofeedback IIb/B, −0.8/−2.0 mm Hg and not significant across 6 trials with 141 people; other meditation III/C; yoga III/C; relaxation III/B; acupuncture III/B; aerobic exercise I/A. Rating: Moderate certainty; 0.24 SD (4 / 17) for guided breathing and 0.28 SD for TM, Small; Most with training, in hypertensive adults.

**Vagal output to the heart.** Farmer et al. (2025) \[83\] recorded single axons in the cervical vagus of 15 people and found seven cardiac-rhythmic units "recruited or enhanced by slow, deep breathing", with firing characteristic of cardioinhibitory efferents; the efferent identity is inferred from the pattern, and the design does not separate a voluntary command from breathing-driven reflexes. Macefield et al. (2026) \[84\], n = 20, recorded during maximal breath-holds; the research pass reported cardiac modulation unchanged during slow breathing, which the Verification section flags for re-reading. Rating: Low certainty; not quantified; prevalence unmeasured.

**Stopping the heart.** Wenger, Bagchi and Anand (1961) \[22\] tested yogis in India who claimed to stop the heart. The ECG showed a lower QRS amplitude "associated with maintained inspiration and signs of raised intra thoracic pressure" (as quoted by Raghavendra et al. 2013 \[24\]); the heart did not stop. Khalsa et al. (2015) \[23\] summarise: "At best, some individuals were able to exert transient bradycardia … by engaging in combinations of posture manipulation, muscular contraction and breath holding (including the Valsalva maneuver)". The primary paper could not be opened (publisher returned 403); both quotations are from peer-reviewed secondary sources. Rating: Not supported; None.

**The Swami Rama episode.** Green and Green (1977) \[25\] report, in a book rather than a journal, that at the Menninger Foundation around 1970 Swami Rama's heart "had begun beating at five times its normal rate", identified as atrial flutter on an EKG read by Dr Marvin Dunne of Kansas University Medical Center. Secondary accounts give 300 bpm for 17 s or 306 bpm for 16.2 s; no peer-reviewed report was found. Rating: Low certainty; 30.5 SD ((300 − 65.5) / 7.7), Extreme; Single case. The score divides a rhythm disturbance by the SD of resting sinus rate, so it overstates "control"; it is kept because it shows how a single outlier dominates the ranking.

## Evidence: temperature and immune

Trained practitioners raise finger temperature by up to 8.3 °C and core temperature by up to 2.2 °C, and a breathing exercise cuts the cytokine response to injected endotoxin by about a third; all of it runs through breathing, visualisation or feedback, and almost all of it comes from a few people or one research group.

**Finger and toe warming (g-Tummo).** Benson et al. (1982) \[3\] studied three practitioners of g-Tummo yoga in Upper Dharamsala in February 1981, with the Dalai Lama's assistance, and recorded finger and toe temperature rises "by as much as 8.3 °C". Rating: Moderate certainty; 2.59 SD (8.3 / 3.2), Large; Single cases (best of three).

**Core temperature (g-Tummo).** Kozhevnikov et al. (2013) \[4\] measured ten expert meditators (7 women, ages 25 to 52) with axillary and finger disk thermometers. Initial core temperature averaged 36.49 °C (SD 0.21); the largest rise to the end of forceful breathing was 2.2 °C (participant 3) and the highest value 38.30 °C (participant 5). Two components were separated: "vase breathing" (forceful breath retention) produced the heat, and concentrative visualisation of flames along the spine sustained it. Western participants raised core temperature with the breathing alone, within narrower limits. Rating: Low certainty; 4.58 SD (2.2 / 0.48), Extreme; Adepts.

**Hand-to-hand temperature split (hypnosis).** Maslach, Marshall and Zimbardo (1972) \[31\] report three trained hypnotic subjects (one the senior author) and six waking controls. Differences "as much as 4 °C" between identical sites on opposite hands appeared within two minutes; the largest decrease was 7 °C and the largest increase 2 °C; no control achieved divergent changes. The figures were read in the authors' 1970 ONR technical report (DTIC AD0716481), not the journal article. Rating: Low certainty; 14.76 SD ((4.0 − 0.31) / 0.25), Extreme; Single cases.

**Thermal biofeedback in clinical use.** The US Headache Consortium guideline (Campbell, Penzien and Wall 2000 \[32\]), as quoted by Andrasik (2010) \[33\], gives Grade A evidence for "thermal biofeedback combined with relaxation training" in migraine prevention; the grade does not cover thermal biofeedback alone, and Ha and Gonzalez (2019) \[97\] rate the same recommendation SORT B. The Raynaud's Treatment Study (2000) \[34\], an RCT of 313 patients with about one year of follow-up, found a 32% reduction in verified attacks with temperature biofeedback that was not significant against EMG-biofeedback control (P = .37), while sustained-release nifedipine cut attacks 66% versus placebo (P < .001); the drug arms were double-masked, the biofeedback arms were not. This is why peripheral warming is rated Moderate rather than High: the ability is real, the clinical effect inconsistent.

**Adrenaline and the innate immune response (breathing exercise).** Kox et al. (2012) \[2\] injected one practitioner (Wim Hof) with endotoxin while he used his technique; his cortisol rise was more pronounced and his inflammatory mediators much lower than other volunteers', with hardly any flu-like symptoms, and the authors state that results from one person cannot serve as evidence. Kox et al. (2014) \[1\] then randomised 24 healthy men to 10 days of training (third-eye meditation, cyclic hyperventilation with breath retention, ice-water immersion) or no training, followed by 2 ng/kg E. coli endotoxin. Practising the techniques produced intermittent respiratory alkalosis and hypoxia with "profoundly increased plasma epinephrine levels"; IL-10 rose faster and higher and correlated with preceding epinephrine; TNF-α, IL-6 and IL-8 were lower; flu-like symptoms were fewer. Zwaag et al. (2022) \[38\] separated the components in 48 men, 12 per arm: cold training alone did not change the response (F(8,37) = 0.60, p = .77); the breathing exercise did (F(8,37) = 3.80, p = .002); cold training amplified the breathing effect (F(8,37) = 2.57, p = .02). Combined training versus control: IL-10 +44%, TNF-α −32%, IL-6 −35%; breathing alone: IL-6 −34%. Rating: Moderate certainty (one research group); percent only, Large; Most with training.

**Mechanism note.** The lever is hyperventilation. The alkalosis and hypoxia drive the adrenaline surge, and adrenaline suppresses the innate response; the training teaches a respiratory manoeuvre, not direct command of the sympathetic chain.

## Evidence: muscle, eye, ear and skin

This is where the best-evidenced control lives: single motor units with feedback, strength gains from imagined contractions, and three effectors that a measurable minority can switch on with no lever at all (middle-ear muscle, voluntary nystagmus, ear muscles).

**Single motor units.** Basmajian (1963) \[6\] showed that with audio and visual EMG feedback, subjects learned to fire a single spinal motor unit in isolation and to control its firing pattern. Bräcklein et al. (2022) \[7\] found that independent control of two units in isometric tasks is constrained by a common synaptic input. Rating: High certainty; on/off; Most with training.

**Strength from imagined contractions.** Ranganathan et al. (2004) \[9\] trained 30 volunteers for 12 weeks (15 min/day, 5 days/week): mental contractions raised little-finger abduction strength 35% (n = 8, P < 0.005) and elbow-flexion strength 13.5% (n = 8, P < 0.001); physical training raised finger strength 53% (n = 6); controls did not change. Clark et al. (2014) \[10\] immobilised the wrist and hand for 4 weeks: strength fell 45.1 ± 5.0% in controls and 23.8 ± 5.6% in the group doing mental imagery of strong contractions 5 days/week. Paravlic et al. (2018) \[49\] pooled 13 studies and 370 participants: motor imagery versus no exercise ES 0.72 \[0.42, 1.02\]; physical practice versus control ES 1.05; physical practice beat imagery by ES 0.42 across 8 studies. Rating: High certainty; 0.72 (reported effect size), Moderate; Most with training.

**Attentional focus during lifting.** Calatayud et al. (2016) \[50\], 18 trained men on bench press: focusing on the pectoralis or triceps raised its normalised EMG at 20 to 60% of 1RM but not at 80% (Table 2 increases of roughly +4 to +11 units, read from a secondary copy). Schoenfeld et al. (2018) \[51\] randomised 30 untrained men to internal or external focus for 8 weeks: elbow-flexor thickness grew 12.4% versus 6.9%; quadriceps changes were similar between groups. Rating: Moderate certainty; +5.5 percentage points, percent only, Small; Most with training.

**Pelvic-floor coordination.** Rao et al. (2007) \[54\] randomised 77 patients with dyssynergic defecation to biofeedback (28), sham feedback (25) or standard therapy (24): dyssynergia was corrected in 79% with biofeedback versus 8.3% standard and 4% sham (P < .0001), percentages as tabulated in Rao and Patcharatrakul (2016) \[55\]. Chiarioni et al. (2006) \[56\]: major improvement at 6 months in 43 of 54 (80%) biofeedback patients versus 12 of 55 (22%) on laxatives (P < .001), sustained to 24 months. Rating: High certainty; binary outcome, not quantified as SD; 79% of patients.

**Pupil, direct.** Eberhardt et al. (2021) \[39\] studied one 23-year-old man with pupillometry, optometry, skin conductance, visual acuity and 3 T fMRI. From a 4.96 mm baseline he constricted his pupil by about 2.4 mm and dilated it by about 0.8 mm; the tests excluded accommodation, brightness and effort as the route ("even at maximal accommodation, the case voluntarily constricted his pupil without changing vergence"); fMRI showed left dorsolateral prefrontal, premotor and supplementary motor activation. Rating: Low certainty; 2.67 SD (2.4 / 0.9), Large; Single case.

**Pupil, via biofeedback.** Meissner et al. (2024) \[40\] randomised 28 to pupil biofeedback and 28 to control (27/27 analysed), replicated in 25 more, with fMRI in 25. Three days of 15-s up/down trials using emotional imagery to dilate and relaxation to constrict gave "volitional control of pupil size" (group effect F(1, 21.58) = 21.49, P = 0.001, ηp² = 0.50 \[0.17, 0.67\]) and modulated locus coeruleus BOLD and heart rate. Laeng and Sulutvedt (2014) \[41\] had earlier shown pupils follow imagined light while "participants were unable to voluntarily constrict their eyes' pupils". Rating: Moderate certainty; d ≈ 2.0 converted from ηp², Large; Most with training.

**Middle-ear muscle (tensor tympani).** Wickens, Floyd and Bance (2017) \[44\] confirmed contraction in 5 people by tympanometry; at 250 Hz, air-conduction thresholds rose 22 dB and bone-conduction thresholds 10 dB. Angeli et al. (2013) \[45\] report a single case with low-frequency conductive loss and raised middle-ear impedance. Prevalence: Röddiger et al. (2021) \[42\] surveyed 192 people recruited without revealing the topic; 83 (43.2%, 95% CI 36.2 to 50.2%) could produce the rumble, and all 16 lab participants were confirmed by otoscope. Hoyle et al. (2024) \[43\], in a self-selected sample of 1,853, found 85% self-reported the ability and 65% could do it in isolation (upper bound 55% overall; 38% in a neurological sample of 170; 20% of 95 people with motor neurone disease); 80% of 70 volunteers showed visible eardrum movement. Rating: High certainty; 4.4 SD (22 / 5), Extreme; Minority (43%, measured).

**Voluntary nystagmus.** Zahn (1978) \[46\] surveyed a college population: 8% could produce voluntary nystagmus and 79% of those had relatives who could. Characteristics, from Thomas, Dunn and Woodhouse (2022) \[47\] citing Zahn and Neppert: low amplitude (2 to 5°), 22 to 30 Hz, typically 4 to 35 s, often triggered by convergence; their own case ran 13 Hz, about 8°, for 4 to 5 s. Rating: High certainty; on/off; Minority (8%, measured, familial).

**Ear muscles.** Code (1995) \[52\], n = 442: about 22% could move one or the other ear and 18% both at once, more men than women. Strauss et al. (2020) \[53\] recorded surface EMG from four auricular muscles in 28 and 21 participants and found activity larger on the side of an attended sound: vestigial orienting, not voluntary control. The popular "10 to 20%" figure (an Ancestry trait page citing 790,000 customers) has no published rate. Rating: High certainty; on/off; Minority (22%, measured).

**Piloerection on cue.** Heathers et al. (2018) \[5\] surveyed 32 people who can raise goosebumps at will; about 80% described the same route, muscular tension at the back of the head, neck or behind the ear, with the bumps spreading down the back and arms, and the group scored high on openness to experience. Katahira et al. (2020) \[48\] added objective evidence: of 4,005 panel respondents, 112 (2.8%) were candidates; in an at-home video study analysed with GooseLab, 9 of 15 participants showed significant piloerection, onset 4.04 s (SD 2.64, range 0.93 to 15.40) after the cue and offset 11.79 s (SD 8.28) after the stop cue; no skin-conductance or heart-rate measures were taken. Rating: Moderate certainty; on/off; Rare (2.8%).

## Evidence: brain activity and pain perception

People can learn to steer single neurons, EEG rhythms and regional fMRI signals when they are shown the signal, and can cut experimental pain by 17 to 57% through suggestion or trained attention; the brain-signal control is well established, the clinical benefits attached to it mostly are not.

**Single neurons via implant.** Cerf et al. (2010) \[8\] worked with epilepsy patients carrying depth electrodes in the medial temporal lobe. Shown a hybrid of two familiar images, patients "reliably regulated, often on the first trial, the firing rate of their neurons", raising one cell's activity and lowering another's to make the chosen image clearer. The abstract gives no success rate or firing-rate magnitude, and the full text was not accessible; a recalled figure of about 70% of trials was not read and is not used. Rating: High certainty; not quantified; Most with training (implant patients).

**EEG rhythms.** Kamiya (1968) \[59\] was among the first to show operant self-regulation of the alpha band (8 to 12 Hz), as reviewed by Enriquez-Geppert, Huster and Herrmann (2017) \[57\]. Sterman and Egner (2006) \[58\] call sensorimotor-rhythm training for epilepsy "arguably the best established clinical application of EEG operant conditioning", citing Wyrwicka and Sterman (1968) in cats and Sterman and Friar (1972) as the first human case. Non-learning is common: Alkoby et al. (2018) \[60\] state that "a significant proportion of subjects does not benefit", and Jacques et al. (2024) \[85\] put non-responders at 15 to 50%. Clinical outcome is weaker than signal control. Cortese et al. (2016) \[61\], 13 RCTs and 520 participants: SMD 0.35 \[0.11, 0.59\] on ratings by the least-blinded raters, not significant with probably-blinded raters or against active and sham controls, and only 4 studies checked whether learning occurred. Westwood et al. (2025) \[62\], 38 RCTs and 2,472 participants: probably-blinded total SMD 0.04 \[−0.10, 0.18\] across 20 trials, 0.21 \[0.02, 0.40\] for standard protocols across 9. Tan et al. (2009) \[63\], epilepsy: 64 of 87 patients (74%) across 10 pre-post studies reported fewer weekly seizures, effect −0.233 (SE 0.057, p < .001), flagged by the DARE appraisal for tiny samples and possible publication bias. Rating: High certainty for the control; not quantified; Most with training, with 15 to 50% non-learners.

**Regional brain activity via real-time fMRI.** deCharms et al. (2005) \[64\] trained subjects to raise or lower rostral anterior cingulate activation and reported a corresponding change in pain perception and lower chronic pain after training, against controls given no feedback, feedback from another region, or sham. The follow-up trial reported in Sulzer et al. (2013) \[65\], 21 experimental and 38 sham participants over six sessions, found "both groups improved similarly"; Thibault, Lifshitz and Raz (2016) \[66\] note that only true feedback produced neural control while pain fell equally in both arms, and no standalone results paper exists. Emmert et al. (2014) \[67\], n = 28, found no significant anterior-cingulate down-regulation across all subjects. Sitaram et al. (2017) \[68\] conclude that learned control over specific neural substrates changes specific behaviours; Thibault et al. (2018) \[69\], reviewing 99 experiments, conclude that self-regulation of brain signatures "seems viable; however, replication of concomitant behavioral outcomes remains sparse". Rating: Moderate certainty; not quantified; Most with training.

**Hypnotic analgesia.** Montgomery, DuHamel and Redd (2000) \[70\] pooled 18 studies, 27 effect sizes and 933 participants: D = 0.67, meaning the average hypnotised participant reported more relief than 75% of controls (a percentile conversion of d, not a responder rate); by suggestibility D = 1.16 high, 0.64 medium, −0.01 low; clinical and experimental pain did not differ. Thompson et al. (2019) \[71\], 85 experimental-pain trials and 3,632 healthy participants: g 0.54 to 0.76 across outcomes; with a direct analgesic suggestion, pain fell 2.30 points (42%) in high, 1.60 (29%) in medium and 0.97 (17%) in low suggestibles, all p < .001; without such a suggestion, lows changed 0.03 points (p = .931). Rating: High certainty; 0.67 (reported effect size), Moderate, rising to 1.16 in high suggestibles; Most with training, scaling with suggestibility.

**Meditation analgesia.** Zeidan et al. (2011) \[72\] gave 15 volunteers four 20-min sessions and found pain unpleasantness reduced 57% and intensity 40% versus rest (intensity F(1,14) = 20.49, η² = 0.59; unpleasantness F(1,14) = 87.99, η² = 0.86), with no sham arm. Zeidan et al. (2015) \[73\], n = 75, compared meditation with placebo cream, sham meditation and book-listening control: intensity fell 27% with meditation versus 11% placebo and 8% sham (control +14%); unpleasantness 16% versus 11%, 7% and +18%; meditation beat placebo (p = 0.032 intensity, p < 0.001 unpleasantness) and sham (p = 0.030, p = 0.043). Zeidan et al. (2016) \[74\], double-blind, n = 78, with naloxone 0.15 mg/kg plus 0.1 mg/kg/h: intensity fell 24% under naloxone versus 21% under saline (p = 0.69) and unpleasantness 33% versus 36% (p = 0.75), so the relief is not opioid-mediated in novices. Khatib et al. (2024) \[76\] replicated the naloxone result in 59 chronic low-back-pain patients; Sharon et al. (2016) \[75\] found the opposite in 15 experienced meditators, where relief vanished under naloxone. Rating: Moderate certainty (mostly one group); −40% intensity, percent only, Large; Most with training (novices after four sessions).

**Seizure frequency via skin-conductance feedback.** Nagai et al. (2004) \[35\] randomised 18 patients, 10 active and 8 sham: seizures fell in the active group (P = 0.017) but not controls (P > 0.10), between-group P = 0.01. Nagai et al. (2018) \[36\] randomised 40 patients with drug-resistant temporal-lobe epilepsy to biofeedback or usual care (not sham): mean seizure reduction 43%, with 45% of patients improving more than 50%, while controls rose 31% (p < 0.001). Nagai, Jones and Sen (2019) \[37\] pooled 4 studies and 99 patients: biofeedback minus control −64.3% \[−85.4, −43.2\], responder rates 45 to 66%, and "none of the studies can robustly eliminate the bias from expectation". Rating: Moderate certainty (two of four trials from one group); −43%, percent only, Large; Most with training.

## Evidence: hard-wired links and claims not supported

Every documented link from one nervous system to a machine or to another person runs through hardware; no unaided link has survived replication.

**Nerve implant and nerve-to-nerve link (Warwick).** On 14 March 2002, at the Radcliffe Infirmary, Oxford, a 100-electrode array was implanted into the median nerve fibres of Kevin Warwick's left arm \[11\]. Through it he operated an electric wheelchair and an articulated hand, received artificial sensation by stimulation through individual electrodes, and, from Columbia University in New York, flexed a robot hand in Reading over the internet. His wife Irena then received a simpler implant, and the two were linked over the internet: each time she opened or closed her hand he received pulses, with transmission accuracy reported above 98% \[12\]; she described the incoming signal as "lightning in the palm of her hand". Guinness World Records lists it as the first electronic communication between human nervous systems \[94\]. The 98% figure comes from a secondary account of \[12\], which was not read.

**Brain to spine (digital bridge).** Lorach et al. (2023) \[13\] implanted two 64-electrode WIMAGINE epidural recorders over the sensorimotor cortex and a 16-electrode paddle lead with an ACTIVA RC pulse generator over the lumbosacral cord in one man with chronic tetraplegia. The interface decodes walking intent and modulates stimulation in real time: calibration "within a few minutes", stable over one year including independent home use, standing and walking in community settings, stair climbing, and recovery of overground walking with crutches even with the interface switched off.

**Brain to brain.** Rao et al. (2014) \[14\], three pairs: a sender's imagined hand movement, read by EEG in the mu band, triggered transcranial magnetic stimulation over the receiver's motor cortex, whose hand then jerked and struck a touchpad. Accuracy was 83.3%, 25.0% and 37.5% across the three pairs, against 0% in control blocks with the channel disabled. Jiang et al. (2019) \[15\], BrainNet, five triads of 18 to 35-year-olds: two senders' decisions, encoded as 15 and 17 Hz steady-state visual evoked potentials, were delivered to a receiver's occipital cortex as phosphenes by TMS during a Tetris-like task; mean accuracy 81.25%, above the 50% chance level (p = 0.002).

**Brain to computer at scale.** Neuralink reported 21 trial participants enrolled worldwide in January 2026 \[96\]; the figure is a company statement relayed by press, not a peer-reviewed count.

**Stopping the heart.** Covered in the cardiovascular section: Wenger, Bagchi and Anand (1961) \[22\] found reduced QRS amplitude under a Valsalva-type manoeuvre, not cardiac arrest. Not supported.

**Unaided mind-to-mind transfer.** The main experimental literature is the ganzfeld telepathy paradigm. Milton and Wiseman (1999) \[16\] pooled 30 ganzfeld studies from 7 independent laboratories that had followed the Bem and Honorton (1994) protocol: participants did not score above chance (p = .24), only 1 of 3 previously reported moderator effects was confirmed, and the authors concluded that "the ganzfeld technique does not at present offer a replicable method for producing ESP in the laboratory". Later positive meta-analyses from proponents remain disputed, and no mechanism has been proposed. Not supported; no documented case of a person reaching another person's nerves without hardware.

**Excluded as not deliberate.** Two top-down effects are real but not initiated by the person, so they are documented here and left out of the scoring. Placebo analgesia uses endogenous opioids: Levine, Gordon and Fields (1978) \[77\] showed after third-molar extraction that naloxone's enhancement of reported pain "can be entirely accounted for by its effect on placebo responders"; Grevert, Albert and Goldstein (1983) \[79\], n = 30, found naloxone only partly reversed it; Sauro and Greenberg (2005) \[78\], 12 studies and 1,183 participants, confirmed that a hidden or blind naloxone injection reverses placebo analgesia. Conditioned immunosuppression: Goebel et al. (2002) \[80\] paired a novel drink with cyclosporin A 2.5 mg/kg in 18 of 34 healthy men; re-exposure to the drink alone suppressed IL-2 and IFN-γ mRNA expression, intracellular production, in-vitro release and lymphocyte proliferation. Albring et al. (2012) \[81\] found suppression after four re-exposures but not one; Kirchhof et al. (2018) \[82\] reproduced it in 30 renal-transplant patients, where T-cell proliferative capacity was significantly reduced.

## Quantitative synthesis

Response strength falls as evidence quality and prevalence rise: Spearman ρ = −0.60 with certainty (p ≈ 0.05) and ρ = −0.81 with prevalence (p = 0.002), over the 11 abilities with a computed score.

&#91;embedded content: Scored from the evidence sections above · 17 abilities with a magnitude; on/off and unquantified abilities are not plotted\]

The Extreme band holds four Low-certainty hills from one to ten people and one High-certainty, measured-minority ability, the middle-ear muscle; everything most people can train sits in the Small to Moderate bands.

**How to read the correlation.** Two biases are built into the comparison and both steepen the slope. Low-certainty rows report the best individual result (the 8.3 °C monk, the 7 °C hand), while High-certainty rows report group means, and small studies overstate effects. The direction is therefore more trustworthy than the coefficient, and the protocol in Section 12 is designed to remove the first bias by measuring individuals and groups in the same sample.

**What survives the biases.** The lever pattern does not depend on effect size: every High-certainty ability runs through feedback, breathing, skeletal-muscle tension, imagery or suggestion, and the only lever-free abilities with population measurements are three small muscles (tensor tympani, extraocular, auricular) and piloerection. The tensor tympani is the one lever-free, Extreme, High-certainty, common ability in the set, which makes it the natural anchor for a primary study.

**Unplotted abilities.** Four on/off abilities (single motor units, voluntary nystagmus, ear muscles, goosebumps) and five unquantified ones (single neurons, EEG rhythms, fMRI regions, pelvic floor, vagal output) have no magnitude to place. An interactive 3D version of this map, with certainty and prevalence as ground axes and strength as elevation, is published separately as the Voluntary Control Terrain artifact.

## Verification status

Of the 98 sources cited, the figures used were read in the primary source (publisher page, repository copy or PMC full text) for 72; the 26 below rest partly on secondary accounts, citation records, or abstracts, and each gap is named so a reviewer can close it. DOIs were checked against Crossref or the publisher page for every reference that lists one; references without a DOI are given with PubMed ID or URL instead.

| Source | What was read | What remains |
| --- | --- | --- |
| Basmajian 1963 \[6\] | Citation record only | Abstract and figures not read (Science page blocked) |
| Engel & Hansen 1966 \[19\], Engel & Chism 1967 \[20\], Brener & Hothersall 1966 \[21\] | Citations from a reference list; Engel & Chism DOI confirmed | bpm figures not read (Wiley 403) |
| Wenger, Bagchi & Anand 1961 \[22\] | Quotations in Raghavendra 2013 \[24\] and Khalsa 2015 \[23\]; DOI confirmed | Primary paper not read (ahajournals 403); number of subjects unconfirmed |
| Green & Green 1977 \[25\] | Book excerpt on hihtindia.org | Figures differ between accounts (300 bpm/17 s vs 306 bpm/16.2 s); no peer-reviewed report found after searching Menninger, atrial flutter and the 1970 preliminary report |
| Maslach et al. 1972 \[31\] | The authors' 1970 ONR report (DTIC AD0716481); DOI confirmed | Journal article not read (Wiley 403) |
| Campbell, Penzien & Wall 2000 \[32\] | Grade A wording quoted in Andrasik 2010 \[33\] and Ha & Gonzalez 2019 | Guideline PDF now returns 404 |
| Heathers et al. 2018 \[5\] | Northeastern news release; DOI confirmed | Paper text not read; n = 32 and the 80% figure are from the release |
| Warwick 2003 \[11\], 2004 \[12\] | Coventry project page, Guinness record \[94\], Atlas Obscura; DOIs confirmed | Papers not read; the >98% accuracy is a secondary account of \[12\] |
| Cerf et al. 2010 \[8\] | Nature abstract | Success rate and firing-rate magnitude not in the abstract; a recalled 70% figure not used |
| Kamiya 1968 \[59\] | As cited in Enriquez-Geppert 2017 \[57\] | Original magazine article not read |
| deCharms et al. 2005 \[64\] | ADS abstract; DOI confirmed | PNAS and PMC blocked; n (12 patients) taken from Thibault 2016 \[66\] |
| Levine, Gordon & Fields 1978 \[77\] | Lancet abstract; DOI confirmed | n not read |
| Angeli et al. 2013 \[45\] | PubMed record (PMID 24289817) | Values and DOI not confirmed |
| Zahn 1978 \[46\] | PMC abstract; DOI confirmed | Hz and duration figures taken from Thomas 2022 \[47\]; survey n not read |
| Calatayud et al. 2016 \[50\] | Abstract (threshold); Table 2 from an academia.edu copy | EMG units inferred as percentage points of maximum; one confidence interval garbled in extraction |
| Schoenfeld et al. 2018 \[51\] | Crossref-deposited abstract | Effect sizes not read; only 12.4% vs 6.9% verified |
| Cortese et al. 2016 \[61\] | ScienceDirect abstract | Probably-blinded SMD magnitudes not read; the statement that they were not significant is from the abstract |
| Westwood et al. 2025 \[62\] | KCL repository abstract; DOI confirmed | Full text not read |
| Zeidan et al. 2015 \[73\] | Journal page | Percentages labelled "MRI Session B"; baseline definition not confirmed |
| Lin, Tai & Fan 2014 \[93\] | Abstract | SDNN and LF values not read |
| Macefield et al. 2026 \[84\] | PMC full text, by the research pass | Title concerns maximal breath-holds; the "unchanged during slow breathing" statement needs a second read |
| Kox et al. 2012 \[2\] | Radboud press release and DOI record | The single-case description (larger cortisol rise, much lower inflammatory mediators, hardly any flu-like symptoms) is the press release's wording \[98\]; the paper itself was not read |
| Neuralink count \[96\] | Press reports of a company statement | Not peer-reviewed |

**Corrections made during reconciliation.**

- Wenger, Bagchi and Anand 1961 is in Circulation 24:1319–1325; the Behavioral Science paper of the same year is a separate article.
- The Nagai controlled trial is 2018 (EBioMedicine); the 2019 Frontiers paper is the meta-analysis.
- Grade A in the US Headache Consortium guideline covers thermal biofeedback combined with relaxation, not thermal biofeedback alone.
- Montgomery's 75% is a percentile conversion of d = 0.67 against controls, not a responder rate.
- The deCharms non-replication is the trial reported inside Sulzer et al. 2013; citations to "deCharms 2012" resolve to the 2008 review.
- The DOI first assumed for Chiarioni et al. 2006 belongs to another paper; it is cited by PMID 16530506.
- Khalsa et al. 2015 is Khalsa, Rudrauf, Davidson and Tranel, "The effect of meditation on regulation of internal body states".
- The core-temperature score uses the population SD (0.48 °C); the within-study SD (0.21 °C) would give 10.5 SD.
- The popular "10 to 20% can wiggle their ears" figure has no published source; Code 1995 gives 22% and 18%.

**Access failures during the review.** ahajournals, Wiley, Taylor & Francis, Science and gastrojournal returned 403; PubMed pages returned no content; PNAS, PMC and JAMA Network intermittently served CAPTCHAs; Europe PMC, Crossref, OpenAlex, Semantic Scholar and ResearchGate rate-limited after a few requests. Each case above says which route was used instead.

## Gaps and research questions

The literature has never measured the lever-free abilities in one unselected sample with one set of instruments, so prevalence, co-occurrence, mechanism and heritability are all open.

**Gaps.**

- No common scale. Effects are reported as percent change, raw units, d, η² or a binary outcome, and no review has converted them to a shared metric; the ranking in Section 9 is the first.
- Prevalence is measured for only four lever-free abilities, each in a different sample decades apart: tensor tympani 43% (2021), auricular muscles 22% (1995), voluntary nystagmus 8% (1978), piloerection 2.8% (2020). No study reports whether they co-occur.
- Selection bias. The largest effects (8.3 °C, 7 °C, 2.2 °C, 2.4 mm) are best cases from adepts or single subjects; the distribution of ability in an unselected sample has never been measured with the same instrument that produced the best case.
- Mechanism. Piloerection is said by 80% of possessors to run through head and neck tension, but no EMG study has tested it; Hoyle et al. found only 65% of rumblers could contract the tensor tympani "in isolation"; the direct pupil case stands alone.
- Heritability. The only datum is Zahn's 79% of voluntary-nystagmus possessors with an affected relative.
- Trait correlates. Openness to experience in goosebump possessors is the only reported correlate; hypnotic suggestibility, interoceptive accuracy and vocal or musical training are untested.
- Trainability. Whether non-possessors can acquire a lever-free ability with feedback has been tested only for the pupil, and there through imagery.
- Verification standards differ: otoscopy, tympanometry, video analysis and eye tracking have each been used once, with no agreed threshold.

**Research questions.**

1. What proportion of unselected adults can contract the tensor tympani, produce voluntary nystagmus, move the auricular muscles and raise piloerection on cue, each confirmed by an objective instrument in the same session?
2. Do these abilities co-occur beyond chance, which would indicate a general trait of voluntary access to normally involuntary effectors?
3. Are they lever-free: does surface EMG of the masseter, temporalis, sternocleidomastoid and frontalis stay silent during a confirmed response?
4. Do they aggregate in first-degree relatives?
5. Which traits predict possession: hypnotic suggestibility, openness, interoceptive accuracy, musical or vocal training, age, sex?
6. Can non-possessors acquire one ability with instrument feedback in five sessions, and does acquisition transfer to a second effector?
7. When every ability in this review is re-extracted under pre-registered rules, does the inverse relation between strength and certainty survive, and how much of it is explained by best-case reporting in small studies?

## Proposed study protocol

Working title: *Lever-free voluntary control of involuntary effectors: prevalence, co-occurrence, mechanism and trainability in an unselected adult sample.* Two phases over 18 months, three papers, one public dataset.

**Aims.**

1. Phase 1: a pre-registered systematic review that re-extracts every ability in this document on the common scale of Section 3 (PRISMA 2020, PROSPERO registration).
2. Phase 2: measure the prevalence of four lever-free abilities in an unselected sample with objective confirmation in one session.
3. Test whether the abilities co-occur and whether a single "voluntary access" factor explains them.
4. Test the lever-free claim with co-registered surface EMG.
5. Estimate familial aggregation and trait correlates.
6. Pilot whether non-possessors can acquire tensor tympani contraction with instrument feedback.

**Pre-registered hypotheses.**

- H1. Objective prevalence of tensor tympani contraction in an unselected sample lies between 25% and 45% (self-report 43% \[42\]; 80% of self-reporters confirmed in \[43\]).
- H2. Possessing one ability raises the odds of possessing another: odds ratio above 2, against a null of 1.
- H3. In at least 80% of confirmed tensor tympani, nystagmus and auricular responses, peak EMG of masseter, temporalis, sternocleidomastoid and frontalis stays below twice the resting level; piloerection is predicted to fail this test, consistent with the neck-tension route reported by 80% of possessors \[5\].
- H4. First-degree relatives of confirmed possessors report the same ability at twice the population rate or more.
- H5. Hypnotic suggestibility and openness correlate with the access score at r ≥ 0.2.
- H6. After five feedback sessions, at least 20% of non-possessors reach the tensor tympani criterion, against 3% or fewer with sham feedback.
- H7. In Phase 1, the inverse correlation between strength and certainty attenuates by at least half when group means replace best-case individual values.

**Design.**

- Phase 1 (months 1 to 4). Searches in PubMed, Embase, PsycINFO and Web of Science plus the first 200 Google Scholar hits per term; inclusion: humans, a self-initiated change in the person's own body, an objective or validated measure; extraction of Δ, SD, n and design by two raters; risk of bias with RoB 2 for trials and the JBI tool for case reports; strength computed per Section 3; sensitivity analysis excluding studies with n ≤ 3.
- Phase 2a, survey (months 3 to 9). Online panel, n = 2,000, quota-matched to census age and sex, recruited with a topic-blind advertisement as in \[42\]. Items: each ability described in plain words with a 15-second demonstration video; two distractor abilities as a response-bias check; family items for parents, siblings and children; Ten-Item Personality Inventory; Multidimensional Assessment of Interoceptive Awareness; musical and vocal training; attention checks.
- Phase 2b, laboratory verification (months 6 to 14). n = 240 from the survey: 120 self-reported possessors of at least one ability, stratified by ability, and 120 non-possessors. Ten cued trials per ability in randomised order, instrument records scored by a rater blind to self-report.
- Phase 2c, training pilot (months 10 to 16). 60 confirmed non-possessors randomised 1:1 to tympanometric feedback or yoked sham feedback, five 20-minute sessions, criterion test at session five and at four weeks.
- Phase 2d, families (months 10 to 16). Relatives of confirmed possessors invited for the same verification battery, target n = 100.

&#91;embedded content: study timeline · 6 workstreams over 18 months, from the design above\]

Analysis and writing run from month 14 to 18, overlapping the training and family arms; the laboratory verification is the critical path.

**Measures.**

| Ability | Instrument | Criterion for a confirmed response | Magnitude in SD units (baseline from Section 3) |
| --- | --- | --- | --- |
| Tensor tympani contraction | 226 Hz tympanometry during the cue, with otoscopic video | Admittance shift with the characteristic pattern of \[44\], on at least 7 of 10 trials | Air-conduction threshold shift at 250 Hz / 5 dB |
| Voluntary nystagmus | Video-oculography at 500 Hz | Oscillation ≥ 10 Hz sustained ≥ 2 s, no convergence trigger required | Frequency and duration reported; no SD baseline exists |
| Auricular movement | Marker-tracked video of both ears plus auricular EMG | Displacement ≥ 2 mm on cue, either ear | Displacement reported; no SD baseline exists |
| Piloerection | Forearm video analysed with GooseLab \[48\], plus skin conductance | Significant piloerection index on cue versus rest, as in \[48\] | Onset latency reported |
| Pupil, exploratory | Pupillometry at fixed luminance (50 cd/m²) with a fixed accommodation target | Change ≥ 0.5 mm within 10 s with no change in vergence | Change / 0.9 mm |
| Lever check, all abilities | Surface EMG: masseter, temporalis, sternocleidomastoid, frontalis, posterior auricular | Peak RMS during response divided by resting RMS below 2 | — |

**Participants.** Adults 18 to 65; hearing thresholds ≤ 25 dB HL at 250 to 4,000 Hz; no middle-ear disease, ear surgery, neurological disorder or eye-movement disorder; no medication affecting pupil size. The survey states only that the study concerns "unusual physical abilities"; the specific abilities are disclosed at debrief.

**Sample size.** The survey's n = 2,000 gives a 95% confidence half-width of ±2.2 percentage points at a prevalence of 43% and ±0.7 points at 2.8%. For H2, a chi-square test on two abilities with base rates 35% and 20% under an odds ratio of 2.5 has effect size w = 0.18, which needs n = 234 for 80% power at α = 0.05; the lab sample of 240 meets it even before oversampling possessors. For H6, 30 per arm gives 80% power to detect 20% versus 3% acquisition (two-sided α = 0.05, arcsine approximation).

**Analysis plan.** Prevalence with Wilson intervals, weighted to census age and sex; self-report against objective confirmation as sensitivity, specificity and positive predictive value; co-occurrence by logistic regression adjusted for age and sex, with tetrachoric correlations and an exploratory one-factor model; the EMG lever index per trial; familial relative risk with exact intervals; trait correlations with Holm correction; training by intention-to-treat difference in proportions. Pre-registration on OSF before data collection, instrument records scored blind, data and code public at publication.

**Ethics.** Institutional review board approval; minimal-risk procedures (tympanometry, video-oculography, surface EMG, video); informed consent with the topic-blind wording disclosed at debrief; no cold exposure, hyperventilation, endotoxin or hypnosis is used.

**Outputs.** Paper 1, the systematic review with the common-scale ranking; Paper 2, prevalence, co-occurrence and mechanism; Paper 3, the training pilot; a public dataset; and a lay article built on the one finding that is High certainty, Extreme and common: about four in ten people can contract a muscle inside the ear at will.

## References

Numbered as cited. DOIs were confirmed against Crossref or the publisher page; where none could be confirmed the entry carries a PubMed ID or URL instead, and author lists marked "et al." after three names were not read in full.

1. Kox M, van Eijk LT, Zwaag J, van den Wildenberg J, Sweep FCGJ, van der Hoeven JG, Pickkers P. Voluntary activation of the sympathetic nervous system and attenuation of the innate immune response in humans. Proc Natl Acad Sci USA. 2014;111(20):7379–7384. doi:10.1073/pnas.1322174111
2. Kox M, Stoffels M, Smeekens SP, et al. The influence of concentration/meditation on autonomic nervous system activity and the innate immune response: a case study. Psychosom Med. 2012;74(5):489–494. doi:10.1097/PSY.0b013e3182583c6d
3. Benson H, Lehmann JW, Malhotra MS, Goldman RF, Hopkins J, Epstein MD. Body temperature changes during the practice of g Tum-mo yoga. Nature. 1982;295(5846):234–236. doi:10.1038/295234a0
4. Kozhevnikov M, Elliott J, Shephard J, Gramann K. Neurocognitive and somatic components of temperature increases during g-Tummo meditation: legend and reality. PLoS ONE. 2013;8(3):e58244. doi:10.1371/journal.pone.0058244
5. Heathers JAJ, Fayn K, Silvia PJ, Tiliopoulos N, Goodwin MS. The voluntary control of piloerection. PeerJ. 2018;6:e5292. doi:10.7717/peerj.5292
6. Basmajian JV. Control and training of individual motor units. Science. 1963;141(3579):440–441. doi:10.1126/science.141.3579.440
7. Bräcklein M, Barsakcioglu DY, Ibáñez J, Eden J, Burdet E, Mehring C, Farina D. The control and training of single motor units in isometric tasks are constrained by a common input signal. eLife. 2022;11:e72871. doi:10.7554/eLife.72871
8. Cerf M, Thiruvengadam N, Mormann F, Kraskov A, Quian Quiroga R, Koch C, Fried I. On-line, voluntary control of human temporal lobe neurons. Nature. 2010;467(7319):1104–1108. doi:10.1038/nature09510
9. Ranganathan VK, Siemionow V, Liu JZ, Sahgal V, Yue GH. From mental power to muscle power: gaining strength by using the mind. Neuropsychologia. 2004;42(7):944–956. doi:10.1016/j.neuropsychologia.2003.11.018
10. Clark BC, Mahato NK, Nakazawa M, Law TD, Thomas JS. The power of the mind: the cortex as a critical determinant of muscle strength/weakness. J Neurophysiol. 2014;112(12):3219–3226. doi:10.1152/jn.00386.2014
11. Warwick K, Gasson M, Hutt B, Goodhew I, Kyberd P, Andrews B, Teddy P, Shad A. The application of implant technology for cybernetic systems. Arch Neurol. 2003;60(10):1369–1373. doi:10.1001/archneur.60.10.1369
12. Warwick K, Gasson M, Hutt B, et al. Thought communication and control: a first step using radiotelegraphy. IEE Proc Commun. 2004;151(3):185–189. doi:10.1049/ip-com:20040409
13. Lorach H, Galvez A, Spagnolo V, et al. Walking naturally after spinal cord injury using a brain–spine interface. Nature. 2023;618(7963):126–133. doi:10.1038/s41586-023-06094-5
14. Rao RPN, Stocco A, Bryan M, Sarma D, Youngquist TM, Wu J, Prat CS. A direct brain-to-brain interface in humans. PLoS ONE. 2014;9(11):e111332. doi:10.1371/journal.pone.0111332
15. Jiang L, Stocco A, Losey DM, Abernethy JA, Prat CS, Rao RPN. BrainNet: a multi-person brain-to-brain interface for direct collaboration between brains. Sci Rep. 2019;9:6115. doi:10.1038/s41598-019-41895-7
16. Milton J, Wiseman R. Does psi exist? Lack of replication of an anomalous process of information transfer. Psychol Bull. 1999;125(4):387–391. doi:10.1037/0033-2909.125.4.387
17. Manuck SB. The voluntary control of heart rate under differential somatic restraint. Biofeedback Self Regul. 1976;1(3):273–284. doi:10.1007/BF01001168
18. Belmaker R, Proctor E, Feather BW. Muscle tension in human operant heart rate conditioning. Cond Reflex. 1972;7(2):97–106. doi:10.1007/BF03000479
19. Engel BT, Hansen SP. Operant conditioning of heart rate slowing. Psychophysiology. 1966;3(2):176–187.
20. Engel BT, Chism RA. Operant conditioning of heart rate speeding. Psychophysiology. 1967;3(4):418–426. doi:10.1111/j.1469-8986.1967.tb02728.x
21. Brener J, Hothersall D. Heart rate control under conditions of augmented sensory feedback. Psychophysiology. 1966;3. doi:10.1111/j.1469-8986.1966.tb02675.x
22. Wenger MA, Bagchi BK, Anand BK. Experiments in India on "voluntary" control of the heart and pulse. Circulation. 1961;24:1319–1325. doi:10.1161/01.CIR.24.6.1319
23. Khalsa SS, Rudrauf D, Davidson RJ, Tranel D. The effect of meditation on regulation of internal body states. Front Psychol. 2015;6:924. doi:10.3389/fpsyg.2015.00924
24. Raghavendra BR, Telles S, Manjunath NK, Deepak KK, Naveen KV, Subramanya P. Voluntary heart rate reduction following yoga using different strategies. Int J Yoga. 2013;6(1):26–30. doi:10.4103/0973-6131.105940
25. Green E, Green A. Beyond Biofeedback. New York: Delacorte Press; 1977. Chapter II.
26. Goessl VC, Curtiss JE, Hofmann SG. The effect of heart rate variability biofeedback training on stress and anxiety: a meta-analysis. Psychol Med. 2017;47(15):2578–2586. doi:10.1017/S0033291717001003
27. Lehrer PM, Gevirtz R. Heart rate variability biofeedback: how and why does it work? Front Psychol. 2014;5:756. doi:10.3389/fpsyg.2014.00756
28. Lehrer P, Kaur K, Sharma A, et al. Heart rate variability biofeedback improves emotional and physical health and performance: a systematic review and meta analysis. Appl Psychophysiol Biofeedback. 2020;45(3):109–129. doi:10.1007/s10484-020-09466-z
29. Pizzoli SFM, et al. A meta-analysis on heart rate variability biofeedback and depressive symptoms. Sci Rep. 2021;11:6650. doi:10.1038/s41598-021-86149-7
30. Brook RD, Appel LJ, Rubenfire M, et al. Beyond medications and diet: alternative approaches to lowering blood pressure. A scientific statement from the American Heart Association. Hypertension. 2013;61(6):1360–1383. doi:10.1161/HYP.0b013e318293645f
31. Maslach C, Marshall G, Zimbardo PG. Hypnotic control of peripheral skin temperature: a case report. Psychophysiology. 1972;9(6):600–605. doi:10.1111/j.1469-8986.1972.tb00769.x. Figures from the same authors' ONR Technical Report Z-OA, November 1970, DTIC AD0716481.
32. Campbell JK, Penzien DB, Wall EM. Evidence-based guidelines for migraine headache: behavioral and physical treatments. US Headache Consortium; 2000.
33. Andrasik F. Biofeedback in headache: an overview of approaches and evidence. Cleve Clin J Med. 2010;77(Suppl 3):S72–S76. PMID 20622082.
34. Raynaud's Treatment Study Investigators. Comparison of sustained-release nifedipine and temperature biofeedback for treatment of primary Raynaud phenomenon: results from a randomized clinical trial with 1-year follow-up. Arch Intern Med. 2000;160(8):1101–1108. doi:10.1001/archinte.160.8.1101
35. Nagai Y, Goldstein LH, Fenwick PBC, Trimble MR. Clinical efficacy of galvanic skin response biofeedback training in reducing seizures in adult epilepsy: a preliminary randomized controlled study. Epilepsy Behav. 2004;5(2):216–223. doi:10.1016/j.yebeh.2003.12.003
36. Nagai Y, Aram J, Koepp M, et al. Epileptic seizures are reduced by autonomic biofeedback therapy through enhancement of fronto-limbic connectivity: a controlled trial and neuroimaging study. EBioMedicine. 2018;27:112–122. doi:10.1016/j.ebiom.2017.12.012
37. Nagai Y, Jones CI, Sen A. Galvanic skin response (GSR)/electrodermal/skin conductance biofeedback on epilepsy: a systematic review and meta-analysis. Front Neurol. 2019;10:377. doi:10.3389/fneur.2019.00377
38. Zwaag J, Naaktgeboren R, van Herwaarden AE, Pickkers P, Kox M. The effects of cold exposure training and a breathing exercise on the inflammatory response in humans: a pilot study. Psychosom Med. 2022;84(4):457–467. doi:10.1097/PSY.0000000000001065
39. Eberhardt LV, Grön G, Ulrich M, Huckauf A, Strauch C. Direct voluntary control of pupil constriction and dilation: exploratory evidence from pupillometry, optometry, skin conductance, perception, and functional MRI. Int J Psychophysiol. 2021;168:33–42. doi:10.1016/j.ijpsycho.2021.08.001
40. Meissner SN, Bächinger M, Kikkert S, Imhof J, Missura S, Carro Dominguez M, Wenderoth N. Self-regulating arousal via pupil-based biofeedback. Nat Hum Behav. 2024;8(1):43–62. doi:10.1038/s41562-023-01729-z
41. Laeng B, Sulutvedt U. The eye pupil adjusts to imaginary light. Psychol Sci. 2014;25(1):188–197. doi:10.1177/0956797613503556
42. Röddiger T, Clarke C, Wolffram D, Budde M, Beigl M. EarRumble: discreet hands- and eyes-free input by voluntary tensor tympani muscle contraction. CHI '21: Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems; 2021. doi:10.1145/3411764.3445205
43. Hoyle AC, Stevenson R, Leonhardt M, et al. Exploring the 'EarSwitch' concept: a novel ear based control method for assistive technology. J NeuroEng Rehabil. 2024;21:210. doi:10.1186/s12984-024-01500-z
44. Wickens B, Floyd D, Bance M. Audiometric findings with voluntary tensor tympani contraction. J Otolaryngol Head Neck Surg. 2017;46:2. doi:10.1186/s40463-016-0182-y
45. Angeli RD, et al. Voluntary contraction of the tensor tympani muscle and its audiometric effects. J Laryngol Otol. 2013;127(12):1235–1237. PMID 24289817.
46. Zahn JR. Incidence and characteristics of voluntary nystagmus. J Neurol Neurosurg Psychiatry. 1978;41(7):617–623. doi:10.1136/jnnp.41.7.617
47. Thomas N, Dunn MJ, Woodhouse JM. Voluntary flutter presenting during ophthalmoscopy: a case report. Case Rep Ophthalmol. 2022;13(1):286–291. doi:10.1159/000524384
48. Katahira K, Kawakami A, Tomita A, Nagata N. Volitional control of piloerection: objective evidence and its potential utility in neuroscience research. Front Neurosci. 2020;14:590. doi:10.3389/fnins.2020.00590
49. Paravlic AH, Slimani M, Tod D, Marusic U, Milanovic Z, Pisot R. Effects and dose–response relationships of motor imagery practice on strength development in healthy adult populations: a systematic review and meta-analysis. Sports Med. 2018;48(5):1165–1187. doi:10.1007/s40279-018-0874-8
50. Calatayud J, Vinstrup J, Jakobsen MD, Sundstrup E, Brandt M, Jay K, Colado JC, Andersen LL. Importance of mind-muscle connection during progressive resistance training. Eur J Appl Physiol. 2016;116(3):527–533. doi:10.1007/s00421-015-3305-7
51. Schoenfeld BJ, Vigotsky A, Contreras B, Golden S, Alto A, Larson R, Winkelman N, Paoli A. Differential effects of attentional focus strategies during long-term resistance training. Eur J Sport Sci. 2018;18(5):705–712. doi:10.1080/17461391.2018.1447020
52. Code C. Asymmetries in ear movements and eyebrow raising in men and women and right- and left-handers. Percept Mot Skills. 1995;80(3 Suppl):1147–1154. doi:10.2466/pms.1995.80.3c.1147
53. Strauss DJ, Corona-Strauss FI, Schroeer A, Flotho P, Hannemann R, Hackley SA. Vestigial auriculomotor activity indicates the direction of auditory attention in humans. eLife. 2020;9:e54536. doi:10.7554/eLife.54536
54. Rao SSC, Seaton K, Miller M, Brown K, Nygaard I, Stumbo P, Zimmerman B, Schulze K. Randomized controlled trial of biofeedback, sham feedback, and standard therapy for dyssynergic defecation. Clin Gastroenterol Hepatol. 2007;5(3):331–338. doi:10.1016/j.cgh.2006.12.023
55. Rao SSC, Patcharatrakul T. Diagnosis and treatment of dyssynergic defecation. J Neurogastroenterol Motil. 2016;22(3):423–435. https://www.jnmjournal.org/view.html?uid=1145&vmd=Full
56. Chiarioni G, Whitehead WE, Pezza V, Morelli A, Bassotti G. Biofeedback is superior to laxatives for normal transit constipation due to pelvic floor dyssynergia. Gastroenterology. 2006;130(3):657–664. PMID 16530506.
57. Enriquez-Geppert S, Huster RJ, Herrmann CS. EEG-neurofeedback as a tool to modulate cognition and behavior: a review tutorial. Front Hum Neurosci. 2017;11:51. doi:10.3389/fnhum.2017.00051
58. Sterman MB, Egner T. Foundation and practice of neurofeedback for the treatment of epilepsy. Appl Psychophysiol Biofeedback. 2006;31(1):21–35. doi:10.1007/s10484-006-9002-x
59. Kamiya J. Conscious control of brain waves. Psychology Today. 1968;1:56–60.
60. Alkoby O, Abu-Rmileh A, Shriki O, Todder D. Can we predict who will respond to neurofeedback? A review of the inefficacy problem and existing predictors for successful EEG neurofeedback learning. Neuroscience. 2018;378:155–164. doi:10.1016/j.neuroscience.2016.12.050
61. Cortese S, Ferrin M, Brandeis D, et al. Neurofeedback for attention-deficit/hyperactivity disorder: meta-analysis of clinical and neuropsychological outcomes from randomized controlled trials. J Am Acad Child Adolesc Psychiatry. 2016;55(6):444–455. doi:10.1016/j.jaac.2016.03.007
62. Westwood SJ, et al. Neurofeedback for attention-deficit/hyperactivity disorder: a systematic review and meta-analysis. JAMA Psychiatry. 2025;82(2):118–129. doi:10.1001/jamapsychiatry.2024.3702
63. Tan G, Thornby J, Hammond DC, et al. Meta-analysis of EEG biofeedback in treating epilepsy. Clin EEG Neurosci. 2009;40(3):173–179. doi:10.1177/155005940904000310
64. deCharms RC, Maeda F, Glover GH, et al. Control over brain activation and pain learned by using real-time functional MRI. Proc Natl Acad Sci USA. 2005;102(51):18626–18631. doi:10.1073/pnas.0505210102
65. Sulzer J, Haller S, Scharnowski F, et al. Real-time fMRI neurofeedback: progress and challenges. NeuroImage. 2013;76:386–399. doi:10.1016/j.neuroimage.2013.03.033
66. Thibault RT, Lifshitz M, Raz A. The self-regulating brain and neurofeedback: experimental science and clinical promise. Cortex. 2016;74:247–261. doi:10.1016/j.cortex.2015.10.024
67. Emmert K, et al. Comparison of anterior cingulate vs. insular cortex as targets for real-time fMRI regulation during pain stimulation. Front Behav Neurosci. 2014;8:350. doi:10.3389/fnbeh.2014.00350
68. Sitaram R, Ros T, Stoeckel L, et al. Closed-loop brain training: the science of neurofeedback. Nat Rev Neurosci. 2017;18(2):86–100. doi:10.1038/nrn.2016.164
69. Thibault RT, MacPherson A, Lifshitz M, Roth RR, Raz A. Neurofeedback with fMRI: a critical systematic review. NeuroImage. 2018;172:786–807. doi:10.1016/j.neuroimage.2017.12.071
70. Montgomery GH, DuHamel KN, Redd WH. A meta-analysis of hypnotically induced analgesia: how effective is hypnosis? Int J Clin Exp Hypn. 2000;48(2):138–153. doi:10.1080/00207140008410045
71. Thompson T, Terhune DB, Oram C, et al. The effectiveness of hypnosis for pain relief: a systematic review and meta-analysis of 85 controlled experimental trials. Neurosci Biobehav Rev. 2019;99:298–310. doi:10.1016/j.neubiorev.2019.02.013
72. Zeidan F, Martucci KT, Kraft RA, Gordon NS, McHaffie JG, Coghill RC. Brain mechanisms supporting the modulation of pain by mindfulness meditation. J Neurosci. 2011;31(14):5540–5548. doi:10.1523/JNEUROSCI.5791-10.2011
73. Zeidan F, Emerson NM, Farris SR, et al. Mindfulness meditation-based pain relief employs different neural mechanisms than placebo and sham mindfulness meditation-induced analgesia. J Neurosci. 2015;35(46):15307–15325. https://www.jneurosci.org/content/35/46/15307
74. Zeidan F, Adler-Neal AL, Wells RE, et al. Mindfulness-meditation-based pain relief is not mediated by endogenous opioids. J Neurosci. 2016;36(11):3391–3397. https://www.jneurosci.org/content/36/11/3391
75. Sharon H, Maron-Katz A, Ben Simon E, et al. Mindfulness meditation modulates pain through endogenous opioids. Am J Med. 2016;129(7):755–758. doi:10.1016/j.amjmed.2016.03.002
76. Khatib L, et al. The role of endogenous opioids in mindfulness and sham mindfulness-meditation for the direct alleviation of evoked chronic low back pain: a randomized clinical trial. Neuropsychopharmacology. 2024;49(7):1069–1077. doi:10.1038/s41386-023-01766-2
77. Levine JD, Gordon NC, Fields HL. The mechanism of placebo analgesia. Lancet. 1978;2(8091):654–657. doi:10.1016/S0140-6736(78)92762-9
78. Sauro MD, Greenberg RP. Endogenous opiates and the placebo effect: a meta-analytic review. J Psychosom Res. 2005;58(2):115–120. doi:10.1016/j.jpsychores.2004.07.001
79. Grevert P, Albert LH, Goldstein A. Partial antagonism of placebo analgesia by naloxone. Pain. 1983;16(2):129–143. doi:10.1016/0304-3959(83)90203-8
80. Goebel MU, Trebst AE, Steiner J, et al. Behavioral conditioning of immunosuppression is possible in humans. FASEB J. 2002;16(14):1869–1873. doi:10.1096/fj.02-0389com
81. Albring A, Wendt L, Benson S, et al. Placebo effects on the immune response in humans: the role of learning and expectation. PLoS ONE. 2012;7(11):e49477. doi:10.1371/journal.pone.0049477
82. Kirchhof J, et al. Learned immunosuppressive placebo responses in renal transplant patients. Proc Natl Acad Sci USA. 2018;115(16):4223–4227. doi:10.1073/pnas.1720548115
83. Farmer DGS, Patros M, Ottaviani MM, et al. Firing properties of single axons with cardiac rhythmicity in the human cervical vagus nerve. J Physiol. 2025;603(7):1941–1958. doi:10.1113/JP286423
84. Macefield VG, et al. Microelectrode recordings from the human cervical vagus nerve during maximal breath-holds. Exp Physiol. 2026;111(2):501–516. doi:10.1113/EP092890
85. Jacques C, Quiquempoix M, Sauvet F, Le Van Quyen M, Gomez-Merino D, Chennaoui M. Interest of neurofeedback training for cognitive performance and risk of brain disorders in the military context. Front Psychol. 2024;15:1412289. doi:10.3389/fpsyg.2024.1412289
86. Quer G, Gouda P, Galarnyk M, Topol EJ, Steinhubl SR. Inter- and intraindividual variability in daily resting heart rate and its associations with age, sex, sleep, BMI, and time of year: retrospective, longitudinal cohort study of 92,457 adults. PLoS ONE. 2020;15(2):e0227709. doi:10.1371/journal.pone.0227709
87. Wright JD, Hughes JP, Ostchega Y, Yoon SS, Nwankwo T. Mean systolic and diastolic blood pressure in adults aged 18 and over in the United States, 2001–2008. National Health Statistics Reports no. 35. Hyattsville, MD: National Center for Health Statistics; 2011. https://www.cdc.gov/nchs/data/nhsr/nhsr035.pdf
88. Geneva II, Cuzzo B, Fazili T, Javaid W. Normal body temperature: a systematic review. Open Forum Infect Dis. 2019;6(4):ofz032. doi:10.1093/ofid/ofz032
89. Uematsu S, Edwin DH, Jankel WR, Kozikowski J, Trattner M. Quantification of thermal asymmetry. Part 1: Normal values and reproducibility. J Neurosurg. 1988;69(4):552–555. doi:10.3171/jns.1988.69.4.0552
90. Gatt A, Mercieca C, Borg A, Grech A, Camilleri L, Gatt C, Chockalingam N, Formosa C. A comparison of thermographic characteristics of the hands and wrists of rheumatoid arthritis patients and healthy controls. Sci Rep. 2019;9:17204. doi:10.1038/s41598-019-53598-0
91. Schröder S, Chashchina E, Janunts E, Cayless A, Langenbucher A. Reproducibility and normal values of static pupil diameters. Eur J Ophthalmol. 2018;28(2):150–156. doi:10.5301/ejo.5001027
92. Shahnaz N, Ciocca V. Bayesian simulation of hearing thresholds at conventional and extended high frequencies in young adults. Hear Res. 2026;472:109547. doi:10.1016/j.heares.2026.109547
93. Lin IM, Tai LY, Fan SY. Breathing at a rate of 5.5 breaths per minute with equal inhalation-to-exhalation ratio increases heart rate variability. Int J Psychophysiol. 2014;91(3):206–211. doi:10.1016/j.ijpsycho.2013.12.006
94. Guinness World Records. First electronic communication between human nervous systems. https://www.guinnessworldrecords.com/world-records/101187-first-electronic-communication-between-human-nervous-systems
95. Warwick K. Project Cyborg 2.0. http://kevinwarwick.coventry.ac.uk/project-cyborg-2-0/ ; Atlas Obscura. Nervous system hookup leads to telepathic hand-holding. https://www.atlasobscura.com/articles/nervous-system-hookup-leads-to-telepathic-hand-holding
96. Reuters, via Yahoo News. Elon Musk's Neuralink says it has 21 participants enrolled in trials. January 2026. https://www.yahoo.com/news/articles/elon-musks-neuralink-says-21-183038116.html
97. Ha H, Gonzalez A. Migraine headache prophylaxis. Am Fam Physician. 2019;99(1):17–24.
98. Radboud University Nijmegen Medical Centre. Research on 'Iceman' Wim Hof suggests it may be possible to influence autonomic nervous system and immune response. Press release, 22 April 2011, via ScienceDaily. https://www.sciencedaily.com/releases/2011/04/110422090203.htm
