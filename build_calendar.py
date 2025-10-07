import csv
import os
from datetime import datetime, time
from typing import Optional, Tuple, List, Dict


INPUT_DIR = "Files"
INPUT_FILENAME = "Cópia de Alocação de Professores e Monitoras - ALOCAÇÕES.csv"
OUTPUT_FILENAME = "calendario_aulas.csv"


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    date_str = date_str.strip()
    # Expecting dd/mm/yyyy
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except Exception:
        return None


def parse_start_time(horario_str: str) -> Optional[time]:
    """Extract the first time (start) found in strings like:
    - "19H ÀS 21H30"
    - "9H30 ÀS 11H30"
    - "10H30 A 12H"
    - "10H ÀS 12H"
    Returns None if no recognizable time is found.
    """
    if not horario_str:
        return None
    s = horario_str.strip().upper()

    # Normalize common separators
    s = s.replace("ÀS", "AS").replace(" A ", " AS ")

    # Find first occurrence like 9H, 9H30, 10H, 10H15, etc.
    # Do a simple scan for patterns ending with 'H' optionally followed by two digits
    hour = None
    minute = 0
    token = ""
    for i, ch in enumerate(s):
        token += ch
        if ch == "H":
            # Look back to get hour digits
            left = token[:-1]
            # Trim non-digits at end
            while left and not left[-1].isdigit():
                left = left[:-1]
            # Collect continuous digits at the end
            digits = ""
            j = len(left) - 1
            while j >= 0 and left[j].isdigit():
                digits = left[j] + digits
                j -= 1
            if digits:
                try:
                    hour_val = int(digits)
                    # Check if minutes follow, e.g., H30
                    minute_val = 0
                    k = i + 1
                    if k + 1 < len(s) and s[k].isdigit() and s[k + 1].isdigit():
                        minute_val = int(s[k:k + 2])
                    if 0 <= hour_val <= 23 and 0 <= minute_val <= 59:
                        hour = hour_val
                        minute = minute_val
                        break
                except Exception:
                    pass
    if hour is None:
        return None
    try:
        return time(hour=hour, minute=minute)
    except Exception:
        return None


def read_rows(input_path: str) -> List[Dict[str, str]]:
    with open(input_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows: List[Dict[str, str]] = []
        for row in reader:
            rows.append(row)
    return rows


def select_and_transform(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # Column keys as present in the CSV (best-effort exact match)
    col_cliente = "CLIENTE"
    col_modulo = "MÓDULO"
    col_atividade = "ATIVIDADE"
    col_facilitador = "FACILITADOR"
    col_horario = "HORÁRIO"
    col_data = "DATA"
    col_monitor = "MONITOR(A)"

    results: List[Tuple[datetime, Optional[time], Dict[str, str]]] = []

    for row in rows:
        # Safely fetch values (handle missing keys or None)
        get = lambda k: (row.get(k) or "").strip()

        data_str = get(col_data)
        horario_str = get(col_horario)
        cliente = get(col_cliente)
        modulo = get(col_modulo)
        atividade = get(col_atividade)
        facilitador = get(col_facilitador)
        monitor = get(col_monitor)

        dt = parse_date(data_str)
        if not dt:
            # Skip rows without a valid date
            continue

        start_t = parse_start_time(horario_str)

        out_row = {
            "DATA": dt.strftime("%d/%m/%Y"),
            "HORÁRIO": horario_str,
            "CLIENTE": cliente,
            "MÓDULO": modulo,
            "AULA": atividade,
            "PROFESSOR": facilitador,
            "MONITORA": monitor,
            "LINK TRANSCRIÇÃO": "",
        }

        results.append((dt, start_t, out_row))

    # Sort by date then by start time (None times go last within the same date)
    def sort_key(item: Tuple[datetime, Optional[time], Dict[str, str]]):
        dt, start_t, _ = item
        return (dt, start_t or time(23, 59))

    results.sort(key=sort_key)

    # Return only the dict rows
    return [r[2] for r in results]


def write_output(output_path: str, rows: List[Dict[str, str]]):
    fieldnames = [
        "DATA",
        "HORÁRIO",
        "CLIENTE",
        "MÓDULO",
        "AULA",
        "PROFESSOR",
        "MONITORA",
        "LINK TRANSCRIÇÃO",
    ]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    input_path = os.path.join(INPUT_DIR, INPUT_FILENAME)
    output_path = os.path.join(INPUT_DIR, OUTPUT_FILENAME)

    rows = read_rows(input_path)
    selected = select_and_transform(rows)
    write_output(output_path, selected)


if __name__ == "__main__":
    main()


