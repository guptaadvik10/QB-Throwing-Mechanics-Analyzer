from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_throw_classifier(X, y):

    model = RandomForestClassifier(
        n_estimators = 100, 
        random_state = 4,
        class_weight = "balanced"
    )

    model.fit(X, y)

    for feature, importance in zip(
        X.columns, 
        model.feature_importances_
    ):
        print(feature, importance)

    return model


