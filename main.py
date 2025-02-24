import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('dataset.csv')

# Preprocess data
# Convert Yes/No to 1/0 for features
df = df.replace({'Yes': 1, 'No': 0}).infer_objects()

# Separate features and target
X = df.drop(['repository', 'deployment'], axis=1)
y = df['deployment']

# Encode the target variable
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
# Get unique classes present in the test set
unique_classes = sorted(list(set(y_test) | set(y_pred)))
target_names = le.inverse_transform(unique_classes)

print("Model Performance:")
print(classification_report(y_test, y_pred, target_names=target_names))

# Function to predict deployment platform for new projects
def predict_deployment(features_dict):
    """
    Predict deployment platform for a new project.
    
    Args:
        features_dict (dict): Dictionary containing feature values (0 or 1)
        
    Returns:
        str: Predicted deployment platform
    """
    # Convert dictionary to DataFrame
    features = pd.DataFrame([features_dict])
    
    # Make prediction
    prediction = model.predict(features)
    
    # Return predicted platform
    return le.inverse_transform(prediction)[0]

# Example usage
example_project = {
    'already_deployed': 0,
    'has_frontend': 1,
    'has_cicd': 0,
    'multiple_environments': 0,
    'uses_containerization': 0,
    'uses_iac': 0,
    'high_availability': 0,
    'authentication': 1,
    'realtime_events': 0,
    'storage': 0,
    'caching': 0,
    'ai_implementation': 0,
    'database': 1,
    'microservices': 0,
    'monolith': 0,
    'api_exposed': 0,
    'message_queues': 0,
    'background_jobs': 0,
    'sensitive_data': 0,
    'external_apis': 0
}

print("\nPrediction for example project:")
print(predict_deployment(example_project))

# Print feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
})
print("\nFeature Importance:")
print(feature_importance.sort_values('importance', ascending=False))
