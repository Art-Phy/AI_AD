from collections import Counter

from aidetect.ml_training import split_dataset



def test_split_dataset_preserves_size_and_balance():
    X = [[float(i)] for i in range(60)]
    y = [0] * 30 + [1] * 30

    X_train, X_test, y_train, y_test = split_dataset(X, y)

    assert len(X_train) == 48
    assert len(X_test) == 12
    assert len(y_train) == 48
    assert len(y_test) == 12

    assert Counter(y_train) == {0: 24, 1: 24}
    assert Counter(y_test) == {0: 6, 1: 6}
