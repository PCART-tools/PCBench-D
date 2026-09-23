def verify_split_model(
    mod: torch.fx.GraphModule, acc_submodule_keyword: str = ACC_SUBMODULE_PREFIX, expected_number: int = 1,
) -> None:
    acc_submodule_num = 0
    for name, _ in mod.named_children():
        if name.startswith(acc_submodule_keyword):
            acc_submodule_num = acc_submodule_num + 1

    if acc_submodule_num < expected_number:
        raise RuntimeError(ERROR_MSG_NO_ACC_MODULE)
    elif acc_submodule_num > expected_number:
        raise RuntimeError(ERROR_MSG_MULTI_ACC_MODULES)
