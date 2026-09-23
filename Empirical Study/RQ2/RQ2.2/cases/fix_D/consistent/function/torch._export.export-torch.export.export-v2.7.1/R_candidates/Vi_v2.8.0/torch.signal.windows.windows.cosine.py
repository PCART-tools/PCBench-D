@_add_docstr(
    r"""
Computes a window with a simple cosine waveform, following the same implementation as SciPy.
This window is also known as the sine window.

The cosine window is defined as follows:

.. math::
    w_n = \sin\left(\frac{\pi (n + 0.5)}{M}\right)

This formula differs from the typical cosine window formula by incorporating a 0.5 term in the numerator,
which shifts the sample positions. This adjustment results in a window that starts and ends with non-zero values.

""",
    r"""

{normalization}

Args:
    {M}

Keyword args:
    {sym}
    {dtype}
    {layout}
    {device}
    {requires_grad}

Examples::

    >>> # Generates a symmetric cosine window.
    >>> torch.signal.windows.cosine(10)
    tensor([0.1564, 0.4540, 0.7071, 0.8910, 0.9877, 0.9877, 0.8910, 0.7071, 0.4540, 0.1564])

    >>> # Generates a periodic cosine window.
    >>> torch.signal.windows.cosine(10, sym=False)
    tensor([0.1423, 0.4154, 0.6549, 0.8413, 0.9595, 1.0000, 0.9595, 0.8413, 0.6549, 0.4154])
""".format(
        **window_common_args,
    ),
)
def cosine(
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

    _window_function_checks("cosine", M, dtype, layout)

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    start = 0.5
    constant = torch.pi / (M + 1 if not sym and M > 1 else M)

    k = torch.linspace(
        start=start * constant,
        end=(start + (M - 1)) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.sin(k)
