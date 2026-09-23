    def get_qa_logit_layer(self) -> nn.Module:
        """
        Returns the the linear layer that produces question answering logits.

        Returns:
            :obj:`nn.Module`: A torch module mapping the question answering prediction hidden states or :obj:`None` if
                LXMERT does not have a visual answering head.
        """
        if hasattr(self, "answer_head"):
            return self.answer_head.logit_fc[-1]
