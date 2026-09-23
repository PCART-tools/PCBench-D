@_add_docstr(
    r"""
Computes the minimum 4-term Blackman-Harris window according to Nuttall.

.. math::
    w_n = 1 - 0.36358 \cos{(z_n)} + 0.48917 \cos{(2z_n)} - 0.13659 \cos{(3z_n)} + 0.01064 \cos{(4z_n)}

where :math:`z_n = \frac{2 \pi n}{M}`.
    """,
    """

{normalization}

Arguments:
    {M}

Keyword args:
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

References::

    - A. Nuttall, "Some windows with very good sidelobe behavior,"
      IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 29, no. 1, pp. 84-91,
      Feb 1981. https://doi.org/10.1109/TASSP.1981.1163506

    - Heinzel G. et al., "Spectrum and spectral density estimation by the Discrete Fourier transform (DFT),
      including a comprehensive list of window functions and some new flat-top windows",
      February 15, 2002 https://holometer.fnal.gov/GH_FFT.pdf

Examples::

    >>> # Generates a symmetric Nutall window.
    >>> torch.signal.windows.general_hamming(5, sym=True)
    tensor([3.6280e-04, 2.2698e-01, 1.0000e+00, 2.2698e-01, 3.6280e-04])

    >>> # Generates a periodic Nuttall window.
    >>> torch.signal.windows.general_hamming(5, sym=False)
    tensor([3.6280e-04, 1.1052e-01, 7.9826e-01, 7.9826e-01, 1.1052e-01])
""".format(
        **window_common_args
    ),
)
def nuttall(
    M: int,
    *,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    return general_cosine(
        M,
        a=[0.3635819, 0.4891775, 0.1365995, 0.0106411],
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )
