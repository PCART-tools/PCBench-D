    def cudnn_benchmark_configs(configs):
        return [(*config, dict(cudnn=False)) for config in configs]
