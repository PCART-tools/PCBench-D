def parzen(M, sym=True):
    """Return a Parzen window.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an empty
        array is returned.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.

    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).

    References
    ----------
    .. [1] E. Parzen, "Mathematical Considerations in the Estimation of
           Spectra", Technometrics,  Vol. 3, No. 2 (May, 1961), pp. 167-190

    Examples
    --------
    Plot the window and its frequency response:

    >>> from scipy import signal
    >>> from scipy.fftpack import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = signal.parzen(51)
    >>> plt.plot(window)
    >>> plt.title("Parzen window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title("Frequency response of the Parzen window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")

    """
    if _len_guards(M):
        return np.ones(M)
    M, needs_trunc = _extend(M, sym)

    n = np.arange(-(M - 1) / 2.0, (M - 1) / 2.0 + 0.5, 1.0)
    na = np.extract(n < -(M - 1) / 4.0, n)
    nb = np.extract(abs(n) <= (M - 1) / 4.0, n)
    wa = 2 * (1 - np.abs(na) / (M / 2.0)) ** 3.0
    wb = (1 - 6 * (np.abs(nb) / (M / 2.0)) ** 2.0 +
          6 * (np.abs(nb) / (M / 2.0)) ** 3.0)
    w = np.r_[wa, wb, wa[::-1]]

    return _truncate(w, needs_trunc)
