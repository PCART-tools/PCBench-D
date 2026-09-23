def blit(photoimage, aggimage, offsets, bbox=None):
    """
    Blit *aggimage* to *photoimage*.

    *offsets* is a tuple describing how to fill the ``offset`` field of the
    ``Tk_PhotoImageBlock`` struct: it should be (0, 1, 2, 3) for RGBA8888 data,
    (2, 1, 0, 3) for little-endian ARBG32 (i.e. GBRA8888) data and (1, 2, 3, 0)
    for big-endian ARGB32 (i.e. ARGB8888) data.

    If *bbox* is passed, it defines the region that gets blitted. That region
    will NOT be blanked before blitting.

    Tcl events must be dispatched to trigger a blit from a non-Tcl thread.
    """
    data = np.asarray(aggimage)
    height, width = data.shape[:2]
    dataptr = (height, width, data.ctypes.data)
    if bbox is not None:
        (x1, y1), (x2, y2) = bbox.__array__()
        x1 = max(math.floor(x1), 0)
        x2 = min(math.ceil(x2), width)
        y1 = max(math.floor(y1), 0)
        y2 = min(math.ceil(y2), height)
        bboxptr = (x1, x2, y1, y2)
        blank = False
    else:
        bboxptr = (0, width, 0, height)
        blank = True

    # NOTE: _tkagg.blit is thread unsafe and will crash the process if called
    # from a thread (GH#13293). Instead of blanking and blitting here,
    # use tkapp.call to post a cross-thread event if this function is called
    # from a non-Tcl thread.

    # tkapp.call coerces all arguments to strings, so to avoid string parsing
    # within _blit, pack up the arguments into a global data structure.
    args = photoimage, dataptr, offsets, bboxptr, blank
    # Need a unique key to avoid thread races.
    # Again, make the key a string to avoid string parsing in _blit.
    argsid = str(id(args))
    _blit_args[argsid] = args

    try:
        photoimage.tk.call(_blit_tcl_name, argsid)
    except tk.TclError as e:
        if "invalid command name" not in str(e):
            raise
        photoimage.tk.createcommand(_blit_tcl_name, _blit)
        photoimage.tk.call(_blit_tcl_name, argsid)
