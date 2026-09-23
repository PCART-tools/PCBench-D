import torch
import inspect
from torch.autograd.gradcheck import get_analytical_jacobian

def main():
    def simple_func(x):
        return x ** 2
    x = torch.tensor([1.0, 2.0, 3.0],
                     dtype=torch.double,
                     requires_grad=True)
    output = simple_func(x)
    jacobian, reentrant, correct_grad_sizes, correct_grad_types = (
        get_analytical_jacobian(
            (x,),         
            output,        
            nondet_tol=0.0,
            grad_out=1.0
        )
    )

    print("Jacobian:")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(get_analytical_jacobian))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()