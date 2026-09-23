def source_code_location(event):
    while event is not None:
        match = re.search(r"\.py\(.*\)", event.name)
        if match is None:
            event = event.parent
            continue
        return event.name
    return "No source code location found"
