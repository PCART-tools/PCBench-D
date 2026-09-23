def sample_inputs_foreach(self, device, dtype, N, *, noncontiguous=False, same_size=False):
    if same_size:
        return [make_tensor((N, N), device, dtype, noncontiguous=noncontiguous) for _ in range(N)]
    else:
        return [make_tensor((N - i, N - i), device, dtype, noncontiguous=noncontiguous) for i in range(N)]
