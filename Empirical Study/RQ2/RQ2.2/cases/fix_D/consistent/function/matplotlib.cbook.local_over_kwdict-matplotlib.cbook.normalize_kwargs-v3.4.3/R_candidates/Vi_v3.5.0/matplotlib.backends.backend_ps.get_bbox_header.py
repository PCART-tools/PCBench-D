def get_bbox_header(lbrt, rotated=False):
    """
    Return a postscript header string for the given bbox lbrt=(l, b, r, t).
    Optionally, return rotate command.
    """

    l, b, r, t = lbrt
    if rotated:
        rotate = "%.2f %.2f translate\n90 rotate" % (l+r, 0)
    else:
        rotate = ""
    bbox_info = '%%%%BoundingBox: %d %d %d %d' % (l, b, np.ceil(r), np.ceil(t))
    hires_bbox_info = '%%%%HiResBoundingBox: %.6f %.6f %.6f %.6f' % (
        l, b, r, t)

    return '\n'.join([bbox_info, hires_bbox_info]), rotate
