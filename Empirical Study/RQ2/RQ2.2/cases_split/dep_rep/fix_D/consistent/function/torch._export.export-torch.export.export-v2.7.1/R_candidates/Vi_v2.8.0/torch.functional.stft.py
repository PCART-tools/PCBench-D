def stft(
    input: Tensor,
    n_fft: int,
    hop_length: Optional[int] = None,
    win_length: Optional[int] = None,
    window: Optional[Tensor] = None,
    center: bool = True,
    pad_mode: str = "reflect",
    normalized: bool = False,
    onesided: Optional[bool] = None,
    return_complex: Optional[bool] = None,
    align_to_window: Optional[bool] = None,
) -> Tensor:
    r"""Short-time Fourier transform (STFT).

    .. warning::
        From version 1.8.0, :attr:`return_complex` must always be given
        explicitly for real inputs and `return_complex=False` has been
        deprecated. Strongly prefer `return_complex=True` as in a future
        pytorch release, this function will only return complex tensors.

        Note that :func:`torch.view_as_real` can be used to recover a real
        tensor with an extra last dimension for real and imaginary components.

    .. warning::
        From version 2.1, a warning will be provided if a :attr:`window` is
        not specified. In a future release, this attribute will be required.
        Not providing a window currently defaults to using a rectangular window,
        which may result in undesirable artifacts. Consider using tapered windows,
        such as :func:`torch.hann_window`.

    The STFT computes the Fourier transform of short overlapping windows of the
    input. This giving frequency components of the signal as they change over
    time. The interface of this function is modeled after (but *not* a drop-in
    replacement for) librosa_ stft function.

    .. _librosa: https://librosa.org/doc/latest/generated/librosa.stft.html

    Ignoring the optional batch dimension, this method computes the following
    expression:

    .. math::
        X[\omega, m] = \sum_{k = 0}^{\text{win\_length-1}}%
                            \text{window}[k]\ \text{input}[m \times \text{hop\_length} + k]\ %
                            \exp\left(- j \frac{2 \pi \cdot \omega k}{\text{n\_fft}}\right),

    where :math:`m` is the index of the sliding window, and :math:`\omega` is
    the frequency :math:`0 \leq \omega < \text{n\_fft}` for ``onesided=False``,
    or :math:`0 \leq \omega < \lfloor \text{n\_fft} / 2 \rfloor + 1` for ``onesided=True``.

    * :attr:`input` must be either a 1-D time sequence or a 2-D batch of time
      sequences.

    * If :attr:`hop_length` is ``None`` (default), it is treated as equal to
      ``floor(n_fft / 4)``.

    * If :attr:`win_length` is ``None`` (default), it is treated as equal to
      :attr:`n_fft`.

    * :attr:`window` can be a 1-D tensor of size :attr:`win_length`, e.g., from
      :meth:`torch.hann_window`. If :attr:`window` is ``None`` (default), it is
      treated as if having :math:`1` everywhere in the window. If
      :math:`\text{win\_length} < \text{n\_fft}`, :attr:`window` will be padded on
      both sides to length :attr:`n_fft` before being applied.

    * If :attr:`center` is ``True`` (default), :attr:`input` will be padded on
      both sides so that the :math:`t`-th frame is centered at time
      :math:`t \times \text{hop\_length}`. Otherwise, the :math:`t`-th frame
      begins at time  :math:`t \times \text{hop\_length}`.

    * :attr:`pad_mode` determines the padding method used on :attr:`input` when
      :attr:`center` is ``True``. See :meth:`torch.nn.functional.pad` for
      all available options. Default is ``"reflect"``.

    * If :attr:`onesided` is ``True`` (default for real input), only values for
      :math:`\omega` in :math:`\left[0, 1, 2, \dots, \left\lfloor
      \frac{\text{n\_fft}}{2} \right\rfloor + 1\right]` are returned because
      the real-to-complex Fourier transform satisfies the conjugate symmetry,
      i.e., :math:`X[m, \omega] = X[m, \text{n\_fft} - \omega]^*`.
      Note if the input or window tensors are complex, then :attr:`onesided`
      output is not possible.

    * If :attr:`normalized` is ``True`` (default is ``False``), the function
      returns the normalized STFT results, i.e., multiplied by :math:`(\text{frame\_length})^{-0.5}`.

    * If :attr:`return_complex` is ``True`` (default if input is complex), the
      return is a ``input.dim() + 1`` dimensional complex tensor. If ``False``,
      the output is a ``input.dim() + 2`` dimensional real tensor where the last
      dimension represents the real and imaginary components.

    Returns either a complex tensor of size :math:`(* \times N \times T)` if
    :attr:`return_complex` is true, or a real tensor of size :math:`(* \times N
    \times T \times 2)`. Where :math:`*` is the optional batch size of
    :attr:`input`, :math:`N` is the number of frequencies where STFT is applied
    and :math:`T` is the total number of frames used.

    .. warning::
      This function changed signature at version 0.4.1. Calling with the
      previous signature may cause error or return incorrect result.

    Args:
        input (Tensor): the input tensor of shape `(B?, L)` where `B?` is an optional
            batch dimension
        n_fft (int): size of Fourier transform
        hop_length (int, optional): the distance between neighboring sliding window
            frames. Default: ``None`` (treated as equal to ``floor(n_fft / 4)``)
        win_length (int, optional): the size of window frame and STFT filter.
            Default: ``None``  (treated as equal to :attr:`n_fft`)
        window (Tensor, optional): the optional window function.
            Shape must be 1d and `<= n_fft`
            Default: ``None`` (treated as window of all :math:`1` s)
        center (bool, optional): whether to pad :attr:`input` on both sides so
            that the :math:`t`-th frame is centered at time :math:`t \times \text{hop\_length}`.
            Default: ``True``
        pad_mode (str, optional): controls the padding method used when
            :attr:`center` is ``True``. Default: ``"reflect"``
        normalized (bool, optional): controls whether to return the normalized STFT results
             Default: ``False``
        onesided (bool, optional): controls whether to return half of results to
            avoid redundancy for real inputs.
            Default: ``True`` for real :attr:`input` and :attr:`window`, ``False`` otherwise.
        return_complex (bool, optional): whether to return a complex tensor, or
            a real tensor with an extra last dimension for the real and
            imaginary components.

            .. versionchanged:: 2.0
               ``return_complex`` is now a required argument for real inputs,
               as the default is being transitioned to ``True``.

            .. deprecated:: 2.0
               ``return_complex=False`` is deprecated, instead use ``return_complex=True``
               Note that calling :func:`torch.view_as_real` on the output will
               recover the deprecated output format.

    Returns:
        Tensor: A tensor containing the STFT result with shape `(B?, N, T, C?)` where
           - `B?` is an optional batch dimension from the input.
           - `N` is the number of frequency samples, `(n_fft // 2) + 1` for
             `onesided=True`, or otherwise `n_fft`.
           - `T` is the number of frames, `1 + L // hop_length`
             for `center=True`, or `1 + (L - n_fft) // hop_length` otherwise.
           - `C?` is an optional length-2 dimension of real and imaginary
             components, present when `return_complex=False`.

    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            stft,
            (input,),
            input,
            n_fft,
            hop_length=hop_length,
            win_length=win_length,
            window=window,
            center=center,
            pad_mode=pad_mode,
            normalized=normalized,
            onesided=onesided,
            return_complex=return_complex,
            align_to_window=align_to_window,
        )
    if center and align_to_window is not None:
        raise RuntimeError(
            "stft align_to_window should only be set when center = false"
        )
    # NOTE: Do not edit. This code will be removed once the forward-compatibility
    #       period is over for PR #73432
    if center:
        signal_dim = input.dim()
        extended_shape = [1] * (3 - signal_dim) + list(input.size())
        pad = int(n_fft // 2)
        input = F.pad(input.view(extended_shape), [pad, pad], pad_mode)
        input = input.view(input.shape[-signal_dim:])
    return _VF.stft(  # type: ignore[attr-defined]
        input,
        n_fft,
        hop_length,
        win_length,
        window,
        normalized,
        onesided,
        return_complex,
        align_to_window,
    )
