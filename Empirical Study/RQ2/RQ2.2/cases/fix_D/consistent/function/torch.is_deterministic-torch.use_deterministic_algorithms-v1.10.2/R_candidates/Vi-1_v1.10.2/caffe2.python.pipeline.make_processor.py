def make_processor(processor, reader=None):
    if processor is None:
        return lambda rec: rec
    elif isinstance(processor, core.Net):
        return NetProcessor(processor)
    else:
        if reader is not None and hasattr(processor, "schema_func"):
            def processor_schema():
                return processor.schema_func(reader)

            processor.schema = processor_schema
        return processor
