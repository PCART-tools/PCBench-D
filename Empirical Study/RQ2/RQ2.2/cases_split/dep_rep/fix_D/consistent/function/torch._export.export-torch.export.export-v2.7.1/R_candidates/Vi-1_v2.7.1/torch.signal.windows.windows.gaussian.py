@_add_docstr(
    r"""
Computes a window with a gaussian waveform.

The gaussian window is defined as follows:

.. math::
    w_n = \exp{\left(-\left(\frac{n}{2\sigma}\right)^2\right)}
    """,
    r"""

{normalization}

Args:
    {M}

Keyword args:
    std (float, optional): the standard deviation of the gaussian. It controls how narrow or wide the window is.
        Default: 1.0.
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric gaussian window with a standard deviation of 1.0.
    >>> torch.signal.windows.gaussian(10)
    tensor([4.0065e-05, 2.1875e-03, 4.3937e-02, 3.2465e-01, 8.8250e-01, 8.8250e-01, 3.2465e-01, 4.3937e-02, 2.1875e-03, 4.0065e-05])

    >>> # Generates a periodic gaussian window and standard deviation equal to 0.9.
    >>> torch.signal.windows.gaussian(10, sym=False,std=0.9)
    tensor([1.9858e-07, 5.1365e-05, 3.8659e-03, 8.4658e-02, 5.3941e-01, 1.0000e+00, 5.3941e-01, 8.4658e-02, 3.8659e-03, 5.1365e-05])
""".format(
        **window_common_args,
    ),
)
def gaussian(
    M: int,
    *,
    std: float = 1.0,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("gaussian", M, dtype, layout)

    if std <= 0:
        raise ValueError(f"Standard deviation must be positive, got: {std} instead.")

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    start = -(M if not sym and M > 1 else M - 1) / 2.0

    constant = 1 / (std * sqrt(2))

    k = torch.linspace(
        start=start * constant,
        end=(start + (M - 1)) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.exp(-(k**2))
