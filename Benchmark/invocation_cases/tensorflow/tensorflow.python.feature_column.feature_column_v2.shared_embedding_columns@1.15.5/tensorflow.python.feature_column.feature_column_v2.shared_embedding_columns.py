import tensorflow as tf
import inspect

def main():
    categorical_column_a = tf.feature_column.categorical_column_with_vocabulary_list(
        key='feature_a', vocabulary_list=['a', 'b', 'c'])
    categorical_column_b = tf.feature_column.categorical_column_with_vocabulary_list(
        key='feature_b', vocabulary_list=['x', 'y', 'z'])
    
    shared_embedding = tf.feature_column.shared_embedding_columns(
        [categorical_column_a, categorical_column_b], dimension=8)
    
    print("shared_embedding result:", shared_embedding)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.feature_column.shared_embedding_columns))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()