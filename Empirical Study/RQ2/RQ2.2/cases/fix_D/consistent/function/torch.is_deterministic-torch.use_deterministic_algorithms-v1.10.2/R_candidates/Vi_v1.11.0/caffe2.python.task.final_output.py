def final_output(blob_or_record):
    """
    Adds an output to the current Task, or if no task is active,
    create a dummy task that returns the given blob or record
    to the client. This will return the value of the blob or record when
    the last task of the TaskGroup for a given node finishes.
    """
    cur_task = Task.current(required=False) or Task()
    return cur_task.add_output(blob_or_record)
