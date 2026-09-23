def _blit(argsid):
    """
    Thin wrapper to blit called via tkapp.call.

    *argsid* is a unique string identifier to fetch the correct arguments from
    the ``_blit_args`` dict, since arguments cannot be passed directly.

    photoimage blanking must occur in the same event and thread as blitting
    to avoid flickering.
    """
    photoimage, dataptr, offsets, bboxptr, blank = _blit_args.pop(argsid)
    if blank:
        photoimage.blank()
    _tkagg.blit(
        photoimage.tk.interpaddr(), str(photoimage), dataptr, offsets, bboxptr)
