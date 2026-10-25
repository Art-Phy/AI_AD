from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler



def split_dataset(
    X: list[list[float]],
    y: list[int],
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Divide el dataset en conjuntos de entrenamiento y test"""
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )



def train_logistic_regression(
    X_train: list[list[float]],
    y_train: list[int],
) -> Pipeline:
    """Entrena un pipeline con estandarización y Logistic Regression"""
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    random_state=42,
                    max_iter=1000,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    return model
