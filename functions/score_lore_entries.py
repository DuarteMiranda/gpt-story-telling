def score_lore_entries(lore_entries: list[dict], keywords: list[str]) -> list[dict]:
    scored_entries = []

    for entry in lore_entries:
        score = 0

        # Normalize for matching
        tags = set(entry.get("tags", []))
        title = (entry.get("title") or "").lower()
        summary = (entry.get("summary") or "").lower()
        content = (entry.get("content") or "").lower()

        for kw in keywords:
            kw = kw.lower()

            # Tag match: strong signal
            if kw in tags:
                score += 5

            # Title / summary match: medium signal
            if kw in title:
                score += 2
            if kw in summary:
                score += 2

            # Content match: weak signal (optional)
            if kw in content:
                score += 1

        if score > 0:
            scored_entry = entry.copy()
            scored_entry["score"] = score
            scored_entries.append(scored_entry)

    # Sort by score descending
    return sorted(scored_entries, key=lambda x: x["score"], reverse=True)
