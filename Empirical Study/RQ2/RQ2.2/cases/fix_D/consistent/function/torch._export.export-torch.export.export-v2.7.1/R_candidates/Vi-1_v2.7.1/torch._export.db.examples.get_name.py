    def get_name(case):
        model = case.model
        if isinstance(model, torch.nn.Module):
            model = type(model)
        return model.__name__
