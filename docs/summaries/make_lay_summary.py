"""One-page plain-language summary of the pilot evidence map (Voluntary Body Control Research Project).

Every number below is taken from docs/research-project.md (export of 3 October 2026) in the
research repository; line references are in the comments next to each figure.
"""
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = sys.argv[1]
SCALE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Sans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", FONT_DIR + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", FONT_DIR + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic", boldItalic="Sans-BoldItalic")

INK = colors.HexColor("#1B1B1B")
MUTED = colors.HexColor("#555B63")
ACCENT = colors.HexColor("#1F5FA8")
RULE = colors.HexColor("#C9CED5")
HEAD_BG = colors.HexColor("#EEF2F7")
WARN_BG = colors.HexColor("#FFF4E0")
WARN_LINE = colors.HexColor("#D9A441")


WIDTH = 7.2 * inch - 12  # the frame width less its default 6 pt padding on each side


def s(v):
    return v * SCALE


title = ParagraphStyle("title", fontName="Sans-Bold", fontSize=s(17), leading=s(20.5), textColor=INK, spaceAfter=s(2))
subtitle = ParagraphStyle("subtitle", fontName="Sans", fontSize=s(8.8), leading=s(11), textColor=MUTED, spaceAfter=s(7))
label = ParagraphStyle("label", fontName="Sans", fontSize=s(8.4), leading=s(10.8), textColor=INK)
lead = ParagraphStyle("lead", fontName="Sans-Bold", fontSize=s(11), leading=s(14.2), textColor=INK, spaceBefore=s(8), spaceAfter=s(2))
h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=s(10.4), leading=s(13), textColor=ACCENT, spaceBefore=s(8), spaceAfter=s(3))
body = ParagraphStyle("body", fontName="Sans", fontSize=s(9.1), leading=s(11.9), textColor=INK, alignment=TA_LEFT)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=s(11), bulletIndent=s(1), spaceAfter=s(3.2))
cell = ParagraphStyle("cell", fontName="Sans", fontSize=s(8.2), leading=s(10.1), textColor=INK)
cell_head = ParagraphStyle("cell_head", parent=cell, fontName="Sans-Bold")
note = ParagraphStyle("note", fontName="Sans-Italic", fontSize=s(7.7), leading=s(9.8), textColor=MUTED, spaceBefore=s(3))
footer = ParagraphStyle("footer", fontName="Sans", fontSize=s(7.4), leading=s(9.4), textColor=MUTED)

story = []
story.append(Paragraph("Controlling ‘automatic’ body functions:<br/>what the pilot evidence shows", title))
story.append(Paragraph("Plain-language summary · Voluntary Body Control Research Project · 4 October 2026", subtitle))

warning = Table(
    [[Paragraph(
        "<b>Preliminary — not for citation.</b> This summarises the project’s pilot evidence map of "
        "3 October 2026, compiled with the help of an AI assistant (Claude). Its numbers have not yet been "
        "independently re-checked, and the project’s registered systematic review will replace it.", label)]],
    colWidths=[WIDTH], hAlign="LEFT",
)
warning.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), WARN_BG),
    ("BOX", (0, 0), (-1, -1), 0.8, WARN_LINE),
    ("LEFTPADDING", (0, 0), (-1, -1), s(7)), ("RIGHTPADDING", (0, 0), (-1, -1), s(7)),
    ("TOPPADDING", (0, 0), (-1, -1), s(5)), ("BOTTOMPADDING", (0, 0), (-1, -1), s(5.5)),
]))
story.append(warning)

# Summary, lines 7 and 9: "at least 20 features"; strength vs certainty and prevalence.
story.append(Paragraph(
    "People can deliberately change more than 20 body functions usually thought of as automatic. "
    "But the most dramatic changes come from the fewest people and the weakest evidence.", lead))

story.append(Paragraph("What the pilot found", h2))
findings = [
    # Line 9: 26 abilities, ten High certainty. data/evidence.csv, lever column: 7 of the 10 work through a lever;
    # tensor_tympani, nystagmus and ear_muscles are 'Direct' (line 94: "no lever at all"). Line 9's claim that
    # every High-certainty ability works through a lever contradicts the dataset, so it is not repeated here.
    "<b>Most proven control works through a ‘lever’.</b> Ten of the 26 abilities reviewed reach the "
    "highest evidence level. Seven of the ten work through breathing, imagined movement, hypnotic suggestion, or "
    "a live readout of a body signal (biofeedback). The other three are small muscles, in the middle ear, in the "
    "eye and on the outer ear, that a minority of people can work directly, with no lever.",
    # Lines 9, 58, 158: n = 11, rho -0.60 and -0.81; best individuals vs group means.
    "<b>The bigger the change, the weaker the proof.</b> Across the 11 abilities whose effect could be put on a "
    "common scale, larger effects came with weaker evidence and with fewer people able to do them (rank "
    "correlations of −0.60 and −0.81). Part of this is how studies report: dramatic results are often one "
    "person’s best attempt, while well-proven results are group averages.",
    # Line 108: Roddiger 2021, 83 of 192 (43.2%); Wickens 2017, 5 people, +22 dB at 250 Hz.
    "<b>One exception stands out.</b> About 4 in 10 people can tense a tiny muscle inside the middle ear on "
    "purpose, often heard as a rumble (83 of 192 people surveyed, 43%). In 5 people tested, while the muscle was "
    "tensed a low tone (250 Hz) had to be 22 decibels louder before they could hear it. It needs no lever, it is "
    "common, and its effect is large and measured with instruments.",
    # Lines 72, 146: stopping the heart not supported; no unaided mind-to-mind link.
    "<b>Some claims fail.</b> No one has been shown to stop their own heart, and there is no documented case of "
    "one person’s mind directly affecting another person’s nerves without implanted or external equipment.",
]
for f in findings:
    story.append(Paragraph(f, bullet, bulletText="•"))

story.append(Paragraph("Examples from the evidence map", h2))
rows = [
    ["Ability", "What was shown", "Who", "How sure"],
    # Line 108.
    ["Middle-ear muscle (‘ear rumble’)", "Hearing threshold for a low tone raised 22 dB during contraction",
     "About 4 in 10 people (43% of 192 surveyed)", "High"],
    # Line 98: Paravlic 2018, 13 studies, 370 participants.
    ["Strength from imagined contractions", "Strength gains from practice without moving (13 studies pooled)",
     "Healthy adults, with training", "High"],
    # Line 126: Montgomery 2000, d 0.67; 1.16 high, -0.01 low suggestibility.
    ["Pain relief by hypnosis", "Less pain on average; much more in highly suggestible people, almost none in the least",
     "Most people, scaling with suggestibility", "High"],
    # Line 68: Brook 2013, about 4 mmHg net of placebo, Class IIa.
    ["Slow, guided breathing", "Systolic blood pressure about 4 mmHg lower, beyond the placebo effect",
     "Adults with high blood pressure", "Moderate"],
    # Line 88: Zwaag 2022, IL-6 -35% with combined training; one research group.
    ["Breathing technique and inflammation", "Lower inflammatory signals in a controlled lab challenge (IL-6 about 35% lower)",
     "Trained volunteers; one research group", "Moderate"],
    # Line 82: Kozhevnikov 2013, largest rise 2.2 degC among ten experts.
    ["Core temperature in g-Tummo meditation", "Armpit temperature up 2.2 °C (the best of 10 people)",
     "Expert meditators", "Low"],
    # Line 74: Green & Green 1977, ~300 bpm for ~17 s, book account.
    ["Heart-rate surge", "About 300 beats per minute for about 17 seconds",
     "One person; a book account, not peer-reviewed", "Low"],
    # Line 72: Wenger 1961; not supported.
    ["Stopping the heart", "Not achieved; the heart kept beating", "No one", "Not supported"],
]
data = [[Paragraph(c, cell_head) for c in rows[0]]] + [[Paragraph(c, cell) for c in r] for r in rows[1:]]
table = Table(data, colWidths=[WIDTH * f for f in (0.225, 0.386, 0.267, 0.122)], repeatRows=1, hAlign="LEFT")
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
    ("LINEBELOW", (0, 0), (-1, 0), 0.8, RULE),
    ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), s(4)), ("RIGHTPADDING", (0, 0), (-1, -1), s(4)),
    ("TOPPADDING", (0, 0), (-1, -1), s(2.6)), ("BOTTOMPADDING", (0, 0), (-1, -1), s(3)),
]))
story.append(table)
# Lines 27-32: the certainty rubric.
story.append(Paragraph(
    "How sure, by the project’s rubric: High = measured with instruments, repeated by independent groups or pooled "
    "in a meta-analysis, with a known mechanism. Moderate = measured in controlled studies, but small samples or "
    "mostly one research group. Low = one study, a handful of people, or not peer-reviewed. Not supported = tested "
    "and not shown.", note))

story.append(Paragraph("What this does not show", h2))
caveats = [
    # Line 166: 72 of 98 read in primary; 26 partly secondary.
    "<b>It is a pilot.</b> 26 of its 98 sources were read only through secondary accounts, citation records or "
    "abstracts, and no number has yet been checked by a second, independent extractor.",
    # Line 27: certainty asks whether the control exists, not clinical usefulness.
    "<b>It asks whether the control exists, not whether it helps.</b> Health benefits, and whether anything is "
    "safe to try, are separate questions.",
    # Line 158: two built-in biases; direction more trustworthy than the coefficient.
    "<b>The headline pattern is exaggerated</b> by setting one person’s best attempt beside group averages; "
    "its direction is more trustworthy than its exact size.",
]
for c in caveats:
    story.append(Paragraph(c, bullet, bulletText="•"))

story.append(Paragraph("What happens next", h2))
story.append(Paragraph(
    "A registered systematic review will re-extract every ability under rules fixed in advance, with two "
    "independent extractors, human sign-off and every number traced to its source. Its results, not this pilot, "
    "are what the project will report.", body))

story.append(Spacer(1, s(6)))
story.append(Paragraph(
    "Source: Voluntary Body Control Research Project, pilot evidence map (export of 3 October 2026, "
    "docs/research-project.md in the private project repository). Program lead: Sean Borycki. "
    "Prepared 4 October 2026.", footer))

doc = SimpleDocTemplate(
    OUT, pagesize=letter,
    leftMargin=0.65 * inch, rightMargin=0.65 * inch, topMargin=0.55 * inch, bottomMargin=0.5 * inch,
    title="Controlling automatic body functions: what the pilot evidence shows",
    author="Voluntary Body Control Research Project (Sean Borycki)",
    subject="Plain-language summary of the pilot evidence map; preliminary, not for citation",
    creator="Drafted with Claude",
)
doc.build(story)
