def pipe(
        input, output=None, num_threads=1, processor=None, name=None,
        capacity=None, group=None, num_runtime_threads=1):
    """
    Given a Reader, Queue or DataStream in `input`, and optionally, a Writer,
    Queue or DataStream in `output`, creates a Task that, when run, will
    pipe the input into the output, using multiple parallel threads.
    Additionally, if a processor is given, it will be called between reading
    and writing steps, allowing it to transform the record.

    Args:
        input:       either a Reader, Queue or DataStream that will be read
                     until a stop is signaled either by the reader or the
                     writer.
        output:      either a Writer, a Queue or a DataStream that will be
                     written to as long as neither reader nor writer signal
                     a stop condition. If output is not provided or is None,
                     a Queue is created with given `capacity` and written to.
        num_threads: number of concurrent threads used for processing and
                     piping. If set to 0, no Task is created, and a
                     reader is returned instead -- the reader returned will
                     read from the reader passed in and process it.
                     ** DEPRECATED **. Use `num_runtime_threads` instead.
                     This option will be removed once all readers/processors
                     support `num_runtime_threads`.
        processor:   (optional) function that takes an input record and
                     optionally returns a record; this will be called
                     between read and write steps. If the processor does
                     not return a record, a writer will not be instantiated.
                     Processor can also be a core.Net with input and output
                     records properly set. In that case, a NetProcessor is
                     instantiated, cloning the net for each of the threads.
        name:        (optional) name of the task to be created.
        capacity:    when output is not passed, a queue of given `capacity`
                     is created and written to.
        group:       (optional) explicitly add the created Task to this
                     TaskGroup, instead of using the currently active one.
        num_runtime_threads: Similar to `num_threads`, but instead of expanding
                     the tasks with a `for` loop in python, does that at
                     runtime. This is preferable to `num_threads`, but some
                     processors/readers still require to be called multiple
                     times in python.

    Returns:
        Output Queue, DataStream, Reader, or None, depending on the parameters
        passed.
    """
    result, _ = _pipe_step(
        input, output, num_threads, processor, name, capacity, group,
        num_runtime_threads)
    return result
