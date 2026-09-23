    def check_close(a, b):
        if isinstance(a, (list, tuple)):
            for ae, be in zip(a, b):
                check_close(ae, be)
        else:
            print(torch.max(torch.abs(a - b)))
            assert torch.allclose(a, b)
