import torch
import inspect
from torch.autograd.gradcheck import get_numerical_jacobian

def main():
    def simple_function(x):
        return x
    x = torch.tensor([1.0, 2.0, 3.0], dtype=torch.double)
    numerical_jacobian = get_numerical_jacobian(
        simple_function,
        x,
        eps=1e-6
    )
    print("Numerical Jacobian:")
    print(numerical_jacobian)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(get_numerical_jacobian))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()