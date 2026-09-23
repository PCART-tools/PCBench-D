    class OffsetFilter(BaseFilter):

        def __init__(self, offsets=(0, 0)):
            self.offsets = offsets

        def get_pad(self, dpi):
            return int(max(self.offsets) / 72 * dpi)

        def process_image(self, padded_src, dpi):
            ox, oy = self.offsets
            a1 = np.roll(padded_src, int(ox / 72 * dpi), axis=1)
            a2 = np.roll(a1, -int(oy / 72 * dpi), axis=0)
            return a2
