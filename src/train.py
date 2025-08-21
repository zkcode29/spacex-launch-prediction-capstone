from sklearn.model_selection import GridSearchCV
import joblib
import os

def tune_model(model, param_grid, X_train, y_train, cv=5, scoring='f1'):
    """
    Performs hyperparameter tuning for a given model using GridSearchCV.

    Args:
        model: A scikit-learn classifier instance.
        param_grid (dict): Dictionary with parameters names (str) as keys and lists of
                           parameter settings to try as values.
        X_train: Training features.
        y_train: Training labels.
        cv (int): Number of cross-validation folds.
        scoring (str): Scoring metric to use for evaluation.

    Returns:
        A trained scikit-learn model with the best found hyperparameters.
    """
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,  # Use all available cores
        verbose=1
    )
    
    # Fit the grid search to the data
    grid_search.fit(X_train, y_train)
    
    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"Best {scoring} Score on Validation Set: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_

def save_model(model, path, filename):
    """
    Saves a trained model to a file using joblib.

    Args:
        model: The trained model object to save.
        path (str): The directory path to save the model in.
        filename (str): The name of the file.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, filename)
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")