def istft(input: Tensor, n_fft: int, hop_length: Optional[int] = None,
          win_length: Optional[int] = None, window: Optional[Tensor] = None,
          center: bool = True, normalized: bool = False,
          onesided: Optional[bool] = None, length: Optional[int] = None,
          return_complex: bool = False) -> Tensor:
    r"""Inverse short time Fourier Transform. This is expected to be the inverse of :func:`~torch.stft`.
    It has the same parameters (+ additional optional parameter of :attr:`length`) and it should return the
    least squares estimation of the original signal. The algorithm will check using the NOLA condition (
    nonzero overlap).

    Important consideration in the parameters :attr:`window` and :attr:`center` so that the envelop
    created by the summation of all the windows is never zero at certain point in time. Specifically,
    :math:`\sum_{t=-\infty}^{\infty} |w|^2[n-t\times hop\_length] \cancel{=} 0`.

    Since :func:`~torch.stft` discards elements at the end of the signal if they do not fit in a frame,
    ``istft`` may return a shorter signal than the original signal (can occur if :attr:`center` is False
    since the signal isn't padded). If `length` is given in the arguments and is longer than expected,
    ``istft`` will pad zeros to the end of the returned signal.

    If :attr:`center` is ``True``, then there will be padding e.g. ``'constant'``, ``'reflect'``, etc.
    Left padding can be trimmed off exactly because they can be calculated but right padding cannot be
    calculated without additional information.

    Example: Suppose the last window is:
    ``[17, 18, 0, 0, 0]`` vs ``[18, 0, 0, 0, 0]``

    The :attr:`n_fft`, :attr:`hop_length`, :attr:`win_length` are all the same which prevents the calculation
    of right padding. These additional values could be zeros or a reflection of the signal so providing
    :attr:`length` could be useful. If :attr:`length` is ``None`` then padding will be aggressively removed
    (some loss of signal).

    [1] D. W. Griffin and J. S. Lim, "Signal estimation from modified short-time Fourier transform,"
    IEEE Trans. ASSP, vol.32, no.2, pp.236-243, Apr. 1984.

    Args:
        input (Tensor): The input tensor. Expected to be output of :func:`~torch.stft`,
            can either be complex (``channel``, ``fft_size``, ``n_frame``), or real
            (``channel``, ``fft_size``, ``n_frame``, 2) where the ``channel``
            dimension is optional.

            .. deprecated:: 1.8.0
               Real input is deprecated, use complex inputs as returned by
               ``stft(..., return_complex=True)`` instead.
        n_fft (int): Size of Fourier transform
        hop_length (Optional[int]): The distance between neighboring sliding window frames.
            (Default: ``n_fft // 4``)
        win_length (Optional[int]): The size of window frame and STFT filter. (Default: ``n_fft``)
        window (Optional[torch.Tensor]): The optional window function.
            (Default: ``torch.ones(win_length)``)
        center (bool): Whether :attr:`input` was padded on both sides so that the :math:`t`-th frame is
            centered at time :math:`t \times \text{hop\_length}`.
            (Default: ``True``)
        normalized (bool): Whether the STFT was normalized. (Default: ``False``)
        onesided (Optional[bool]): Whether the STFT was onesided.
            (Default: ``True`` if ``n_fft != fft_size`` in the input size)
        length (Optional[int]): The amount to trim the signal by (i.e. the
            original signal length). (Default: whole signal)
        return_complex (Optional[bool]):
            Whether the output should be complex, or if the input should be
            assumed to derive from a real signal and window.
            Note that this is incompatible with ``onesided=True``.
            (Default: ``False``)

    Returns:
        Tensor: Least squares estimation of the original signal of size (..., signal_length)
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            istft, (input,), input, n_fft, hop_length=hop_length, win_length=win_length,
            window=window, center=center, normalized=normalized, onesided=onesided,
            length=length, return_complex=return_complex)

    return _VF.istft(input, n_fft, hop_length, win_length, window, center,  # type: ignore[attr-defined]
                     normalized, onesided, length, return_complex)
