def run_benchmark(name: str, function: object, dtype: torch.dtype, seed: int, device: str, samples: int,
                  probability_regular: float):
    cuda = device == 'cuda'
    spectral_fuzzer = SpectralOpFuzzer(seed=seed, dtype=dtype, cuda=cuda,
                                       probability_regular=probability_regular)
    results = []
    for tensors, tensor_params, params in spectral_fuzzer.take(samples):
        shape = [params['k0'], params['k1'], params['k2']][:params['ndim']]
        str_shape = ' x '.join([f"{s:<4}" for s in shape])
        sub_label = f"{str_shape} {'' if tensor_params['x']['is_contiguous'] else '(discontiguous)'}"
        for dim in _dim_options(params['ndim']):
            for nthreads in (1, 4, 16) if not cuda else (1,):
                measurement = benchmark.Timer(
                    stmt='func(x, dim=dim)',
                    globals={'func': function, 'x': tensors['x'], 'dim': dim},
                    label=f"{name}_{device}",
                    sub_label=sub_label,
                    description=f"dim={dim}",
                    num_threads=nthreads,
                ).blocked_autorange(min_run_time=1)
                measurement.metadata = {
                    'name': name,
                    'device': device,
                    'dim': dim,
                    'shape': shape,
                }
                measurement.metadata.update(tensor_params['x'])
                results.append(measurement)
    return results
