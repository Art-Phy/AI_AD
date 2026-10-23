from collections import Counter

from sklearn.linear_model import LogisticRegression
from aidetect.ml_training import split_dataset, train_logistic_regression



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



def test_train_logistic_regression():
    X = [
        [1.0, 1.0],
        [1.1, 1.2],
        [0.9, 1.1],
        [4.0, 4.0],
        [4.1, 3.9],
        [3.9, 4.2],
    ]

    y = [0, 0, 0, 1, 1, 1]

    model = train_logistic_regression(X, y)

    assert isinstance(model, LogisticRegression)
    assert hasattr(model, "coef_")
    assert hasattr(model, "intercept_")
