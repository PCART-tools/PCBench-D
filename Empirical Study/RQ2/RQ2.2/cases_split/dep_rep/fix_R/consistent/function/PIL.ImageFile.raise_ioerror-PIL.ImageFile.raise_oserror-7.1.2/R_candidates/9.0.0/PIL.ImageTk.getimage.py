def getimage(photo):
    """Copies the contents of a PhotoImage to a PIL image memory."""
    im = Image.new("RGBA", (photo.width(), photo.height()))
    block = im.im

    photo.tk.call("PyImagingPhotoGet", photo, block.id)

    return im
