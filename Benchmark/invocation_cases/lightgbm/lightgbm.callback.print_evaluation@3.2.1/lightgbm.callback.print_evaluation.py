import lightgbm as lgb
import inspect
import numpy as np

def main():
    # Simulate training data
    train_data = lgb.Dataset(np.array([[1, 2], [3, 4]], dtype=np.float32), label=np.array([0, 1], dtype=np.float32))
    params = {'objective': 'binary', 'verbose': -1}
    
    # Train a simple model
    bst = lgb.train(params, train_data, num_boost_round=10, callbacks=[lgb.callback.print_evaluation()])
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(lgb.callback.print_evaluation))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()