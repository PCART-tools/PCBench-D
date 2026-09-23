def _pipe_step(
        input, output=None, num_threads=1, processor=None, name=None,
        capacity=None, group=None, num_runtime_threads=None, final_outputs=None):
    """
    """
    assert num_threads <= 1 or num_runtime_threads <= 1, (
        'Only one of num_threads or num_runtime_threads must be set.')

    if isinstance(input, Reader):
        reader = input
    elif hasattr(input, 'reader'):
        reader = input.reader()
    else:
        raise ValueError(
            'Input must be a reader, queue or stream. Got {}'.format(type(input)))

    if processor is not None:
        reader = ProcessingReader(reader, processor)

    if num_threads == 0 or num_runtime_threads == 0:
        assert output is None
        return reader, None

    if name is None and processor is not None:
        name = processor_name(processor)
    if name is None and output is not None:
        name = 'pipe_into:%s' % processor_name(output)
    if name is None:
        name = 'pipe_from:%s' % processor_name(input)

    if num_threads > 1:
        return _static_threads_task(
            name, group, final_outputs, reader, num_threads, output, capacity)
    else:
        return _runtime_threads_task(
            name, group, final_outputs, reader, num_runtime_threads, output,
            capacity)
