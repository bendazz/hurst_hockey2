from typing import List
import csv

from models import Bio


def generate_bio_instances(csv_path: str = "players.csv") -> List[Bio]:
    """Read `csv_path` and return a list of `Bio` instances (not persisted).

    Fields are mapped from the CSV headers to the `Bio` model.
    """
    instances: List[Bio] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first = (row.get("First Name") or "").strip()
            last = (row.get("Last Name") or "").strip()

            num_raw = (row.get("Number") or "").strip()
            try:
                number = int(num_raw) if num_raw != "" else None
            except ValueError:
                number = None

            weight_raw = (row.get("Weight") or "").strip()
            try:
                weight = int(weight_raw) if weight_raw != "" else None
            except ValueError:
                weight = None

            bio = Bio(
                first_name=first,
                last_name=last,
                number=number,
                position=(row.get("Position") or None),
                height=(row.get("Height") or None),
                weight=weight,
                academic_class=(row.get("Class") or None),
                hometown=(row.get("Hometown") or None),
                high_school=(row.get("High School") or None),
            )
            instances.append(bio)

    return instances


__all__ = ["generate_bio_instances"]
