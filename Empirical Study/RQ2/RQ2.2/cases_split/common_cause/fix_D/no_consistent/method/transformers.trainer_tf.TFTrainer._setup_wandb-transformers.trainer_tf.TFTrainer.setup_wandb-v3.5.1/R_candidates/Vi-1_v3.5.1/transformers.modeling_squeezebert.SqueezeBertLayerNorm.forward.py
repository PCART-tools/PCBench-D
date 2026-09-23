    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = nn.LayerNorm.forward(self, x)
        return x.permute(0, 2, 1)
