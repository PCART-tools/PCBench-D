    class DropShadowFilter(BaseFilter):

        def __init__(self, sigma, alpha=0.3, color=(0, 0, 0), offsets=(0, 0)):
            self.gauss_filter = GaussianFilter(sigma, alpha, color)
            self.offset_filter = OffsetFilter(offsets)

        def get_pad(self, dpi):
            return max(self.gauss_filter.get_pad(dpi),
                       self.offset_filter.get_pad(dpi))

        def process_image(self, padded_src, dpi):
            t1 = self.gauss_filter.process_image(padded_src, dpi)
            t2 = self.offset_filter.process_image(t1, dpi)
            return t2
