    def __init__(self, image_or_list, mask=None):
        try:
            if mask:
                self.h = image_or_list.histogram(mask)
            else:
                self.h = image_or_list.histogram()
        except AttributeError:
            self.h = image_or_list  # assume it to be a histogram list
        if not isinstance(self.h, list):
            msg = "first argument must be image or list"
            raise TypeError(msg)
        self.bands = list(range(len(self.h) // 256))
