def source_code_location(event: Optional[_ProfilerEvent]):
    while event:
        if event.tag == _EventType.PyCall or event.tag == _EventType.PyCCall:
            assert isinstance(
                event.extra_fields, (_ExtraFields_PyCall, _ExtraFields_PyCCall)
            )
            if not event.extra_fields.caller.file_name.startswith("torch" + os.sep):
                return f"{event.extra_fields.caller.file_name}:{event.extra_fields.caller.line_number}"
        event = event.parent
    return "No source code location found"
