def pipe_and_output(
        input, output=None, num_threads=1, processor=None, name=None,
        capacity=None, group=None, num_runtime_threads=1, final_outputs=None):
    """
    Similar to `pipe`, with the additional ability for the pipe Task to
    return output values to the `Session` once done.

    Returns:
        Tuple (out_queue, *task_outputs)
            out_queue:    same as return value of `pipe`.
            task_outputs: TaskOutput object, fetchable from the client after
                          session.run() returns.
    """
    assert num_threads > 0
    result, task = _pipe_step(
        input, output, num_threads, processor, name, capacity, group,
        num_runtime_threads, final_outputs)
    output = None
    if final_outputs is not None:
        output = task.outputs()
        if type(final_outputs) not in (list, tuple):
            output = output[0]
    return result, output
