import tensorflow as tf
from keras.layers.preprocessing.category_crossing import CategoryCrossing
import inspect

def main():
    # Simulate input data
    data = tf.constant([["A", "B"], ["C", "D"]], dtype=tf.string)
    
    # Create a CategoryCrossing layer
    category_crossing_layer = CategoryCrossing()
    
    # Call the layer on the data
    result = category_crossing_layer(data)
    print("CategoryCrossing result:", result.numpy())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(CategoryCrossing))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
