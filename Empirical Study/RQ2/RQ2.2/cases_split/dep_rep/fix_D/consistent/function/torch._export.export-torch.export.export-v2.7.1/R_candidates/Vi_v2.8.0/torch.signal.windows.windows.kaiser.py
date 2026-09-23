@_add_docstr(
    r"""
Computes the Kaiser window.

The Kaiser window is defined as follows:

.. math::
    w_n = I_0 \left( \beta \sqrt{1 - \left( {\frac{n - N/2}{N/2}} \right) ^2 } \right) / I_0( \beta )

where ``I_0`` is the zeroth order modified Bessel function of the first kind (see :func:`torch.special.i0`), and
``N = M - 1 if sym else M``.
    """,
    r"""

{normalization}

Args:
    {M}

Keyword args:
    beta (float, optional): shape parameter for the window. Must be non-negative. Default: 12.0
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric gaussian window with a standard deviation of 1.0.
    >>> torch.signal.windows.kaiser(5)
    tensor([4.0065e-05, 2.1875e-03, 4.3937e-02, 3.2465e-01, 8.8250e-01, 8.8250e-01, 3.2465e-01, 4.3937e-02, 2.1875e-03, 4.0065e-05])
    >>> # Generates a periodic gaussian window and standard deviation equal to 0.9.
    >>> torch.signal.windows.kaiser(5, sym=False,std=0.9)
    tensor([1.9858e-07, 5.1365e-05, 3.8659e-03, 8.4658e-02, 5.3941e-01, 1.0000e+00, 5.3941e-01, 8.4658e-02, 3.8659e-03, 5.1365e-05])
""".format(
        **window_common_args,
    ),
)
def kaiser(
    M: int,
    *,
    beta: float = 12.0,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("kaiser", M, dtype, layout)

    if beta < 0:
        raise ValueError(f"beta must be non-negative, got: {beta} instead.")

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if M == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    # Avoid NaNs by casting `beta` to the appropriate dtype.
    beta = torch.tensor(beta, dtype=dtype, device=device)

    start = -beta
    constant = 2.0 * beta / (M if not sym else M - 1)
    end = torch.minimum(beta, start + (M - 1) * constant)

    k = torch.linspace(
        start=start,
        end=end,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.i0(torch.sqrt(beta * beta - torch.pow(k, 2))) / torch.i0(beta)
