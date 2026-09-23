def print_params(stage, model_1, model_2, optim_1, optim_2):
    with FSDP.summon_full_params(model_1):
        with FSDP.summon_full_params(model_2):
            print(
                f"{stage} --- rank: {dist.get_rank()}\n"
                f"model.weight: {model_1.weight}\n"
                f"model_2.weight:{model_2.weight}\n"
                f"model.bias: {model_1.bias}\n"
                f"model_2.bias: {model_2.bias}\n"
            )

    print(
        f"{stage} --- rank: {dist.get_rank()}\n"
        f"optim exp_avg:{opt_at(optim_1, 0)['exp_avg']}\n"
        f"optim_2 exp_avg:{opt_at(optim_2, 0)['exp_avg']}\n"
        f"optim exp_avg_sq:{opt_at(optim_1, 0)['exp_avg_sq']}\n"
        f"optim_2 exp_avg_sq:{opt_at(optim_2, 0)['exp_avg_sq']}\n"
    )
