def _try_get_shapes(nets):
    '''
    Get missing shapes for all blobs contained in the nets.

    Args:
        nets: List of core.Net to extract blob shape information from.

    Returns:
        Dictionary containing blob name to shape/dimensions mapping. The net
            is a computation graph that is composed of operators, and the
            operators have input and output blobs, each with their own dims.
    '''
    try:
        # Note: this will inspect the workspace for better or worse.
        # We don't care about the types, only the shapes
        shapes, _ = workspace.InferShapesAndTypes(nets)
        return shapes
    except Exception as e:
        logging.warning('Failed to compute shapes: %s', e)
        return {}
