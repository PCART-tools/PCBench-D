        def reference_fn(i, p, m):
            # For bad reasons this would create LongTensors that requires gradients
            # Remove requires_grad to avoid this
            for p in m.parameters():
                p.requires_grad_(False)
            m._apply(lambda t: t.long())
            input = i.long()
            out = m.forward(input)
            return out
