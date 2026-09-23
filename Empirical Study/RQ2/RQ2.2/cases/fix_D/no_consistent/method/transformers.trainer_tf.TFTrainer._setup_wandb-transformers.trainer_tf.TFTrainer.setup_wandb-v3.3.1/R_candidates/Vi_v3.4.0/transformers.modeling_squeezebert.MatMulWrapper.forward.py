    def forward(self, mat1, mat2):
        """

        :param inputs: two torch tensors
        :return: matmul of these tensors

        Here are the typical dimensions found in BERT (the B is optional)
            mat1.shape: [B, <optional extra dims>, M, K]
            mat2.shape: [B, <optional extra dims>, K, N]
            output shape: [B, <optional extra dims>, M, N]
        """
        return torch.matmul(mat1, mat2)
