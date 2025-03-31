from pathlib import Path

LORE_FOLDER = Path("data/lore")

def load_lore_entries(lore_folder: str = "data/lore"):
    lore_entries = []
    global_tags = set()

    for file in LORE_FOLDER.glob("*.txt"):
        entry = {
            "file": file.name,
            "title": None,
            "tags": [],
            "summary": None,
            "content": ""
        }

        metadata_done = False
        content_lines = []

        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()

                if stripped.startswith("# Title:"):
                    entry["title"] = stripped.split(":", 1)[1].strip()
                elif stripped.lower().startswith("# tags:"):
                    tags = [tag.strip().lower() for tag in stripped.split(":", 1)[1].split(",")]
                    entry["tags"] = tags
                    global_tags.update(tags)
                elif stripped.lower().startswith("# summary:"):
                    entry["summary"] = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("#"):
                    continue  # other metadata fields, ignore
                else:
                    content_lines.append(line.rstrip())

        entry["content"] = "\n".join(content_lines).strip()
        lore_entries.append(entry)

    return lore_entries, global_tags