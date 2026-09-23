@_add_docstr(
    r"""
Computes the Blackman window.

The Blackman window is defined as follows:

.. math::
    w_n = 0.42 - 0.5 \cos \left( \frac{2 \pi n}{M - 1} \right) + 0.08 \cos \left( \frac{4 \pi n}{M - 1} \right)
    """,
    r"""

{normalization}

Arguments:
    {M}

Keyword args:
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric Blackman window.
    >>> torch.signal.windows.blackman(5)
    tensor([-1.4901e-08,  3.4000e-01,  1.0000e+00,  3.4000e-01, -1.4901e-08])

    >>> # Generates a periodic Blackman window.
    >>> torch.signal.windows.blackman(5, sym=False)
    tensor([-1.4901e-08,  2.0077e-01,  8.4923e-01,  8.4923e-01,  2.0077e-01])
""".format(
        **window_common_args
    ),
)
def blackman(
    M: int,
    *,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("blackman", M, dtype, layout)

    return general_cosine(
        M,
        a=[0.42, 0.5, 0.08],
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )
