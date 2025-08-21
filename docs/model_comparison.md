# Model Performance Comparison

This document provides a detailed comparison of the machine learning models trained to predict Falcon 9 first stage landing success.

## Evaluation Metrics

The following metrics were used to assess model performance on the unseen test dataset:

| Model                            | Accuracy | Precision | Recall | F1-Score |
| -------------------------------- | -------- | --------- | ------ | -------- |
| **Logistic Regression**          | 0.926829 | 0.906250  | 1.0    | 0.950820 |
| **Decision Tree**                | 0.926829 | 0.906250  | 1.0    | 0.950820 |
| **Random Forest**                | 0.902439 | 0.878788  | 1.0    | 0.935484 |
| **Support Vector Machine (SVM)** | 0.926829 | 0.906250  | 1.0    | 0.950820 |
|

## Analysis

**Logistic Regression:**
Serves as a strong baseline model. Its performance was consistent across accuracy, precision, recall, and F1-score. After hyperparameter tuning, it achieved a best cross-validation score of 0.9335, confirming its robustness and generalization ability. This balance of simplicity and strong performance makes it an excellent choice as the final model.

**Decision Tree:**
This model provided comparable results to Logistic Regression and SVM on the test set. However, it achieved a slightly lower tuned score (0.9285) and may be prone to overfitting, as decision trees often memorize training data. While interpretable, it did not generalize as well as the other models.

**Random Forest:**
As an ensemble method, it improved upon the single Decision Tree by reducing overfitting. After tuning, it achieved the highest cross-validation score of 0.9338, slightly outperforming Logistic Regression and SVM. However, it had a slightly lower F1-score on the test set compared to Logistic Regression, suggesting it may not balance precision and recall as effectively despite its ensemble strength.

**Support Vector Machine (SVM):**
The SVM model performed almost identically to Logistic Regression, achieving a tuned score of 0.9335. While effective, SVMs can be computationally more expensive compared to Logistic Regression, especially with larger datasets. In this case, Logistic Regression offered a simpler yet equally effective solution.

## Best Model Selection

Based on the evaluation metrics, the Logistic Regression model was selected as the final model for this project. It demonstrated the best balance of precision and recall and achieved the highest F1-Score, making it the most reliable predictor of landing success among the models tested.