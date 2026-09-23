def warning_text(name, amb):
    """The text for ambiguity warnings"""
    text = f"\nAmbiguities exist in dispatched function {name}\n\n"
    text += "The following signatures may result in ambiguous behavior:\n"
    for pair in amb:
        text += "\t" + ", ".join("[" + str_signature(s) + "]" for s in pair) + "\n"
    text += "\n\nConsider making the following additions:\n\n"
    text += "\n\n".join(
        [
            "@dispatch(" + str_signature(super_signature(s)) + f")\ndef {name}(...)"
            for s in amb
        ]
    )
    return text
