    def transform(self, size, image, **options):
        # can be overridden
        method, data = self.getdata()
        return image.transform(size, method, data, **options)
