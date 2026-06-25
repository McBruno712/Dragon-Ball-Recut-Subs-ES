def rewrite_styles(styles: list[str]) -> list[str]:
    out: list[str] = []
    for line in styles:
        parts = line.split(",")
        if len(parts) >= 2 and parts[1].strip() == "Avenir Black":
            parts[1] = "Arial"
        out.append(",".join(parts))
    return out
