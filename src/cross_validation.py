from sklearn.model_selection import StratifiedGroupKFold

def get_cv_splits(X, y, groups, n_splits=4):

    cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=4)
    return cv.split(X, y, groups=groups)