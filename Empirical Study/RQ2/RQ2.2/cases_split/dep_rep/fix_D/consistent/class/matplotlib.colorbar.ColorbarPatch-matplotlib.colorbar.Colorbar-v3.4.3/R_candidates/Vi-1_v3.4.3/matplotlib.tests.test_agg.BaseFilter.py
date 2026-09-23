    class BaseFilter:

        def get_pad(self, dpi):
            return 0

        def process_image(self, padded_src, dpi):
            raise NotImplementedError("Should be overridden by subclasses")

        def __call__(self, im, dpi):
            pad = self.get_pad(dpi)
            padded_src = np.pad(im, [(pad, pad), (pad, pad), (0, 0)],
                                "constant")
            tgt_image = self.process_image(padded_src, dpi)
            return tgt_image, -pad, -pad
