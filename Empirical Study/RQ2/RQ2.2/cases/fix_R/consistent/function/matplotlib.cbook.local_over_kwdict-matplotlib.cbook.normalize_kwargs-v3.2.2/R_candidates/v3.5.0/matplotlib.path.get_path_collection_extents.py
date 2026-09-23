def get_path_collection_extents(
        master_transform, paths, transforms, offsets, offset_transform):
    r"""
    Given a sequence of `Path`\s, `.Transform`\s objects, and offsets, as
    found in a `.PathCollection`, returns the bounding box that encapsulates
    all of them.

    Parameters
    ----------
    master_transform : `.Transform`
        Global transformation applied to all paths.
    paths : list of `Path`
    transforms : list of `.Affine2D`
    offsets : (N, 2) array-like
    offset_transform : `.Affine2D`
        Transform applied to the offsets before offsetting the path.

    Notes
    -----
    The way that *paths*, *transforms* and *offsets* are combined
    follows the same method as for collections:  Each is iterated over
    independently, so if you have 3 paths, 2 transforms and 1 offset,
    their combinations are as follows:

        (A, A, A), (B, B, A), (C, A, A)
    """
    from .transforms import Bbox
    if len(paths) == 0:
        raise ValueError("No paths provided")
    extents, minpos = _path.get_path_collection_extents(
        master_transform, paths, np.atleast_3d(transforms),
        offsets, offset_transform)
    return Bbox.from_extents(*extents, minpos=minpos)
