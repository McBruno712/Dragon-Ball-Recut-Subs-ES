class ValidationError(RuntimeError):
    pass


def validate(original, translated) -> None:
    if len(original.events) != len(translated.events):
        raise ValidationError(
            f"Event count mismatch: {len(original.events)} vs {len(translated.events)}"
        )
    for i, (o, t) in enumerate(zip(original.events, translated.events)):
        if o.start != t.start or o.end != t.end:
            raise ValidationError(
                f"Timestamp mismatch at line {i}: "
                f"({o.start},{o.end}) vs ({t.start},{t.end})"
            )
        for field in ("style", "effect", "marginl", "marginr", "marginv", "name"):
            if getattr(o, field, None) != getattr(t, field, None):
                raise ValidationError(
                    f"Field '{field}' changed at line {i}: "
                    f"{getattr(o, field, None)!r} vs {getattr(t, field, None)!r}"
                )
