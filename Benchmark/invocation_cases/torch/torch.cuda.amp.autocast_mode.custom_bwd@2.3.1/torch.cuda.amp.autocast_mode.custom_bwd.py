import torch
import inspect
from torch.cuda.amp import custom_fwd, custom_bwd

def main():
    class CustomFunction(torch.autograd.Function):
        @staticmethod
        @custom_fwd(cast_inputs=torch.float16)
        def forward(ctx, x):
            ctx.save_for_backward(x)
            return x * x

        @staticmethod
        @custom_bwd
        def backward(ctx, grad_output):
            x, = ctx.saved_tensors
            return grad_output * 2 * x
    if not torch.cuda.is_available():
        print("CUDA not available, skipping test.")
        return

    x = torch.tensor([1.0, 2.0, 3.0],
                     device="cuda",
                     requires_grad=True)

    with torch.cuda.amp.autocast():
        y = CustomFunction.apply(x)
        loss = y.sum()

    loss.backward()

    print("x:", x)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(custom_bwd))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()