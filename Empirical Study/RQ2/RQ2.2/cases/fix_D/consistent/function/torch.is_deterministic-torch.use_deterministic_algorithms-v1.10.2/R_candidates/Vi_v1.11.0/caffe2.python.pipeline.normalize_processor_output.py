def normalize_processor_output(output):
    """
    Allow for processors to return results in several formats.
    TODO(azzolini): simplify once all processors use NetBuilder API.
    """
    if isinstance(output, Output):
        """ Processor returned an Output. """
        return output
    elif isinstance(output, Field):
        """ Processor returned a record. """
        return Output(record=output)
    elif isinstance(output, tuple):
        is_record_and_blob = (
            len(output) == 2 and
            isinstance(output[0], Field) and
            isinstance(output[1], core.BlobReference))
        if is_record_and_blob:
            """ Processor returned (record, stop_blob) """
            return Output(None, *output)
        else:
            """ Processor returned (nets, record, stop_blob) """
            return Output(*output)
    else:
        """ Processor returned nets, no output """
        return Output(output)
