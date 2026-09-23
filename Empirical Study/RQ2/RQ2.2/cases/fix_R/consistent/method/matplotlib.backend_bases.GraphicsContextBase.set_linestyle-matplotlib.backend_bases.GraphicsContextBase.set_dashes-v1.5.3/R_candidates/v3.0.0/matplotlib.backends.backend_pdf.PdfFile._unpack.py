    def _unpack(self, im):
        """
        Unpack the image object im into height, width, data, alpha,
        where data and alpha are HxWx3 (RGB) or HxWx1 (grayscale or alpha)
        arrays, except alpha is None if the image is fully opaque.
        """
        h, w = im.shape[:2]
        im = im[::-1]
        if im.ndim == 2:
            return h, w, im, None
        else:
            rgb = im[:, :, :3]
            rgb = np.array(rgb, order='C')
            # PDF needs a separate alpha image
            if im.shape[2] == 4:
                alpha = im[:, :, 3][..., None]
                if np.all(alpha == 255):
                    alpha = None
                else:
                    alpha = np.array(alpha, order='C')
            else:
                alpha = None
            return h, w, rgb, alpha
