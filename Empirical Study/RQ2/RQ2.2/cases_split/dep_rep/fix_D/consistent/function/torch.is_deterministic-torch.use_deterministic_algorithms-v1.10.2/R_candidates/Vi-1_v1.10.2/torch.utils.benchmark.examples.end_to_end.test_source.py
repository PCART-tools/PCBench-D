def test_source(envs):
    """Ensure that subprocess"""
    for env in envs:
        result = run(f"source activate {env}")
        if result.returncode != 0:
            raise ValueError(f"Failed to source environment `{env}`")
