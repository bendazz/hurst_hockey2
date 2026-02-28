from typing import List, Optional
import csv

from models import Stats


def _int(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    s = val.strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _float(val: Optional[str]) -> Optional[float]:
    if val is None:
        return None
    s = val.strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def generate_stats_instances(csv_path: str = "stats.csv") -> List[Stats]:
    """Read `csv_path` and return a list of `Stats` instances (not persisted)."""
    instances: List[Stats] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first = (row.get("First_name") or row.get("First Name") or "").strip()
            last = (row.get("Last_name") or row.get("Last Name") or "").strip()

            number_raw = (row.get("Number") or "").strip()
            # keep as string when not purely numeric (e.g., 'TM') to match model Optional[str]
            number = number_raw if number_raw != "" else None

            stats = Stats(
                first_name=first,
                last_name=last,
                number=number,
                GP=_int(row.get("GP")),
                G=_int(row.get("G")),
                A=_int(row.get("A")),
                PTS=_int(row.get("PTS")),
                SH=_int(row.get("SH")),
                SH_PCT=_float(row.get("SH_PCT")),
                Plus_Minus=_int(row.get("Plus_Minus")),
                PPG=_int(row.get("PPG")),
                SHG=_int(row.get("SHG")),
                FG=_int(row.get("FG")),
                GWG=_int(row.get("GWG")),
                GTG=_int(row.get("GTG")),
                OTG=_int(row.get("OTG")),
                HTG=_int(row.get("HTG")),
                UAG=_int(row.get("UAG")),
                PN_PIM=(row.get("PN-PIM") or row.get("PN_PIM") or None),
                MIN=_int(row.get("MIN")),
                MAJ=_int(row.get("MAJ")),
                OTH=_int(row.get("OTH")),
                BLK=_int(row.get("BLK")),
            )
            instances.append(stats)

    return instances


__all__ = ["generate_stats_instances"]
