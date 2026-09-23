    @_preprocess_data(replace_names=["x"], label_namer=None)
    @docstring.dedent_interpd
    def angle_spectrum(self, x, Fs=None, Fc=None, window=None,
                       pad_to=None, sides=None, **kwargs):
        """
        Plot the angle spectrum.

        Call signature::

          angle_spectrum(x, Fs=2, Fc=0,  window=mlab.window_hanning,
                         pad_to=None, sides='default', **kwargs)

        Compute the angle spectrum (wrapped phase spectrum) of *x*.
        Data is padded to a length of *pad_to* and the windowing function
        *window* is applied to the signal.

        Parameters
        ----------
        x : 1-D array or sequence
            Array or sequence containing the data

        %(Spectral)s

        %(Single_Spectrum)s

        Fc : integer
            The center frequency of *x* (defaults to 0), which offsets
            the x extents of the plot to reflect the frequency range used
            when a signal is acquired and then filtered and downsampled to
            baseband.

        Returns
        -------
        spectrum : 1-D array
            The values for the angle spectrum in radians (real valued)

        freqs : 1-D array
            The frequencies corresponding to the elements in *spectrum*

        line : a :class:`~matplotlib.lines.Line2D` instance
            The line created by this function

        Other Parameters
        ----------------
        **kwargs :
            Keyword arguments control the :class:`~matplotlib.lines.Line2D`
            properties:

            %(Line2D)s

        See Also
        --------
        :func:`magnitude_spectrum`
            :func:`angle_spectrum` plots the magnitudes of the corresponding
            frequencies.

        :func:`phase_spectrum`
            :func:`phase_spectrum` plots the unwrapped version of this
            function.

        :func:`specgram`
            :func:`specgram` can plot the angle spectrum of segments within the
            signal in a colormap.
        """
        if not self._hold:
            self.cla()

        if Fc is None:
            Fc = 0

        spec, freqs = mlab.angle_spectrum(x=x, Fs=Fs, window=window,
                                          pad_to=pad_to, sides=sides)
        freqs += Fc

        lines = self.plot(freqs, spec, **kwargs)
        self.set_xlabel('Frequency')
        self.set_ylabel('Angle (radians)')

        return spec, freqs, lines[0]
