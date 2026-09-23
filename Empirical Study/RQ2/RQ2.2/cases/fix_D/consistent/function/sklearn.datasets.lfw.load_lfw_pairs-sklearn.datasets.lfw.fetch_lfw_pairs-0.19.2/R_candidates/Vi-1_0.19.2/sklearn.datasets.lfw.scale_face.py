def scale_face(face):
    """Scale back to 0-1 range in case of normalization for plotting"""
    scaled = face - face.min()
    scaled /= scaled.max()
    return scaled
