# -*- coding: utf-8 -*-
"""Sampling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l2eiIS-Q8FBVHjnl8OnqvbIoJ0GbT9lQ
"""

import pandas as pd
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import TomekLinks
from imblearn.under_sampling import NearMiss
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1. Load the dataset
url = "/content/drive/MyDrive/Creditcard_data.csv"
data = pd.read_csv(url)

# 2. Define features and target
X = data.drop('Class', axis=1)
y = data['Class']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Sampling Techniques

# 1. Random Over-Sampling (Duplicate instances of the minority class)
ros = RandomOverSampler(sampling_strategy='minority')
X_ros, y_ros = ros.fit_resample(X_train, y_train)

# 2. Random Under-Sampling (Remove instances of the majority class)
rus = RandomUnderSampler(sampling_strategy='majority')
X_rus, y_rus = rus.fit_resample(X_train, y_train)

# 3. SMOTE (Generate synthetic samples for the minority class)
smote = SMOTE(sampling_strategy='minority')
X_smote, y_smote = smote.fit_resample(X_train, y_train)

# 4. Tomek Links (Remove very close examples from different classes)
tomek = TomekLinks(sampling_strategy='all')
X_tomek, y_tomek = tomek.fit_resample(X_train, y_train)

# 5. NearMiss (Under-sample the majority class by selecting instances closest to the minority class)
nearmiss = NearMiss(sampling_strategy='not majority')  # Corrected sampling strategy
X_nearmiss, y_nearmiss = nearmiss.fit_resample(X_train, y_train)

# 3. Define the machine learning models
models = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(),
    "KNN": KNeighborsClassifier(),
    "Gradient Boosting": GradientBoostingClassifier()
}

# 4. Function to train and evaluate models with different sampling techniques
def evaluate_sampling_models():
    results = {}
    # Loop over models
    for model_name, model in models.items():
        model_results = {}

        # Loop over sampling techniques
        for sampling_name, (X_sampled, y_sampled) in [
            ("Random Over-Sampling", (X_ros, y_ros)),
            ("Random Under-Sampling", (X_rus, y_rus)),
            ("SMOTE", (X_smote, y_smote)),
            ("Tomek Links", (X_tomek, y_tomek)),
            ("NearMiss", (X_nearmiss, y_nearmiss))
        ]:
            # Train the model on the sampled data
            model.fit(X_sampled, y_sampled)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)

            # Save accuracy for comparison
            model_results[sampling_name] = accuracy

        # Store results for each model
        results[model_name] = model_results

    return results

# 5. Evaluate all models with all sampling techniques
results = evaluate_sampling_models()

# 6. Display results
for model_name, model_results in results.items():
    print(f"\nResults for {model_name}:")
    for sampling_name, accuracy in model_results.items():
        print(f" - {sampling_name}: {accuracy:.4f}")

# 7. Identify the best sampling technique for each model
best_sampling_techniques = {}
for model_name, model_results in results.items():
    best_sampling_techniques[model_name] = max(model_results, key=model_results.get)

print("\nBest Sampling Technique for Each Model:")
for model_name, best_sampling in best_sampling_techniques.items():
    print(f"{model_name}: {best_sampling}")