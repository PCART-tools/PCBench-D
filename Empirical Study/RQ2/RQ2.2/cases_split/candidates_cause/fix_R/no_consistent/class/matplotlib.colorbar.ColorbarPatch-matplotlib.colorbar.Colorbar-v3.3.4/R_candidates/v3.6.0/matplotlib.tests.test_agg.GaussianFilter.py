    class GaussianFilter(BaseFilter):
        """Simple Gaussian filter."""

        def __init__(self, sigma, alpha=0.5, color=(0, 0, 0)):
            self.sigma = sigma
            self.alpha = alpha
            self.color = color

        def get_pad(self, dpi):
            return int(self.sigma*3 / 72 * dpi)

        def process_image(self, padded_src, dpi):
            tgt_image = np.empty_like(padded_src)
            tgt_image[:, :, :3] = self.color
            tgt_image[:, :, 3] = smooth2d(padded_src[:, :, 3] * self.alpha,
                                          self.sigma / 72 * dpi)
            return tgt_image
