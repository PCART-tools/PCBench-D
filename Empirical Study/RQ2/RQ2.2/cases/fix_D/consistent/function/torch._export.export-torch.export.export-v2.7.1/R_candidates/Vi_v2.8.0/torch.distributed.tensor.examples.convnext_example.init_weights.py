@torch.no_grad()
def init_weights(m):
    if type(m) == nn.Conv2d or type(m) == nn.Linear:
        nn.init.ones_(m.weight)
        if m.bias is not None:
            nn.init.zeros_(m.bias)
