    def forward(self, visual_feats, visual_pos):
        x = self.visn_fc(visual_feats)
        x = self.visn_layer_norm(x)
        y = self.box_fc(visual_pos)
        y = self.box_layer_norm(y)
        output = (x + y) / 2

        output = self.dropout(output)
        return output
