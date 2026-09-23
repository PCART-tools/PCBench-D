    @_preprocess_data(replace_names=["x"])
    @docstring.dedent_interpd
    def magnitude_spectrum(self, x, Fs=None, Fc=None, window=None,
                           pad_to=None, sides=None, scale=None,
                           **kwargs):
        """
        Plot the magnitude spectrum.

        Compute the magnitude spectrum of *x*.  Data is padded to a
        length of *pad_to* and the windowing function *window* is applied to
        the signal.

        Parameters
        ----------
        x : 1-D array or sequence
            Array or sequence containing the data.

        %(Spectral)s

        %(Single_Spectrum)s

        scale : {'default', 'linear', 'dB'}
            The scaling of the values in the *spec*.  'linear' is no scaling.
            'dB' returns the values in dB scale, i.e., the dB amplitude
            (20 * log10). 'default' is 'linear'.

        Fc : int
            The center frequency of *x* (defaults to 0), which offsets
            the x extents of the plot to reflect the frequency range used
            when a signal is acquired and then filtered and downsampled to
            baseband.

        Returns
        -------
        spectrum : 1-D array
            The values for the magnitude spectrum before scaling (real valued).

        freqs : 1-D array
            The frequencies corresponding to the elements in *spectrum*.

        line : a :class:`~matplotlib.lines.Line2D` instance
            The line created by this function.

        Other Parameters
        ----------------
        **kwargs
            Keyword arguments control the :class:`~matplotlib.lines.Line2D`
            properties:

        %(_Line2D_docstr)s

        See Also
        --------
        :func:`psd`
            :func:`psd` plots the power spectral density.`.

        :func:`angle_spectrum`
            :func:`angle_spectrum` plots the angles of the corresponding
            frequencies.

        :func:`phase_spectrum`
            :func:`phase_spectrum` plots the phase (unwrapped angle) of the
            corresponding frequencies.

        :func:`specgram`
            :func:`specgram` can plot the magnitude spectrum of segments within
            the signal in a colormap.

        """
        if Fc is None:
            Fc = 0

        if scale is None or scale == 'default':
            scale = 'linear'

        spec, freqs = mlab.magnitude_spectrum(x=x, Fs=Fs, window=window,
                                              pad_to=pad_to, sides=sides)
        freqs += Fc

        if scale == 'linear':
            Z = spec
            yunits = 'energy'
        elif scale == 'dB':
            Z = 20. * np.log10(spec)
            yunits = 'dB'
        else:
            raise ValueError('Unknown scale %s', scale)

        lines = self.plot(freqs, Z, **kwargs)
        self.set_xlabel('Frequency')
        self.set_ylabel('Magnitude (%s)' % yunits)

        return spec, freqs, lines[0]
