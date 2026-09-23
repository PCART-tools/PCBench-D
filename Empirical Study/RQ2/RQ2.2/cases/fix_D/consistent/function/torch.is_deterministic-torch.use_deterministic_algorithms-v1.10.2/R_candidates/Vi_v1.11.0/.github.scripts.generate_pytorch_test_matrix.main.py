def main() -> None:
    INCLUDE_DEFAULT_TEST = True
    TEST_RUNNER_TYPE = os.getenv('TEST_RUNNER_TYPE')
    assert TEST_RUNNER_TYPE is not None
    RUN_SMOKE_TESTS_ONLY_ON_PR = os.getenv('RUN_SMOKE_TESTS_ONLY_ON_PR')
    RUN_SMOKE_TESTS = RUN_SMOKE_TESTS_ONLY_ON_PR == "true" and not run_as_if_on_trunk()
    NUM_TEST_SHARDS_ON_PULL_REQUEST = os.getenv('NUM_TEST_SHARDS_ON_PULL_REQUEST')
    NUM_TEST_SHARDS = int(os.getenv('NUM_TEST_SHARDS', '0'))
    if not run_as_if_on_trunk() and NUM_TEST_SHARDS_ON_PULL_REQUEST:
        NUM_TEST_SHARDS = int(NUM_TEST_SHARDS_ON_PULL_REQUEST)
    MULTIGPU_RUNNER_TYPE = os.getenv('MULTIGPU_RUNNER_TYPE')
    DISTRIBUTED_GPU_RUNNER_TYPE = os.getenv('DISTRIBUTED_GPU_RUNNER_TYPE', TEST_RUNNER_TYPE)
    NOGPU_RUNNER_TYPE = os.getenv('NOGPU_RUNNER_TYPE')
    configs: Dict[str, Config] = {}
    if os.getenv('ENABLE_JIT_LEGACY_TEST'):
        configs['jit_legacy'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    if MULTIGPU_RUNNER_TYPE is not None and os.getenv('ENABLE_MULTIGPU_TEST'):
        configs['multigpu'] = {'num_shards': 1, 'runner': MULTIGPU_RUNNER_TYPE}
    if NOGPU_RUNNER_TYPE is not None:
        if os.getenv('ENABLE_NOGPU_NO_AVX_TEST'):
            configs['nogpu_NO_AVX'] = {'num_shards': 1, 'runner': NOGPU_RUNNER_TYPE}
        if os.getenv('ENABLE_NOGPU_NO_AVX2_TEST'):
            configs['nogpu_NO_AVX2'] = {'num_shards': 1, 'runner': NOGPU_RUNNER_TYPE}
        if os.getenv('ENABLE_FORCE_ON_CPU_TEST'):
            configs['force_on_cpu'] = {'num_shards': 1, 'runner': NOGPU_RUNNER_TYPE}
    if os.getenv('ENABLE_DISTRIBUTED_TEST'):
        configs['distributed'] = {
            'num_shards': 1,
            'runner': DISTRIBUTED_GPU_RUNNER_TYPE if "cuda" in str(BUILD_ENVIRONMENT) else TEST_RUNNER_TYPE
        }
    if os.getenv('ENABLE_FX2TRT_TEST'):
        configs['fx2trt'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    if os.getenv('ENABLE_SLOW_TEST'):
        configs['slow'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    if os.getenv('ENABLE_DOCS_TEST'):
        configs['docs_test'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    if os.getenv('ENABLE_BACKWARDS_COMPAT_TEST'):
        configs['backwards_compat'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    if os.getenv('ENABLE_XLA_TEST'):
        configs['xla'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
        INCLUDE_DEFAULT_TEST = False
    if os.getenv('ENABLE_NOARCH_TEST'):
        configs['noarch'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    if RUN_SMOKE_TESTS:
        configs['smoke_tests'] = {'num_shards': 1, 'runner': TEST_RUNNER_TYPE}
    matrix = {
        'include': [
            {
                'config': 'default',
                'shard': shard,
                'num_shards': NUM_TEST_SHARDS,
                'runner': TEST_RUNNER_TYPE,
            }
            for shard in range(1, NUM_TEST_SHARDS + 1)
            if INCLUDE_DEFAULT_TEST
        ] + [
            {
                'config': name,
                'shard': shard,
                'num_shards': config['num_shards'],
                'runner': config['runner'],
            }
            for name, config in configs.items()
            for shard in range(1, config['num_shards'] + 1)
        ]
    }
    render_matrix = {'config': list(dict.fromkeys(x['config'] for x in matrix['include']))}
    print(json.dumps({'matrix': matrix, 'render-matrix': render_matrix}, indent=2))
    print(f'::set-output name=matrix::{json.dumps(matrix)}')
    print(f'::set-output name=render-matrix::{json.dumps(render_matrix)}')
    print(f'::set-output name=ignore-disabled-issues::{get_disabled_issues()}')
