import json
from pathlib import Path

from app.models import Assessment


CATALOG_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "shl_catalog.json"
)


def normalize_bool(value: str) -> bool:
    return str(value).strip().lower() == "yes"


def load_catalog():

    with open(CATALOG_PATH, "rb") as f:
        raw_bytes = f.read()

    raw_text = raw_bytes.decode(
        "utf-8",
        errors="ignore"
    )

    cleaned_text = "".join(
        ch for ch in raw_text
        if ord(ch) >= 32 or ch in "\n\r\t"
    )

    raw_data = json.loads(cleaned_text)

    catalog = []

    for item in raw_data:

        assessment = Assessment(
            entity_id=str(item.get("entity_id", "")),
            name=item.get("name", "").strip(),
            url=item.get("link", "").strip(),
            description=item.get("description", "").strip(),

            job_levels=item.get("job_levels", []),
            languages=item.get("languages", []),

            duration=item.get("duration", "").strip(),

            remote=normalize_bool(item.get("remote", "no")),
            adaptive=normalize_bool(item.get("adaptive", "no")),

            categories=item.get("keys", [])
        )

        catalog.append(assessment)

    return catalog