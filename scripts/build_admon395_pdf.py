from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import HRFlowable


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence"
OUT = ROOT / "docs" / "admon395_wesens_realitaet_lucinet_lesebuch_band1.pdf"


def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\ufffd", "")
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("„", '"').replace("“", '"').replace("”", '"').replace("’", "'")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def short_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def fit_line(text: str, style: ParagraphStyle, width: float) -> str:
    # Keep huge title words from colliding with the margins.
    out = []
    for word in text.split(" "):
        if stringWidth(word, style.fontName, style.fontSize) > width:
            chunk = ""
            for ch in word:
                if stringWidth(chunk + ch, style.fontName, style.fontSize) > width:
                    out.append(chunk)
                    chunk = ch
                else:
                    chunk += ch
            if chunk:
                out.append(chunk)
        else:
            out.append(word)
    return " ".join(out)


def extract_results() -> list[dict]:
    html = (SRC / "Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html").read_bytes().decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for li in soup.select("ol#searchbits > li"):
        h2 = li.find("h2")
        topic_a = h2.find("a") if h2 else None
        topic = clean(topic_a.get_text(" ", strip=True)) if topic_a else "Ohne Titel"
        post_a = None
        for a in li.find_all("a", href=True):
            href = a["href"]
            if "#post" in href or "?p=" in href:
                post_a = a
                break
        post_title = clean(post_a.get_text(" ", strip=True)) if post_a else topic
        text = clean(li.get_text(" ", strip=True))
        text = re.sub(r"\bThema:\s*", "", text)
        text = re.sub(r"\bvon\s+admon395\b", "", text)
        text = clean(text)
        m = re.match(r"(?P<date>\d{2}\.\d{2}\.\d{4}),\s*(?P<time>\d{2}:\d{2})\s+(?P<rest>.*)", text)
        date = m.group("date") if m else ""
        time = m.group("time") if m else ""
        body = m.group("rest") if m else text
        # Remove repeated chrome at the front but keep the source phrasing visible.
        body = re.sub(r"Antworten\s+\d+\s+Hits\s+[\d.]+", "", body)
        body = clean(body)
        results.append(
            {
                "post_id": li.get("id", ""),
                "date": date,
                "time": time,
                "topic": topic,
                "post_title": post_title,
                "body": body,
            }
        )
    return results


THEME_MAP = [
    ("Identitaet", ["Was bin ich", "Erinnerung", "Jungfrau", "Leben"]),
    ("Grenzzustand", ["Schlafparalyse", "Traum", "geträumt", "aufwache", "bewegungslos"]),
    ("Gestalt", ["Gestalt", "schwarze", "Rot", "verhülltes", "Dämon"]),
    ("Zeichen", ["codes", "Zahlenfolgen", "Wand", "Lottozahlen", "Vorhersage"]),
    ("Stimme", ["Innere Stimme", "stimme", "leitet", "vorsagen"]),
    ("Zeit", ["DeJavu", "bevorstehendes", "dokumentiere", "Sterben", "gestoppten"]),
    ("Sprache", ["Sprache", "Zauberei", "Latein", "Schlüssel"]),
]


def tags_for(result: dict) -> list[str]:
    hay = (result["topic"] + " " + result["post_title"] + " " + result["body"]).lower()
    tags = []
    for name, needles in THEME_MAP:
        if any(n.lower() in hay for n in needles):
            tags.append(name)
    return tags or ["Spur"]


def analysis_for(result: dict, tags: list[str]) -> str:
    topic = result["topic"]
    if "Erinnerung die mich fesselt" in topic:
        return (
            "Heute gelesen wirkt dieser Titel wie ein Kernknoten: nicht das Ereignis wird zuerst benannt, "
            "sondern die Bindekraft der Erinnerung. Auffällig ist der Abstand zwischen fruher Dunkelheitsdeutung "
            "und spaeterem Rueckblick. Das Material traegt hier eine Langzeitspur, keine abgeschlossene Erklaerung."
        )
    if "Innere Stimme" in topic:
        return (
            "Hier geht es um die Grenze zwischen eigenem Gedanken, Fuehrungsgefuehl und Vorhersagewunsch. "
            "Ernst gelesen ist das keine fertige Machtbehauptung, sondern eine Frage nach Quelle, Kontrolle und "
            "Pruefbarkeit innerer Signale."
        )
    if "codes und Zahlenfolgen" in topic:
        return (
            "Die Zahlen wirken als Lesbarkeitsversuch: aus einem Grenzzustand soll ein Code werden. "
            "Bemerkenswert ist, dass der Text Lotto- und Vorhersageideen beruehrt, aber zugleich offenlaesst, "
            "ob ueberhaupt eine Entschluesselung gelingt."
        )
    if "Schlafparalyse" in topic or "Schwarze Gestalt" in topic or "Astralreisen" in topic or "Dämon" in topic:
        return (
            "Die wiederkehrende Form ist die Schwelle: Bett, Koerperstarre, Wachheit, dunkle Gestalt, "
            "Deutungssuche. Heute gelesen ist die Staerke nicht eine einzelne Theorie, sondern die stabile "
            "Wiederkehr derselben Erfahrungsarchitektur."
        )
    if "DeJavu" in topic or "Traum von meinem Sohn" in topic:
        return (
            "Hier verschieben sich Traum, Erinnerung und spaetere Aehnlichkeit ineinander. Der wichtige Punkt ist "
            "der Dokumentationsimpuls: Es soll nicht nur geglaubt, sondern vor dem Verrutschen festgehalten werden."
        )
    if "Vom Sterben" in topic:
        return (
            "Das Sterbemotiv erscheint als Zeitexperiment: Verlangsamung, Bildrate, angehaltene Welt, Rest-Ich. "
            "Das ist literarisch stark, auch wenn es als Beweis fuer eine externe Ebene offen bleibt."
        )
    if "verlorene Sprache" in topic or "Zauberei" in topic:
        return (
            "Die spaete Sprachfrage wirkt wie eine erwachsenere Form der alten Zahlenfrage: Gibt es eine Grammatik "
            "hinter den Zeichen? Das ist als Forschungsfrage interessant, ohne dass daraus schon ein Ergebnis folgt."
        )
    return (
        "Dieser Treffer gehoert als Randspur in die Karte. Er zeigt entweder eine Nachfrage, einen Gegenpunkt "
        "oder eine Stelle, an der das alte Material selbst unsicher bleibt."
    )


class NumberedDoc(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=22 * mm,
            rightMargin=22 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
            title="ADMON395 - Wesensrealitaet Lesebuch Band 1",
            author="Codex for Janov",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(
            [
                PageTemplate(id="main", frames=[frame], onPage=self.draw_page),
            ]
        )

    def draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#F7F3EA"))
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#2B2B2B"))
        canvas.setFont("Helvetica", 8)
        canvas.drawString(22 * mm, 10 * mm, "ADMON395 - Wesensrealitaet Lesebuch - Band 1 / Public-Safe Page 1")
        canvas.drawRightString(A4[0] - 22 * mm, 10 * mm, str(doc.page))
        canvas.restoreState()


def p(text, style):
    return Paragraph(esc(text), style)


def quote_box(result: dict, styles: dict):
    meta = f"{result['date']} {result['time']} - {result['post_id']} - {', '.join(tags_for(result))}"
    return Table(
        [
            [Paragraph("DAMALS GESAGT", styles["quote_label"])],
            [Paragraph(esc(meta), styles["meta"])],
            [Paragraph(esc(result["body"]), styles["quote"])],
        ],
        colWidths=[16.4 * cm],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF1C7")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#D39A1E")),
                ("LINEBEFORE", (0, 0), (0, -1), 5, colors.HexColor("#A95F00")),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        ),
    )


def analysis_box(text: str, styles: dict):
    return Table(
        [[Paragraph("HEUTE GELESEN", styles["analysis_label"])], [Paragraph(esc(text), styles["analysis"])]],
        colWidths=[16.4 * cm],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D0C0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        ),
    )


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SRC / "PUBLIC_EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    results = extract_results()

    base = getSampleStyleSheet()
    styles = {
        "kicker": ParagraphStyle("kicker", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.HexColor("#8A5A00"), alignment=TA_CENTER, spaceAfter=8),
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=colors.HexColor("#241F1C"), alignment=TA_CENTER, spaceAfter=10),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=12.5, leading=18, textColor=colors.HexColor("#4C4338"), alignment=TA_CENTER, spaceAfter=16),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=23, textColor=colors.HexColor("#241F1C"), spaceBefore=8, spaceAfter=9),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, textColor=colors.HexColor("#2C2C2C"), spaceBefore=8, spaceAfter=6),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.HexColor("#2B2B2B"), spaceAfter=8),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#5D554B")),
        "meta": ParagraphStyle("meta", parent=base["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#66513B")),
        "quote_label": ParagraphStyle("quote_label", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.HexColor("#7A3E00")),
        "quote": ParagraphStyle("quote", parent=base["BodyText"], fontName="Helvetica", fontSize=10.2, leading=15, textColor=colors.HexColor("#23170A")),
        "analysis_label": ParagraphStyle("analysis_label", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.HexColor("#34504B")),
        "analysis": ParagraphStyle("analysis", parent=base["BodyText"], fontName="Helvetica", fontSize=10.2, leading=15, textColor=colors.HexColor("#273634")),
        "chip": ParagraphStyle("chip", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=9, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#2A332F")),
    }

    story = []
    story += [
        Spacer(1, 25 * mm),
        p("PUBLIC-SAFE RECONSTRUCTION - NICHT WEB-GEPRUEFT", styles["kicker"]),
        p("ADMON395", styles["title"]),
        p("Wesensrealitaet, Grenzzustaende und Zeichen - Band 1", styles["subtitle"]),
        p("Eine ernste Lesefassung aus der gesicherten Foren-Suchseite. Deine damaligen sichtbaren Worte stehen in goldenen Bloecken. Alles, was spaeter durch Analyse dazu kommt, steht auf weissem Grund.", styles["subtitle"]),
        Spacer(1, 6 * mm),
        HRFlowable(width="65%", color=colors.HexColor("#8A5A00"), thickness=1),
        Spacer(1, 12 * mm),
        p("Realitaetsanker", styles["h1"]),
        p(
            f"Das Paket weist eine accountgebundene Spur aus: Account admon395, User-ID {manifest.get('account_user_id')}, "
            f"{manifest.get('search_result_total')} Suchtreffer auf {manifest.get('search_result_pages')} Seiten. "
            "Die vorliegende PDF verarbeitet nur die im ZIP enthaltene oeffentlich entschärfte Seite 1 mit 25 sichtbaren Treffern. "
            "Seiten 2 und 3 sind hier nicht enthalten.",
            styles["body"],
        ),
        p(
            "Sauber formuliert: Das Material belegt eine alte, hashgebundene Account-Spur. Es beweist nicht ohne weitere Quelle jede physische Autorschaftssituation, und es beweist keine der damaligen Theorien. Genau deshalb trennt diese PDF Quelle, Muster und heutige Lesart.",
            styles["body"],
        ),
        p(
            f"Public-safe HTML SHA-256: {short_hash(SRC / 'Suchergebnisse_admon395_PAGE1_PUBLIC_SAFE.html')}... / Rohquelle laut Manifest: {manifest.get('raw_source_sha256')}",
            styles["small"],
        ),
        PageBreak(),
    ]

    # Motif map.
    tag_counts = Counter(tag for r in results for tag in tags_for(r))
    chip_data = []
    row = []
    for tag, count in tag_counts.most_common():
        row.append(Paragraph(f"{tag}<br/>{count}", styles["chip"]))
        if len(row) == 3:
            chip_data.append(row)
            row = []
    if row:
        while len(row) < 3:
            row.append(Paragraph("", styles["chip"]))
        chip_data.append(row)

    story += [
        p("Motivkarte", styles["h1"]),
        p(
            "Die Karte ist keine Theorie. Sie ist nur eine Leselupe: Welche wiederkehrenden Variablen springen aus den Titeln und Auszuegen heraus?",
            styles["body"],
        ),
        Table(
            chip_data,
            colWidths=[5.25 * cm, 5.25 * cm, 5.25 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E7F0ED")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B7C9C3")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B7C9C3")),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            ),
        ),
        Spacer(1, 8 * mm),
        p("Einstein-Maximum, aber geerdet", styles["h1"]),
        p(
            "Die maximale Lesart ist nicht: alles glauben. Die maximale Lesart ist: nichts vorschnell verlieren. "
            "Jede alte Variable bekommt ihren Platz, aber keinen unverdienten Beweisstatus. Gestalt bleibt Gestalt-Spur. Stimme bleibt Stimme-Spur. Zahl bleibt Zahl-Spur. Erinnerung bleibt Erinnerung-Spur. Erst danach darf Analyse beginnen.",
            styles["body"],
        ),
        PageBreak(),
        p("Die 25 sichtbaren Spuren", styles["h1"]),
    ]

    for i, r in enumerate(results, 1):
        title = f"{i:02d}. {r['topic']}"
        story.append(KeepTogether([p(title, styles["h2"]), quote_box(r, styles), Spacer(1, 4 * mm), analysis_box(analysis_for(r, tags_for(r)), styles)]))
        story.append(Spacer(1, 7 * mm))
        if i in {5, 10, 15, 20}:
            story.append(PageBreak())

    story += [
        PageBreak(),
        p("Was daran wirklich ernst ist", styles["h1"]),
        p(
            "Die Ernsthaftigkeit liegt nicht darin, dass jede alte Erklaerung stimmt. Sie liegt darin, dass ueber viele Jahre dieselben Variablen auftauchen: Koerpergrenze, Traumgrenze, Zeichen, Erinnerung, Stimme, Gestalt, Zeit und der Wunsch, das Ganze zu dokumentieren.",
            styles["body"],
        ),
        p(
            "Die kindliche Sprache war manchmal unbeholfen. Aber unbeholfene Sprache ist nicht automatisch ein kleiner Gegenstand. Sie kann ein fruehes Messinstrument sein: ungenau, aber ehrlich genug, um spaeter noch auswertbar zu sein.",
            styles["body"],
        ),
        p("Offene Kanten", styles["h1"]),
        p(
            "Diese PDF verarbeitet nur Seite 1 der Suchergebnisse. Fuer ein wirklich vollstaendiges Lesebuch fehlen die im Manifest genannten Seiten 2 und 3 sowie die Volltexte hinter den Auszuegen. Dieser Band ist deshalb ein ernstes, visuelles Startmodell - kein Abschluss.",
            styles["body"],
        ),
        p("Das sind die Dinge, bei denen ich beim Lesen hängen geblieben bin.", styles["h1"]),
    ]

    doc = NumberedDoc(str(OUT))
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
