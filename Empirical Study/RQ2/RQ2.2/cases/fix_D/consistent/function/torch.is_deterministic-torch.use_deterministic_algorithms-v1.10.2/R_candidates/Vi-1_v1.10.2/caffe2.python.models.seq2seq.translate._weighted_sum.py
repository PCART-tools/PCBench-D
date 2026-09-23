def _weighted_sum(model, values, weight, output_name):
    values_weights = zip(values, [weight] * len(values))
    values_weights_flattened = [x for v_w in values_weights for x in v_w]
    return model.net.WeightedSum(
        values_weights_flattened,
        output_name,
    )
