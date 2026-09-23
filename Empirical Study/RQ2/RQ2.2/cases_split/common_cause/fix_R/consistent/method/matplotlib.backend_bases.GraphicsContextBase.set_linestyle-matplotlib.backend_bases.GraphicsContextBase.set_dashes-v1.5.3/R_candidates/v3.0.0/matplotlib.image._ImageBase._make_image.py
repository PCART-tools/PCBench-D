    def _make_image(self, A, in_bbox, out_bbox, clip_bbox, magnification=1.0,
                    unsampled=False, round_to_pixel_border=True):
        """
        Normalize, rescale and color the image `A` from the given
        in_bbox (in data space), to the given out_bbox (in pixel
        space) clipped to the given clip_bbox (also in pixel space),
        and magnified by the magnification factor.

        `A` may be a greyscale image (MxN) with a dtype of `float32`,
        `float64`, `float128`, `uint16` or `uint8`, or an RGBA image (MxNx4)
        with a dtype of `float32`, `float64`, `float128`, or `uint8`.

        If `unsampled` is True, the image will not be scaled, but an
        appropriate affine transformation will be returned instead.

        If `round_to_pixel_border` is True, the output image size will
        be rounded to the nearest pixel boundary.  This makes the
        images align correctly with the axes.  It should not be used
        in cases where you want exact scaling, however, such as
        FigureImage.

        Returns the resulting (image, x, y, trans), where (x, y) is
        the upper left corner of the result in pixel space, and
        `trans` is the affine transformation from the image to pixel
        space.
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
             + Affine2D().translate(
                 -clipped_bbox.x0,
                 -clipped_bbox.y0)
             .scale(magnification, magnification))

        # So that the image is aligned with the edge of the axes, we want
        # to round up the output width to the next integer.  This also
        # means scaling the transform just slightly to account for the
        # extra subpixel.
        if (t.is_affine and round_to_pixel_border and
                (out_width_base % 1.0 != 0.0 or out_height_base % 1.0 != 0.0)):
            out_width = int(ceil(out_width_base))
            out_height = int(ceil(out_height_base))
            extra_width = (out_width - out_width_base) / out_width_base
            extra_height = (out_height - out_height_base) / out_height_base
            t += Affine2D().scale(1.0 + extra_width, 1.0 + extra_height)
        else:
            out_width = int(out_width_base)
            out_height = int(out_height_base)

        if not unsampled:
            if A.ndim not in (2, 3):
                raise ValueError("Invalid dimensions, got {}".format(A.shape))

            if A.ndim == 2:
                # if we are a 2D array, then we are running through the
                # norm + colormap transformation.  However, in general the
                # input data is not going to match the size on the screen so we
                # have to resample to the correct number of pixels
                # need to

                # TODO slice input array first
                inp_dtype = A.dtype
                a_min = A.min()
                a_max = A.max()
                # figure out the type we should scale to.  For floats,
                # leave as is.  For integers cast to an appropriate-sized
                # float.  Small integers get smaller floats in an attempt
                # to keep the memory footprint reasonable.
                if a_min is np.ma.masked:
                    # all masked, so values don't matter
                    a_min, a_max = np.int32(0), np.int32(1)
                if inp_dtype.kind == 'f':
                    scaled_dtype = A.dtype
                    # Cast to float64
                    if A.dtype not in (np.float32, np.float16):
                        if A.dtype != np.float64:
                            warnings.warn(
                                "Casting input data from '{0}' to 'float64'"
                                "for imshow".format(A.dtype))
                        scaled_dtype = np.float64
                else:
                    # probably an integer of some type.
                    da = a_max.astype(np.float64) - a_min.astype(np.float64)
                    if da > 1e8:
                        # give more breathing room if a big dynamic range
                        scaled_dtype = np.float64
                    else:
                        scaled_dtype = np.float32

                # scale the input data to [.1, .9].  The Agg
                # interpolators clip to [0, 1] internally, use a
                # smaller input scale to identify which of the
                # interpolated points need to be should be flagged as
                # over / under.
                # This may introduce numeric instabilities in very broadly
                # scaled data
                A_scaled = np.empty(A.shape, dtype=scaled_dtype)
                A_scaled[:] = A
                # clip scaled data around norm if necessary.
                # This is necessary for big numbers at the edge of
                # float64's ability to represent changes.  Applying
                # a norm first would be good, but ruins the interpolation
                # of over numbers.
                self.norm.autoscale_None(A)
                dv = (np.float64(self.norm.vmax) -
                      np.float64(self.norm.vmin))
                vmid = self.norm.vmin + dv / 2
                fact = 1e7 if scaled_dtype == np.float64 else 1e4
                newmin = vmid - dv * fact
                if newmin < a_min:
                    newmin = None
                else:
                    a_min = np.float64(newmin)
                newmax = vmid + dv * fact
                if newmax > a_max:
                    newmax = None
                else:
                    a_max = np.float64(newmax)
                if newmax is not None or newmin is not None:
                    A_scaled = np.clip(A_scaled, newmin, newmax)

                A_scaled -= a_min
                # a_min and a_max might be ndarray subclasses so use
                # asscalar to avoid errors
                a_min = np.asscalar(a_min.astype(scaled_dtype))
                a_max = np.asscalar(a_max.astype(scaled_dtype))

                if a_min != a_max:
                    A_scaled /= ((a_max - a_min) / 0.8)
                A_scaled += 0.1
                A_resampled = np.zeros((out_height, out_width),
                                       dtype=A_scaled.dtype)
                # resample the input data to the correct resolution and shape
                _image.resample(A_scaled, A_resampled,
                                t,
                                _interpd_[self.get_interpolation()],
                                self.get_resample(), 1.0,
                                self.get_filternorm(),
                                self.get_filterrad())

                # we are done with A_scaled now, remove from namespace
                # to be sure!
                del A_scaled
                # un-scale the resampled data to approximately the
                # original range things that interpolated to above /
                # below the original min/max will still be above /
                # below, but possibly clipped in the case of higher order
                # interpolation + drastically changing data.
                A_resampled -= 0.1
                if a_min != a_max:
                    A_resampled *= ((a_max - a_min) / 0.8)
                A_resampled += a_min
                # if using NoNorm, cast back to the original datatype
                if isinstance(self.norm, mcolors.NoNorm):
                    A_resampled = A_resampled.astype(A.dtype)

                mask = np.empty(A.shape, dtype=np.float32)
                if A.mask.shape == A.shape:
                    # this is the case of a nontrivial mask
                    mask[:] = np.where(A.mask, np.float32(np.nan),
                                       np.float32(1))
                else:
                    mask[:] = 1

                # we always have to interpolate the mask to account for
                # non-affine transformations
                out_mask = np.zeros((out_height, out_width),
                                    dtype=mask.dtype)
                _image.resample(mask, out_mask,
                                t,
                                _interpd_[self.get_interpolation()],
                                True, 1,
                                self.get_filternorm(),
                                self.get_filterrad())
                # we are done with the mask, delete from namespace to be sure!
                del mask
                # Agg updates the out_mask in place.  If the pixel has
                # no image data it will not be updated (and still be 0
                # as we initialized it), if input data that would go
                # into that output pixel than it will be `nan`, if all
                # the input data for a pixel is good it will be 1, and
                # if there is _some_ good data in that output pixel it
                # will be between [0, 1] (such as a rotated image).

                out_alpha = np.array(out_mask)
                out_mask = np.isnan(out_mask)
                out_alpha[out_mask] = 1

                # mask and run through the norm
                output = self.norm(np.ma.masked_array(A_resampled, out_mask))
            else:
                # Always convert to RGBA, even if only RGB input
                if A.shape[2] == 3:
                    A = _rgb_to_rgba(A)
                elif A.shape[2] != 4:
                    raise ValueError("Invalid dimensions, got %s" % (A.shape,))

                output = np.zeros((out_height, out_width, 4), dtype=A.dtype)

                alpha = self.get_alpha()
                if alpha is None:
                    alpha = 1.0

                _image.resample(
                    A, output, t, _interpd_[self.get_interpolation()],
                    self.get_resample(), alpha,
                    self.get_filternorm(), self.get_filterrad())

            # at this point output is either a 2D array of normed data
            # (of int or float)
            # or an RGBA array of re-sampled input
            output = self.to_rgba(output, bytes=True, norm=False)
            # output is now a correctly sized RGBA array of uint8

            # Apply alpha *after* if the input was greyscale without a mask
            if A.ndim == 2:
                alpha = self.get_alpha()
                if alpha is None:
                    alpha = 1
                alpha_channel = output[:, :, 3]
                alpha_channel[:] = np.asarray(
                    np.asarray(alpha_channel, np.float32) * out_alpha * alpha,
                    np.uint8)

        else:
            if self._imcache is None:
                self._imcache = self.to_rgba(A, bytes=True, norm=(A.ndim == 2))
            output = self._imcache

            # Subset the input image to only the part that will be
            # displayed
            subset = TransformedBbox(
                clip_bbox, t0.frozen().inverted()).frozen()
            output = output[
                int(max(subset.ymin, 0)):
                int(min(subset.ymax + 1, output.shape[0])),
                int(max(subset.xmin, 0)):
                int(min(subset.xmax + 1, output.shape[1]))]

            t = Affine2D().translate(
                int(max(subset.xmin, 0)), int(max(subset.ymin, 0))) + t

        return output, clipped_bbox.x0, clipped_bbox.y0, t
