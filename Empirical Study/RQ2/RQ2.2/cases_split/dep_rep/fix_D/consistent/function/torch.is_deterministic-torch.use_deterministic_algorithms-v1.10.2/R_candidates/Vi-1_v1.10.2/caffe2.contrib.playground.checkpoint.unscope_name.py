def unscope_name(blob_name):
    return blob_name[blob_name.rfind(scope._NAMESCOPE_SEPARATOR) + 1:]
