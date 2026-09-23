def generate_redistribute_costs(
    src_strategy: OpStrategy, dst_spec: DTensorSpec
) -> list[float]:
    redistribute_costs: list[float] = [
        redistribute_cost(strat.output_spec, dst_spec)
        for strat in src_strategy.strategies
    ]

    return redistribute_costs
