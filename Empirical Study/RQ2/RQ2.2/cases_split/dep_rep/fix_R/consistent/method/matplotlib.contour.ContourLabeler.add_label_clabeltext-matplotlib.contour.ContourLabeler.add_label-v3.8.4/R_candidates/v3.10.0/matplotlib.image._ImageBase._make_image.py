    def _make_image(self, A, in_bbox, out_bbox, clip_bbox, magnification=1.0,
                    unsampled=False, round_to_pixel_border=True):
        """
        Normalize, rescale, and colormap the image *A* from the given *in_bbox*
        (in data space), to the given *out_bbox* (in pixel space) clipped to
        the given *clip_bbox* (also in pixel space), and magnified by the
        *magnification* factor.

        Parameters
        ----------
        A : ndarray

            - a (M, N) array interpreted as scalar (greyscale) image,
              with one of the dtypes `~numpy.float32`, `~numpy.float64`,
              `~numpy.float128`, `~numpy.uint16` or `~numpy.uint8`.
            - (M, N, 4) RGBA image with a dtype of `~numpy.float32`,
              `~numpy.float64`, `~numpy.float128`, or `~numpy.uint8`.

        in_bbox : `~matplotlib.transforms.Bbox`

        out_bbox : `~matplotlib.transforms.Bbox`

        clip_bbox : `~matplotlib.transforms.Bbox`

        magnification : float, default: 1

        unsampled : bool, default: False
            If True, the image will not be scaled, but an appropriate
            affine transformation will be returned instead.

        round_to_pixel_border : bool, default: True
            If True, the output image size will be rounded to the nearest pixel
            boundary.  This makes the images align correctly with the Axes.
            It should not be used if exact scaling is needed, such as for
            `.FigureImage`.

        Returns
        -------
        image : (M, N, 4) `numpy.uint8` array
            The RGBA image, resampled unless *unsampled* is True.
        x, y : float
            The upper left corner where the image should be drawn, in pixel
            space.
        trans : `~matplotlib.transforms.Affine2D`
            The affine transformation from image to pixel space.
        """
        if A is None:
            raise RuntimeError('You must first set the image '
                               'array or the image attribute')
        if A.size == 0:
            raise RuntimeError("_make_image must get a non-empty image. "
                               "Your Artist's draw method must filter before "
                               "this method is called.")

        clipped_bbox = Bbox.intersection(out_bbox, clip_bbox)

        if clipped_bbox is None:
            return None, 0, 0, None

        out_width_base = clipped_bbox.width * magnification
        out_height_base = clipped_bbox.height * magnification

        if out_width_base == 0 or out_height_base == 0:
            return None, 0, 0, None

        if self.origin == 'upper':
            # Flip the input image using a transform.  This avoids the
            # problem with flipping the array, which results in a copy
            # when it is converted to contiguous in the C wrapper
            t0 = Affine2D().translate(0, -A.shape[0]).scale(1, -1)
        else:
            t0 = IdentityTransform()

        t0 += (
            Affine2D()
            .scale(
                in_bbox.width / A.shape[1],
                in_bbox.height / A.shape[0])
            .translate(in_bbox.x0, in_bbox.y0)
            + self.get_transform())

        t = (t0
             + (Affine2D()
                .translate(-clipped_bbox.x0, -clipped_bbox.y0)
                .scale(magnification)))

        # So that the image is aligned with the edge of the Axes, we want to
        # round up the output width to the next integer.  This also means
        # scaling the transform slightly to account for the extra subpixel.
        if ((not unsampled) and t.is_affine and round_to_pixel_border and
                (out_width_base % 1.0 != 0.0 or out_height_base % 1.0 != 0.0)):
            out_width = math.ceil(out_width_base)
            out_height = math.ceil(out_height_base)
            extra_width = (out_width - out_width_base) / out_width_base
            extra_height = (out_height - out_height_base) / out_height_base
            t += Affine2D().scale(1.0 + extra_width, 1.0 + extra_height)
        else:
            out_width = int(out_width_base)
            out_height = int(out_height_base)
        out_shape = (out_height, out_width)

        if not unsampled:
            if not (A.ndim == 2 or A.ndim == 3 and A.shape[-1] in (3, 4)):
                raise ValueError(f"Invalid shape {A.shape} for image data")

            # if antialiased, this needs to change as window sizes
            # change:
            interpolation_stage = self._interpolation_stage
            if interpolation_stage in ['antialiased', 'auto']:
                pos = np.array([[0, 0], [A.shape[1], A.shape[0]]])
                disp = t.transform(pos)
                dispx = np.abs(np.diff(disp[:, 0])) / A.shape[1]
                dispy = np.abs(np.diff(disp[:, 1])) / A.shape[0]
                if (dispx < 3) or (dispy < 3):
                    interpolation_stage = 'rgba'
                else:
                    interpolation_stage = 'data'

            if A.ndim == 2 and interpolation_stage == 'data':
                # if we are a 2D array, then we are running through the
                # norm + colormap transformation.  However, in general the
                # input data is not going to match the size on the screen so we
                # have to resample to the correct number of pixels

                if A.dtype.kind == 'f':  # Float dtype: scale to same dtype.
                    scaled_dtype = np.dtype("f8" if A.dtype.itemsize > 4 else "f4")
                    if scaled_dtype.itemsize < A.dtype.itemsize:
                        _api.warn_external(f"Casting input data from {A.dtype}"
                                           f" to {scaled_dtype} for imshow.")
                else:  # Int dtype, likely.
                    # TODO slice input array first
                    # Scale to appropriately sized float: use float32 if the
                    # dynamic range is small, to limit the memory footprint.
                    da = A.max().astype("f8") - A.min().astype("f8")
                    scaled_dtype = "f8" if da > 1e8 else "f4"

                # resample the input data to the correct resolution and shape
                A_resampled = _resample(self, A.astype(scaled_dtype), out_shape, t)

                # if using NoNorm, cast back to the original datatype
                if isinstance(self.norm, mcolors.NoNorm):
                    A_resampled = A_resampled.astype(A.dtype)

                # Compute out_mask (what screen pixels include "bad" data
                # pixels) and out_alpha (to what extent screen pixels are
                # covered by data pixels: 0 outside the data extent, 1 inside
                # (even for bad data), and intermediate values at the edges).
                mask = (np.where(A.mask, np.float32(np.nan), np.float32(1))
                        if A.mask.shape == A.shape  # nontrivial mask
                        else np.ones_like(A, np.float32))
                # we always have to interpolate the mask to account for
                # non-affine transformations
                out_alpha = _resample(self, mask, out_shape, t, resample=True)
                del mask  # Make sure we don't use mask anymore!
                out_mask = np.isnan(out_alpha)
                out_alpha[out_mask] = 1
                # Apply the pixel-by-pixel alpha values if present
                alpha = self.get_alpha()
                if alpha is not None and np.ndim(alpha) > 0:
                    out_alpha *= _resample(self, alpha, out_shape, t, resample=True)
                # mask and run through the norm
                resampled_masked = np.ma.masked_array(A_resampled, out_mask)
                output = self.norm(resampled_masked)
            else:
                if A.ndim == 2:  # interpolation_stage = 'rgba'
                    self.norm.autoscale_None(A)
                    A = self.to_rgba(A)
                alpha = self._get_scalar_alpha()
                if A.shape[2] == 3:
                    # No need to resample alpha or make a full array; NumPy will expand
                    # this out and cast to uint8 if necessary when it's assigned to the
                    # alpha channel below.
                    output_alpha = (255 * alpha) if A.dtype == np.uint8 else alpha
                else:
                    output_alpha = _resample(  # resample alpha channel
                        self, A[..., 3], out_shape, t, alpha=alpha)
                output = _resample(  # resample rgb channels
                    self, _rgb_to_rgba(A[..., :3]), out_shape, t, alpha=alpha)
                output[..., 3] = output_alpha  # recombine rgb and alpha

            # output is now either a 2D array of normed (int or float) data
            # or an RGBA array of re-sampled input
            output = self.to_rgba(output, bytes=True, norm=False)
            # output is now a correctly sized RGBA array of uint8

            # Apply alpha *after* if the input was greyscale without a mask
            if A.ndim == 2:
                alpha = self._get_scalar_alpha()
                alpha_channel = output[:, :, 3]
                alpha_channel[:] = (  # Assignment will cast to uint8.
                    alpha_channel.astype(np.float32) * out_alpha * alpha)

        else:
            if self._imcache is None:
                self._imcache = self.to_rgba(A, bytes=True, norm=(A.ndim == 2))
            output = self._imcache

            # Subset the input image to only the part that will be displayed.
            subset = TransformedBbox(clip_bbox, t0.inverted()).frozen()
            output = output[
                int(max(subset.ymin, 0)):
                int(min(subset.ymax + 1, output.shape[0])),
                int(max(subset.xmin, 0)):
                int(min(subset.xmax + 1, output.shape[1]))]

            t = Affine2D().translate(
                int(max(subset.xmin, 0)), int(max(subset.ymin, 0))) + t

        return output, clipped_bbox.x0, clipped_bbox.y0, t
