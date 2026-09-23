def _save_spider(im, fp, filename):
    # get the filename extension and register it with Image
    ext = os.path.splitext(filename)[1]
    Image.register_extension(SpiderImageFile.format, ext)
    _save(im, fp, filename)
