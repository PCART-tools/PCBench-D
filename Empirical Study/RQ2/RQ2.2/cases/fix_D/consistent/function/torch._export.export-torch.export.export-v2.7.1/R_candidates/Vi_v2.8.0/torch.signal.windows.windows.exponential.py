@_add_docstr(
    r"""
Computes a window with an exponential waveform.
Also known as Poisson window.

The exponential window is defined as follows:

.. math::
    w_n = \exp{\left(-\frac{|n - c|}{\tau}\right)}

where `c` is the ``center`` of the window.
    """,
    r"""

{normalization}

Args:
    {M}

Keyword args:
    center (float, optional): where the center of the window will be located.
        Default: `M / 2` if `sym` is `False`, else `(M - 1) / 2`.
    tau (float, optional): the decay value.
        Tau is generally associated with a percentage, that means, that the value should
        vary within the interval (0, 100]. If tau is 100, it is considered the uniform window.
        Default: 1.0.
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric exponential window of size 10 and with a decay value of 1.0.
    >>> # The center will be at (M - 1) / 2, where M is 10.
    >>> torch.signal.windows.exponential(10)
    tensor([0.0111, 0.0302, 0.0821, 0.2231, 0.6065, 0.6065, 0.2231, 0.0821, 0.0302, 0.0111])

    >>> # Generates a periodic exponential window and decay factor equal to .5
    >>> torch.signal.windows.exponential(10, sym=False,tau=.5)
    tensor([4.5400e-05, 3.3546e-04, 2.4788e-03, 1.8316e-02, 1.3534e-01, 1.0000e+00, 1.3534e-01, 1.8316e-02, 2.4788e-03, 3.3546e-04])
    """.format(
        **window_common_args
    ),
)
def exponential(
    M: int,
    *,
    center: Optional[float] = None,
    tau: float = 1.0,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("exponential", M, dtype, layout)

    if tau <= 0:
        raise ValueError(f"Tau must be positive, got: {tau} instead.")

    if sym and center is not None:
        raise ValueError("Center must be None for symmetric windows")

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if center is None:
        center = (M if not sym and M > 1 else M - 1) / 2.0

    constant = 1 / tau

    k = torch.linspace(
        start=-center * constant,
        end=(-center + (M - 1)) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.exp(-torch.abs(k))
