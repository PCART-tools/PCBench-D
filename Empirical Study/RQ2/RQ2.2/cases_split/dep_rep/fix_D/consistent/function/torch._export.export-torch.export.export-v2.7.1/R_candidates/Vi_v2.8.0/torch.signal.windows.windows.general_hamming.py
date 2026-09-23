@_add_docstr(
    r"""
Computes the general Hamming window.

The general Hamming window is defined as follows:

.. math::
    w_n = \alpha - (1 - \alpha) \cos{ \left( \frac{2 \pi n}{M-1} \right)}
    """,
    r"""

{normalization}

Arguments:
    {M}

Keyword args:
    alpha (float, optional): the window coefficient. Default: 0.54.
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric Hamming window with the general Hamming window.
    >>> torch.signal.windows.general_hamming(10, sym=True)
    tensor([0.0800, 0.1876, 0.4601, 0.7700, 0.9723, 0.9723, 0.7700, 0.4601, 0.1876, 0.0800])

    >>> # Generates a periodic Hann window with the general Hamming window.
    >>> torch.signal.windows.general_hamming(10, alpha=0.5, sym=False)
    tensor([0.0000, 0.0955, 0.3455, 0.6545, 0.9045, 1.0000, 0.9045, 0.6545, 0.3455, 0.0955])
""".format(
        **window_common_args
    ),
)
def general_hamming(
    M,
    *,
    alpha: float = 0.54,
    sym: bool = True,
    dtype: Optional[torch.dtype] = None,
    layout: torch.layout = torch.strided,
    device: Optional[torch.device] = None,
    requires_grad: bool = False,
) -> Tensor:
    return general_cosine(
        M,
        a=[alpha, 1.0 - alpha],
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )
