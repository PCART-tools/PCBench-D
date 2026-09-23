def create_offsets(x, m1_size, m2_size, offs_size):
    m1_is_2d = len(m1_size) == 2
    m2_is_2d = len(m2_size) == 2
    if m1_is_2d:
        if m2_is_2d:
            k = V.graph.sizevars.size_hint(m1_size[1])
            noffs = V.graph.sizevars.size_hint(offs_size[0])
            step = k / noffs
            return torch.linspace(
                step, k, noffs, dtype=x.get_dtype(), device=x.get_device()
            )

        else:
            m = V.graph.sizevars.size_hint(m1_size[0])
            noffs = V.graph.sizevars.size_hint(offs_size[0])
            step = m / noffs
            return torch.linspace(
                step, m, noffs, dtype=x.get_dtype(), device=x.get_device()
            )
    else:
        if m2_is_2d:
            n = V.graph.sizevars.size_hint(m2_size[0])
            noffs = V.graph.sizevars.size_hint(offs_size[0])
            step = n / noffs
            return torch.linspace(
                step, n, noffs, dtype=x.get_dtype(), device=x.get_device()
            )
        else:
            return None
