    def backward_pass(
        self,
        next_attn_output,
        hidden_states,
        grad_attn_output,
        grad_hidden_states,
        attention_mask=None,
        head_mask=None,
        buckets=None,
    ):
        # Implements the backward pass for reversible ResNets.
        # A good blog post on how this works can be found here:
        # Implementation of RevNet (see Fig. 6 in https://towardsdatascience.com/illustrating-the-reformer-393575ac6ba0)
        # This code is heavily inspired by https://github.com/lucidrains/reformer-pytorch/blob/master/reformer_pytorch/reversible.py

        with torch.enable_grad():
            next_attn_output.requires_grad = True

            # set seed to have correct dropout
            torch.manual_seed(self.feed_forward_seed)
            # g(Y_1)
            res_hidden_states = self.feed_forward(next_attn_output)
            res_hidden_states.backward(grad_hidden_states, retain_graph=True)

        with torch.no_grad():
            # X_2 = Y_2 - g(Y_1)
            hidden_states = hidden_states - res_hidden_states
            del res_hidden_states

            grad_attn_output = grad_attn_output + next_attn_output.grad
            next_attn_output.grad = None

        with torch.enable_grad():
            hidden_states.requires_grad = True

            # set seed to have correct dropout
            torch.manual_seed(self.attention_seed)
            # f(X_2)
            # use cached buckets for backprob if buckets not None for LSHSelfAttention
            output = self.attention(
                hidden_states=hidden_states,
                head_mask=head_mask,
                attention_mask=attention_mask,
                buckets=buckets,
            ).hidden_states
            output.backward(grad_attn_output, retain_graph=True)

        with torch.no_grad():
            # X_1 = Y_1 - f(X_2)
            attn_output = next_attn_output - output
            del output, next_attn_output

            grad_hidden_states = grad_hidden_states + hidden_states.grad
            hidden_states.grad = None
            hidden_states = hidden_states.detach()

        return ReformerBackwardOutput(
            attn_output=attn_output,
            hidden_states=hidden_states,
            grad_attn_output=grad_attn_output,
            grad_hidden_states=grad_hidden_states,
        )
