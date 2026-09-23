def gen_abtest_config(control: str, treatment: str, models: List[str]) -> str:
    d = {}
    d["control"] = control
    d["treatment"] = treatment
    config = ABTEST_CONFIG_TEMPLATE.format(**d)
    if models == ["ALL"]:
        return config + "\n"
    for model in models:
        config = f"{config}\n  - {model}"
    config = config + "\n"
    return config
