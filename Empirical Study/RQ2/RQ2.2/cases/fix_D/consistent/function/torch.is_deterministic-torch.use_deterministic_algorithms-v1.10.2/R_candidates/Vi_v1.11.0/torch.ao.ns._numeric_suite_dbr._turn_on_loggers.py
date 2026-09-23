def _turn_on_loggers(name: str, model: torch.nn.Module) -> None:
    for _, module in model.named_modules():
        if isinstance(module, AutoQuantizationState):
            module.logging_model_name = name
            module.log_op_outputs = True
