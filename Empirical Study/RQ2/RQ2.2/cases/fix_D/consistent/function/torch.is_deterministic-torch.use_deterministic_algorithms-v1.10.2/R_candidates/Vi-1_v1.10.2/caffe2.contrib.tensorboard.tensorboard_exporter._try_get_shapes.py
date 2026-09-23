def _try_get_shapes(nets):
    try:
        # Note: this will inspect the workspace for better or worse.
        shapes, _ = workspace.InferShapesAndTypes(nets)
        return shapes
    except Exception as e:
        logging.warning('Failed to compute shapes: %s', e)
        return {}
