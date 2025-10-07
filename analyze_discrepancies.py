import csv
import os
import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple


CALENDAR_PATH = os.path.join("Files", "calendario_aulas.csv")
TRANSCRIPTS_DIR = os.path.join("output")
REPORT_PATH = os.path.join("Files", "discrepancias.csv")


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    s = value.strip().lower()
    # remove accents lightly via regex fallback
    replacements = {
        "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "ô": "o", "õ": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
    }
    for a, b in replacements.items():
        s = s.replace(a, b)
    return s


def read_calendar_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def list_transcript_files(dir_path: str) -> List[str]:
    files: List[str] = []
    for name in os.listdir(dir_path):
        if name.lower().endswith(".txt"):
            files.append(os.path.join(dir_path, name))
    return files


def build_filename_index(files: List[str]) -> List[Tuple[str, str]]:
    indexed: List[Tuple[str, str]] = []
    for fp in files:
        base = os.path.basename(fp)
        indexed.append((fp, normalize_text(base)))
    return indexed


def tokenize(text: str) -> List[str]:
    return re.findall(r"[\w\-]+", text.lower())


def choose_best_match(calendar_row: Dict[str, str], candidates: List[Tuple[str, str]]) -> Optional[str]:
    # Score by presence of key tokens from CLIENTE, MÓDULO, AULA and professor surname in filename
    cliente = normalize_text(calendar_row.get("CLIENTE", ""))
    modulo = normalize_text(calendar_row.get("MÓDULO", ""))
    aula = normalize_text(calendar_row.get("AULA", ""))
    professor = normalize_text(calendar_row.get("PROFESSOR", ""))

    keywords: List[str] = []
    # split by separators and keep alnum tokens >=3
    for field in (cliente, modulo, aula):
        for tok in tokenize(field):
            if len(tok) >= 3:
                keywords.append(tok)
    # professor surname(s)
    prof_parts = [p for p in tokenize(professor) if len(p) >= 3]
    if prof_parts:
        # weight surnames later
        pass

    best_fp: Optional[str] = None
    best_score = 0

    for fp, norm_name in candidates:
        score = 0
        for kw in keywords:
            if kw in norm_name:
                score += 2
        # professor name tokens higher weight
        for p in prof_parts:
            if p in norm_name:
                score += 3
        # small bonus for date token when present (dd/mm/yyyy -> dd or mm names not present in filenames)
        # Many filenames contain client/module more than date; skip date scoring.
        if score > best_score:
            best_score = score
            best_fp = fp

    return best_fp


SPEAKER_LINE_RE = re.compile(r"^([^:]{1,100}):\s")


def infer_main_speaker(file_path: str) -> Optional[str]:
    # Strategy:
    # 1) Count explicit "Name: text" speaker tags if present
    # 2) Fallback: detect most repeated capitalized name appearing as tag-like or in lines
    speaker_counts: Counter[str] = Counter()

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                m = SPEAKER_LINE_RE.match(line_stripped)
                if m:
                    name = m.group(1).strip()
                    # sanitize very long or placeholder names (e.g., None)
                    if 1 <= len(name) <= 60 and name.lower() not in ("none", "desconhecido", "speaker"):
                        speaker_counts[name] += 1
    except Exception:
        return None

    if speaker_counts:
        # return most frequent speaker tag
        return speaker_counts.most_common(1)[0][0]

    # Fallback heuristic: scan first 3000 lines for capitalized tokens repeated often
    name_like_counts: Counter[str] = Counter()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i > 3000:
                    break
                # capture tokens with initial capital and length >= 3
                for token in re.findall(r"\b[A-ZÁÂÃÀÄÉÊÈËÍÎÌÏÓÔÕÒÖÚÛÙÜÇ][a-záâãàäéêèëíîìïóôõòöúûùüç]{2,}(?:\s+[A-ZÁÂÃÀÄÉÊÈËÍÎÌÏÓÔÕÒÖÚÛÙÜÇ][a-záâãàäéêèëíîìïóôõòöúûùüç]{2,}){0,2}", line):
                    # Limit to up to 3 words to avoid sentences
                    cleaned = token.strip()
                    if len(cleaned) <= 60:
                        name_like_counts[cleaned] += 1
    except Exception:
        return None

    if not name_like_counts:
        return None

    return name_like_counts.most_common(1)[0][0]


def normalize_person_name(name: str) -> str:
    # keep full normalized for comparison and a simplified surname as backup
    return normalize_text(name)


def is_name_match(expected: str, detected: str) -> bool:
    if not expected or not detected:
        return False
    ne = normalize_person_name(expected)
    nd = normalize_person_name(detected)
    if not ne or not nd:
        return False
    if ne in nd or nd in ne:
        return True
    # match by any surname token (length >=3)
    e_tokens = [t for t in tokenize(ne) if len(t) >= 3]
    d_tokens = [t for t in tokenize(nd) if len(t) >= 3]
    return any(t in d_tokens for t in e_tokens)


def analyze() -> List[Dict[str, str]]:
    calendar_rows = read_calendar_rows(CALENDAR_PATH)
    transcript_files = list_transcript_files(TRANSCRIPTS_DIR)
    idx = build_filename_index(transcript_files)

    discrepancies: List[Dict[str, str]] = []

    for row in calendar_rows:
        expected_prof = (row.get("PROFESSOR") or "").strip()
        if not expected_prof:
            continue

        match_fp = choose_best_match(row, idx)
        if not match_fp:
            # no file matched; flag as discrepancy because we cannot validate
            discrepancies.append({
                "DATA": row.get("DATA", ""),
                "HORÁRIO": row.get("HORÁRIO", ""),
                "CLIENTE": row.get("CLIENTE", ""),
                "MÓDULO": row.get("MÓDULO", ""),
                "AULA": row.get("AULA", ""),
                "PROFESSOR (PLANEJADO)": expected_prof,
                "ARQUIVO": "(não encontrado)",
                "PROFESSOR (DETECTADO)": "(indisponível)",
                "OBS": "Transcrição correspondente não encontrada pelo nome do arquivo",
            })
            continue

        detected = infer_main_speaker(match_fp)
        if not detected:
            discrepancies.append({
                "DATA": row.get("DATA", ""),
                "HORÁRIO": row.get("HORÁRIO", ""),
                "CLIENTE": row.get("CLIENTE", ""),
                "MÓDULO": row.get("MÓDULO", ""),
                "AULA": row.get("AULA", ""),
                "PROFESSOR (PLANEJADO)": expected_prof,
                "ARQUIVO": os.path.basename(match_fp),
                "PROFESSOR (DETECTADO)": "(não identificado)",
                "OBS": "Não consegui identificar o principal falante",
            })
            continue

        if not is_name_match(expected_prof, detected):
            discrepancies.append({
                "DATA": row.get("DATA", ""),
                "HORÁRIO": row.get("HORÁRIO", ""),
                "CLIENTE": row.get("CLIENTE", ""),
                "MÓDULO": row.get("MÓDULO", ""),
                "AULA": row.get("AULA", ""),
                "PROFESSOR (PLANEJADO)": expected_prof,
                "ARQUIVO": os.path.basename(match_fp),
                "PROFESSOR (DETECTADO)": detected,
                "OBS": "Professor detectado diferente do planejado",
            })

    return discrepancies


def write_report(rows: List[Dict[str, str]], path: str) -> None:
    fieldnames = [
        "DATA",
        "HORÁRIO",
        "CLIENTE",
        "MÓDULO",
        "AULA",
        "PROFESSOR (PLANEJADO)",
        "ARQUIVO",
        "PROFESSOR (DETECTADO)",
        "OBS",
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    discrepancies = analyze()
    write_report(discrepancies, REPORT_PATH)
    print(f"Gerado relatório: {REPORT_PATH} ({len(discrepancies)} discrepâncias)")


if __name__ == "__main__":
    main()


