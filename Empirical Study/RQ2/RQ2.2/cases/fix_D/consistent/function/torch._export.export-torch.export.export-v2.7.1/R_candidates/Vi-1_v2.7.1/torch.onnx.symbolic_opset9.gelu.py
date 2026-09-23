@_onnx_symbolic("aten::gelu")
@symbolic_helper.parse_args("v", "s")
def gelu(g: jit_utils.GraphContext, self: torch._C.Value, approximate: str = "none"):
    if approximate == "tanh":
        kBeta = math.sqrt(2 / math.pi)
        kKappa = 0.044715

        beta = torch.tensor(kBeta, dtype=torch.double)
        kappa = torch.tensor(kKappa, dtype=torch.double)
        one = torch.tensor(1.0, dtype=torch.double)
        half = torch.tensor(0.5, dtype=torch.double)

        self_cube = mul(g, self, mul(g, self, self))
        inner = mul(g, beta, add(g, self, mul(g, kappa, self_cube)))
        return mul(g, half, mul(g, self, add(g, one, g.op("Tanh", inner))))
    else:
        _sqrt2 = 1.4142135623730951
        erf = g.op("Erf", g.op("Div", self, torch.tensor(_sqrt2, dtype=torch.double)))
        erf_plusone = add(
            g, erf, g.op("Constant", value_t=torch.tensor(1, dtype=torch.double))
        )
        return mul(
            g,
            mul(g, self, erf_plusone),
            g.op("Constant", value_t=torch.tensor(0.5, dtype=torch.double)),
        )
