def toqpixmap(im):
    # # This doesn't work. For now using a dumb approach.
    # im_data = _toqclass_helper(im)
    # result = QPixmap(im_data["size"][0], im_data["size"][1])
    # result.loadFromData(im_data["data"])
    qimage = toqimage(im)
    return QPixmap.fromImage(qimage)
