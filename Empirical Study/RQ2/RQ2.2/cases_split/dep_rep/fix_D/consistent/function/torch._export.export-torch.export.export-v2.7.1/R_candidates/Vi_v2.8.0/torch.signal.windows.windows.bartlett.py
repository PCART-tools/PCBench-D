@_add_docstr(
    r"""
Computes the Bartlett window.

The Bartlett window is defined as follows:

.. math::
    w_n = 1 - \left| \frac{2n}{M - 1} - 1 \right| = \begin{cases}
        \frac{2n}{M - 1} & \text{if } 0 \leq n \leq \frac{M - 1}{2} \\
        2 - \frac{2n}{M - 1} & \text{if } \frac{M - 1}{2} < n < M \\ \end{cases}
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

    >>> # Generates a symmetric Bartlett window.
    >>> torch.signal.windows.bartlett(10)
    tensor([0.0000, 0.2222, 0.4444, 0.6667, 0.8889, 0.8889, 0.6667, 0.4444, 0.2222, 0.0000])

    >>> # Generates a periodic Bartlett window.
    >>> torch.signal.windows.bartlett(10, sym=False)
    tensor([0.0000, 0.2000, 0.4000, 0.6000, 0.8000, 1.0000, 0.8000, 0.6000, 0.4000, 0.2000])
""".format(
        **window_common_args
    ),
)
def bartlett(
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

    _window_function_checks("bartlett", M, dtype, layout)

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if M == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    start = -1
    constant = 2 / (M if not sym else M - 1)

    k = torch.linspace(
        start=start,
        end=start + (M - 1) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return 1 - torch.abs(k)
