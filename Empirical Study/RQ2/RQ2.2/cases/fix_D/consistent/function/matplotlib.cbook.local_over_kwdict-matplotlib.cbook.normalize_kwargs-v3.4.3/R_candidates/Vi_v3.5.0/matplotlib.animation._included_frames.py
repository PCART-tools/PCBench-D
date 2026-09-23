def _included_frames(paths, frame_format):
    """paths should be a list of Paths"""
    return INCLUDED_FRAMES.format(Nframes=len(paths),
                                  frame_dir=paths[0].parent,
                                  frame_format=frame_format)
