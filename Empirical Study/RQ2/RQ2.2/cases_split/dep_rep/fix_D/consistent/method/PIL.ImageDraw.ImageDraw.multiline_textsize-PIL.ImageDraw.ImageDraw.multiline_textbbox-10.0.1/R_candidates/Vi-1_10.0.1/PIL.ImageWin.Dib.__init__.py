    def __init__(self, image, size=None):
        if hasattr(image, "mode") and hasattr(image, "size"):
            mode = image.mode
            size = image.size
        else:
            mode = image
            image = None
        if mode not in ["1", "L", "P", "RGB"]:
            mode = Image.getmodebase(mode)
        self.image = Image.core.display(mode, size)
        self.mode = mode
        self.size = size
        if image:
            self.paste(image)
