def _blit(argsid):
    """
    Thin wrapper to blit called via tkapp.call.

    *argsid* is a unique string identifier to fetch the correct arguments from
    the ``_blit_args`` dict, since arguments cannot be passed directly.
    """
    photoimage, dataptr, offsets, bboxptr, comp_rule = _blit_args.pop(argsid)
    _tkagg.blit(photoimage.tk.interpaddr(), str(photoimage), dataptr,
                comp_rule, offsets, bboxptr)
