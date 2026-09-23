def _get_image_from_kw(kw):
    source = None
    if "file" in kw:
        source = kw.pop("file")
    elif "data" in kw:
        source = BytesIO(kw.pop("data"))
    if source:
        return Image.open(source)
