@_api.deprecated("3.3")
def validate_movie_writer(s):
    # writers.list() would only list actually available writers, but
    # FFMpeg.isAvailable is slow and not worth paying for at every import.
    if s in animation.writers._registered:
        return s
    else:
        raise ValueError(f"Supported animation writers are "
                         f"{sorted(animation.writers._registered)}")
