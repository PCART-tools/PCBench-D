def linspace(g, start, end, steps, dtype, layout, device, pin_memory):
    step = div(g, sub(g, end, start), sub(g, steps, g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))))
    end_epsilon = g.op("Add", step, end)
    return sym_help._arange_helper(g, start, end_epsilon, step, dtype, None, None, None)
