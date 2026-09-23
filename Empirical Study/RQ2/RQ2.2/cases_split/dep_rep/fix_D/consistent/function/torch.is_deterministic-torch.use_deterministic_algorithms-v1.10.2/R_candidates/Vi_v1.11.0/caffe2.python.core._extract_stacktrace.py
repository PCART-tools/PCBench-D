def _extract_stacktrace():
    '''
    This function extracts stacktrace without file system access
    by purely using sys._getframe() and removes part that belongs to
    this file (core.py). We are not using inspect module because
    its just a wrapper on top of sys._getframe() whose
    logic is based on accessing source files on disk - exactly what
    we are trying to avoid here. Same stands for traceback module

    The reason for file system access avoidance is that
    if code is located on an NFS, file access might be slow

    Function returns a list of tuples (file_name, line_number, function)
    '''

    result = []
    # Ignore top 3 layers of stack: this function, _CreateAndAddToSelf, and
    # whatever calls _CreateAndAddToSelf (either __getattr__ or Python)
    frame = sys._getframe(3)
    # We just go down the frame stack in a loop
    while frame:
        # Its important to extract information from the frame here
        # as frame's current line most probably will change later.
        result.append((frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name))
        frame = frame.f_back
    return result
