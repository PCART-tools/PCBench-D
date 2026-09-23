class _ImageBase(martist.Artist, cm.ScalarMappable):
    """
    Base class for images.

    interpolation and cmap default to their rc settings

    cmap is a colors.Colormap instance
    norm is a colors.Normalize instance to map luminance to 0-1

    extent is data axes (left, right, bottom, top) for making image plots
    registered with data plots.  Default is to label the pixel
    centers with the zero-based row and column indices.

    Additional kwargs are matplotlib.artist properties
    """
    zorder = 0

    def __init__(self, ax,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
                 filternorm=True,
                 filterrad=4.0,
                 resample=False,
                 *,
                 interpolation_stage=None,
                 **kwargs
                 ):
        martist.Artist.__init__(self)
        cm.ScalarMappable.__init__(self, norm, cmap)
        if origin is None:
            origin = mpl.rcParams['image.origin']
        _api.check_in_list(["upper", "lower"], origin=origin)
        self.origin = origin
        self.set_filternorm(filternorm)
        self.set_filterrad(filterrad)
        self.set_interpolation(interpolation)
        self.set_interpolation_stage(interpolation_stage)
        self.set_resample(resample)
        self.axes = ax

        self._imcache = None

        self._internal_update(kwargs)

    def __str__(self):
        try:
            size = self.get_size()
            return f"{type(self).__name__}(size={size!r})"
        except RuntimeError:
            return type(self).__name__

    def __getstate__(self):
        # Save some space on the pickle by not saving the cache.
        return {**super().__getstate__(), "_imcache": None}

    def get_size(self):
        """Return the size of the image as tuple (numrows, numcols)."""
        if self._A is None:
            raise RuntimeError('You must first set the image array')

        return self._A.shape[:2]

    def set_alpha(self, alpha):
        """
        Set the alpha value used for blending - not supported on all backends.

        Parameters
        ----------
        alpha : float or 2D array-like or None
        """
        martist.Artist._set_alpha_for_array(self, alpha)
        if np.ndim(alpha) not in (0, 2):
            raise TypeError('alpha must be a float, two-dimensional '
                            'array, or None')
        self._imcache = None

    def _get_scalar_alpha(self):
        """
        Get a scalar alpha value to be applied to the artist as a whole.

        If the alpha value is a matrix, the method returns 1.0 because pixels
        have individual alpha values (see `~._ImageBase._make_image` for
        details). If the alpha value is a scalar, the method returns said value
        to be applied to the artist as a whole because pixels do not have
        individual alpha values.
        """
        return 1.0 if self._alpha is None or np.ndim(self._alpha) > 0 \
            else self._alpha

    def changed(self):
        """
        Call this whenever the mappable is changed so observers can update.
        """
        self._imcache = None
        cm.ScalarMappable.changed(self)

    def _make_image(self, A, in_bbox, out_bbox, clip_bbox, magnification=1.0,
                    unsampled=False, round_to_pixel_border=True):
        """
        Normalize, rescale, and colormap the image *A* from the given *in_bbox*
        (in data space), to the given *out_bbox* (in pixel space) clipped to
        the given *clip_bbox* (also in pixel space), and magnified by the
        *magnification* factor.

        *A* may be a greyscale image (M, N) with a dtype of float32, float64,
        float128, uint16 or uint8, or an (M, N, 4) RGBA image with a dtype of
        float32, float64, float128, or uint8.

        If *unsampled* is True, the image will not be scaled, but an
        appropriate affine transformation will be returned instead.

        If *round_to_pixel_border* is True, the output image size will be
        rounded to the nearest pixel boundary.  This makes the images align
        correctly with the axes.  It should not be used if exact scaling is
        needed, such as for `FigureImage`.

        Returns
        -------
        image : (M, N, 4) uint8 array
            The RGBA image, resampled unless *unsampled* is True.
        x, y : float
            The upper left corner where the image should be drawn, in pixel
            space.
        trans : Affine2D
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

        # So that the image is aligned with the edge of the axes, we want to
        # round up the output width to the next integer.  This also means
        # scaling the transform slightly to account for the extra subpixel.
        if (t.is_affine and round_to_pixel_border and
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
            if A.ndim == 2 and self._interpolation_stage != 'rgba':
                # if we are a 2D array, then we are running through the
                # norm + colormap transformation.  However, in general the
                # input data is not going to match the size on the screen so we
                # have to resample to the correct number of pixels

                # TODO slice input array first
                a_min = A.min()
                a_max = A.max()
                if a_min is np.ma.masked:  # All masked; values don't matter.
                    a_min, a_max = np.int32(0), np.int32(1)
                if A.dtype.kind == 'f':  # Float dtype: scale to same dtype.
                    scaled_dtype = np.dtype(
                        np.float64 if A.dtype.itemsize > 4 else np.float32)
                    if scaled_dtype.itemsize < A.dtype.itemsize:
                        _api.warn_external(f"Casting input data from {A.dtype}"
                                           f" to {scaled_dtype} for imshow.")
                else:  # Int dtype, likely.
                    # Scale to appropriately sized float: use float32 if the
                    # dynamic range is small, to limit the memory footprint.
                    da = a_max.astype(np.float64) - a_min.astype(np.float64)
                    scaled_dtype = np.float64 if da > 1e8 else np.float32

                # Scale the input data to [.1, .9].  The Agg interpolators clip
                # to [0, 1] internally, and we use a smaller input scale to
                # identify the interpolated points that need to be flagged as
                # over/under.  This may introduce numeric instabilities in very
                # broadly scaled data.

                # Always copy, and don't allow array subtypes.
                A_scaled = np.array(A, dtype=scaled_dtype)
                # Clip scaled data around norm if necessary.  This is necessary
                # for big numbers at the edge of float64's ability to represent
                # changes.  Applying a norm first would be good, but ruins the
                # interpolation of over numbers.
                self.norm.autoscale_None(A)
                dv = np.float64(self.norm.vmax) - np.float64(self.norm.vmin)
                vmid = np.float64(self.norm.vmin) + dv / 2
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
                    np.clip(A_scaled, newmin, newmax, out=A_scaled)

                # Rescale the raw data to [offset, 1-offset] so that the
                # resampling code will run cleanly.  Using dyadic numbers here
                # could reduce the error, but would not fully eliminate it and
                # breaks a number of tests (due to the slightly different
                # error bouncing some pixels across a boundary in the (very
                # quantized) colormapping step).
                offset = .1
                frac = .8
                # Run vmin/vmax through the same rescaling as the raw data;
                # otherwise, data values close or equal to the boundaries can
                # end up on the wrong side due to floating point error.
                vmin, vmax = self.norm.vmin, self.norm.vmax
                if vmin is np.ma.masked:
                    vmin, vmax = a_min, a_max
                vrange = np.array([vmin, vmax], dtype=scaled_dtype)

                A_scaled -= a_min
                vrange -= a_min
                # .item() handles a_min/a_max being ndarray subclasses.
                a_min = a_min.astype(scaled_dtype).item()
                a_max = a_max.astype(scaled_dtype).item()

                if a_min != a_max:
                    A_scaled /= ((a_max - a_min) / frac)
                    vrange /= ((a_max - a_min) / frac)
                A_scaled += offset
                vrange += offset
                # resample the input data to the correct resolution and shape
                A_resampled = _resample(self, A_scaled, out_shape, t)
                del A_scaled  # Make sure we don't use A_scaled anymore!
                # Un-scale the resampled data to approximately the original
                # range. Things that interpolated to outside the original range
                # will still be outside, but possibly clipped in the case of
                # higher order interpolation + drastically changing data.
                A_resampled -= offset
                vrange -= offset
                if a_min != a_max:
                    A_resampled *= ((a_max - a_min) / frac)
                    vrange *= ((a_max - a_min) / frac)
                A_resampled += a_min
                vrange += a_min
                # if using NoNorm, cast back to the original datatype
                if isinstance(self.norm, mcolors.NoNorm):
                    A_resampled = A_resampled.astype(A.dtype)

                mask = (np.where(A.mask, np.float32(np.nan), np.float32(1))
                        if A.mask.shape == A.shape  # nontrivial mask
                        else np.ones_like(A, np.float32))
                # we always have to interpolate the mask to account for
                # non-affine transformations
                out_alpha = _resample(self, mask, out_shape, t, resample=True)
                del mask  # Make sure we don't use mask anymore!
                # Agg updates out_alpha in place.  If the pixel has no image
                # data it will not be updated (and still be 0 as we initialized
                # it), if input data that would go into that output pixel than
                # it will be `nan`, if all the input data for a pixel is good
                # it will be 1, and if there is _some_ good data in that output
                # pixel it will be between [0, 1] (such as a rotated image).
                out_mask = np.isnan(out_alpha)
                out_alpha[out_mask] = 1
                # Apply the pixel-by-pixel alpha values if present
                alpha = self.get_alpha()
                if alpha is not None and np.ndim(alpha) > 0:
                    out_alpha *= _resample(self, alpha, out_shape,
                                           t, resample=True)
                # mask and run through the norm
                resampled_masked = np.ma.masked_array(A_resampled, out_mask)
                # we have re-set the vmin/vmax to account for small errors
                # that may have moved input values in/out of range
                s_vmin, s_vmax = vrange
                if isinstance(self.norm, mcolors.LogNorm) and s_vmin <= 0:
                    # Don't give 0 or negative values to LogNorm
                    s_vmin = np.finfo(scaled_dtype).eps
                # Block the norm from sending an update signal during the
                # temporary vmin/vmax change
                with self.norm.callbacks.blocked(), \
                     cbook._setattr_cm(self.norm, vmin=s_vmin, vmax=s_vmax):
                    output = self.norm(resampled_masked)
            else:
                if A.ndim == 2:  # _interpolation_stage == 'rgba'
                    self.norm.autoscale_None(A)
                    A = self.to_rgba(A)
                if A.shape[2] == 3:
                    A = _rgb_to_rgba(A)
                alpha = self._get_scalar_alpha()
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

    def make_image(self, renderer, magnification=1.0, unsampled=False):
        """
        Normalize, rescale, and colormap this image's data for rendering using
        *renderer*, with the given *magnification*.

        If *unsampled* is True, the image will not be scaled, but an
        appropriate affine transformation will be returned instead.

        Returns
        -------
        image : (M, N, 4) uint8 array
            The RGBA image, resampled unless *unsampled* is True.
        x, y : float
            The upper left corner where the image should be drawn, in pixel
            space.
        trans : Affine2D
            The affine transformation from image to pixel space.
        """
        raise NotImplementedError('The make_image method must be overridden')

    def _check_unsampled_image(self):
        """
        Return whether the image is better to be drawn unsampled.

        The derived class needs to override it.
        """
        return False

    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        # if not visible, declare victory and return
        if not self.get_visible():
            self.stale = False
            return
        # for empty images, there is nothing to draw!
        if self.get_array().size == 0:
            self.stale = False
            return
        # actually render the image.
        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_alpha(self._get_scalar_alpha())
        gc.set_url(self.get_url())
        gc.set_gid(self.get_gid())
        if (renderer.option_scale_image()  # Renderer supports transform kwarg.
                and self._check_unsampled_image()
                and self.get_transform().is_affine):
            im, l, b, trans = self.make_image(renderer, unsampled=True)
            if im is not None:
                trans = Affine2D().scale(im.shape[1], im.shape[0]) + trans
                renderer.draw_image(gc, l, b, im, trans)
        else:
            im, l, b, trans = self.make_image(
                renderer, renderer.get_image_magnification())
            if im is not None:
                renderer.draw_image(gc, l, b, im)
        gc.restore()
        self.stale = False

    def contains(self, mouseevent):
        """Test whether the mouse event occurred within the image."""
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        # 1) This doesn't work for figimage; but figimage also needs a fix
        #    below (as the check cannot use x/ydata and extents).
        # 2) As long as the check below uses x/ydata, we need to test axes
        #    identity instead of `self.axes.contains(event)` because even if
        #    axes overlap, x/ydata is only valid for event.inaxes anyways.
        if self.axes is not mouseevent.inaxes:
            return False, {}
        # TODO: make sure this is consistent with patch and patch
        # collection on nonlinear transformed coordinates.
        # TODO: consider returning image coordinates (shouldn't
        # be too difficult given that the image is rectilinear
        trans = self.get_transform().inverted()
        x, y = trans.transform([mouseevent.x, mouseevent.y])
        xmin, xmax, ymin, ymax = self.get_extent()
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin

        if x is not None and y is not None:
            inside = (xmin <= x <= xmax) and (ymin <= y <= ymax)
        else:
            inside = False

        return inside, {}

    def write_png(self, fname):
        """Write the image to png file *fname*."""
        im = self.to_rgba(self._A[::-1] if self.origin == 'lower' else self._A,
                          bytes=True, norm=True)
        PIL.Image.fromarray(im).save(fname, format="png")

    def set_data(self, A):
        """
        Set the image array.

        Note that this function does *not* update the normalization used.

        Parameters
        ----------
        A : array-like or `PIL.Image.Image`
        """
        if isinstance(A, PIL.Image.Image):
            A = pil_to_array(A)  # Needed e.g. to apply png palette.
        self._A = cbook.safe_masked_invalid(A, copy=True)

        if (self._A.dtype != np.uint8 and
                not np.can_cast(self._A.dtype, float, "same_kind")):
            raise TypeError("Image data of dtype {} cannot be converted to "
                            "float".format(self._A.dtype))

        if self._A.ndim == 3 and self._A.shape[-1] == 1:
            # If just one dimension assume scalar and apply colormap
            self._A = self._A[:, :, 0]

        if not (self._A.ndim == 2
                or self._A.ndim == 3 and self._A.shape[-1] in [3, 4]):
            raise TypeError("Invalid shape {} for image data"
                            .format(self._A.shape))

        if self._A.ndim == 3:
            # If the input data has values outside the valid range (after
            # normalisation), we issue a warning and then clip X to the bounds
            # - otherwise casting wraps extreme values, hiding outliers and
            # making reliable interpretation impossible.
            high = 255 if np.issubdtype(self._A.dtype, np.integer) else 1
            if self._A.min() < 0 or high < self._A.max():
                _log.warning(
                    'Clipping input data to the valid range for imshow with '
                    'RGB data ([0..1] for floats or [0..255] for integers).'
                )
                self._A = np.clip(self._A, 0, high)
            # Cast unsupported integer types to uint8
            if self._A.dtype != np.uint8 and np.issubdtype(self._A.dtype,
                                                           np.integer):
                self._A = self._A.astype(np.uint8)

        self._imcache = None
        self.stale = True

    def set_array(self, A):
        """
        Retained for backwards compatibility - use set_data instead.

        Parameters
        ----------
        A : array-like
        """
        # This also needs to be here to override the inherited
        # cm.ScalarMappable.set_array method so it is not invoked by mistake.
        self.set_data(A)

    def get_interpolation(self):
        """
        Return the interpolation method the image uses when resizing.

        One of 'antialiased', 'nearest', 'bilinear', 'bicubic', 'spline16',
        'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
        'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos',
        or 'none'.
        """
        return self._interpolation

    def set_interpolation(self, s):
        """
        Set the interpolation method the image uses when resizing.

        If None, use :rc:`image.interpolation`. If 'none', the image is
        shown as is without interpolating. 'none' is only supported in
        agg, ps and pdf backends and will fall back to 'nearest' mode
        for other backends.

        Parameters
        ----------
        s : {'antialiased', 'nearest', 'bilinear', 'bicubic', 'spline16', \
'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', \
'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos', 'none'} or None
        """
        if s is None:
            s = mpl.rcParams['image.interpolation']
        s = s.lower()
        _api.check_in_list(_interpd_, interpolation=s)
        self._interpolation = s
        self.stale = True

    def set_interpolation_stage(self, s):
        """
        Set when interpolation happens during the transform to RGBA.

        Parameters
        ----------
        s : {'data', 'rgba'} or None
            Whether to apply up/downsampling interpolation in data or rgba
            space.
        """
        if s is None:
            s = "data"  # placeholder for maybe having rcParam
        _api.check_in_list(['data', 'rgba'], s=s)
        self._interpolation_stage = s
        self.stale = True

    def can_composite(self):
        """Return whether the image can be composited with its neighbors."""
        trans = self.get_transform()
        return (
            self._interpolation != 'none' and
            trans.is_affine and
            trans.is_separable)

    def set_resample(self, v):
        """
        Set whether image resampling is used.

        Parameters
        ----------
        v : bool or None
            If None, use :rc:`image.resample`.
        """
        if v is None:
            v = mpl.rcParams['image.resample']
        self._resample = v
        self.stale = True

    def get_resample(self):
        """Return whether image resampling is used."""
        return self._resample

    def set_filternorm(self, filternorm):
        """
        Set whether the resize filter normalizes the weights.

        See help for `~.Axes.imshow`.

        Parameters
        ----------
        filternorm : bool
        """
        self._filternorm = bool(filternorm)
        self.stale = True

    def get_filternorm(self):
        """Return whether the resize filter normalizes the weights."""
        return self._filternorm

    def set_filterrad(self, filterrad):
        """
        Set the resize filter radius only applicable to some
        interpolation schemes -- see help for imshow

        Parameters
        ----------
        filterrad : positive float
        """
        r = float(filterrad)
        if r <= 0:
            raise ValueError("The filter radius must be a positive number")
        self._filterrad = r
        self.stale = True

    def get_filterrad(self):
        """Return the filterrad setting."""
        return self._filterrad
