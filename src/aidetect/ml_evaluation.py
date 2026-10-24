from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from aidetect.ml_training import train_logistic_regression



def evaluate_model(
    model,
    X_test: list[list[float]],
    y_test: list[int],
) -> dict:
    y_pred = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "predictions": [int(value) for value in y_pred],
    }



def cross_validate_model(
    X: list[list[float]],
    y: list[int],
    n_splits: int = 5,
    random_state: int = 42,
) -> dict:
    splitter = StratifiedKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )

    fold_results = []

    for train_indices, test_indices in splitter.split(X, y):
        X_train = [X[index] for index in train_indices]
        X_test = [X[index] for index in test_indices]
        y_train = [y[index] for index in train_indices]
        y_test = [y[index] for index in test_indices]

        model = train_logistic_regression(X_train, y_train)
        result = evaluate_model(model, X_test, y_test)

        fold_results.append(result)


    accuracies = [result["accuracy"] for result in fold_results]
    precisions = [result["precision"] for result in fold_results]
    recalls = [result["recall"] for result in fold_results]
    f1_scores = [result["f1"] for result in fold_results]

    return {
        "folds": fold_results,
        "mean_accuracy": sum(accuracies) / len(accuracies),
        "mean_precision": sum(precisions) / len(precisions),
        "mean_recall": sum(recalls) / len(recalls),
        "mean_f1": sum(f1_scores) / len(f1_scores),
    }
