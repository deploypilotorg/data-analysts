import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from collections import Counter

# Load the dataset
df = pd.read_csv('dataset.csv')

# Preprocess data
# Convert Yes/No to 1/0 for features
df = df.replace({'Yes': 1, 'No': 0})
df = df.infer_objects(copy=False)

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
print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
print(classification_report(y_test, y_pred, target_names=target_names))

# Convert boolean strings to integers (if needed)
X = X.astype(int)

# Initialize and fit the scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Calculate cosine similarity matrix
similarity_matrix = cosine_similarity(X_scaled)

def predict_deployment(repository_name, n_similar=5):
    """
    Predict the deployment type based on similar repositories

    Args:
        repository_name (str): Name of the repository to predict deployment for
        n_similar (int): Number of similar repositories to consider for prediction

    Returns:
        str: Predicted deployment type
    """
    # Find the index of the repository
    idx = df[df['repository'] == repository_name].index[0]

    # Get similarity scores for this repository
    similarity_scores = list(enumerate(similarity_matrix[idx]))

    # Sort repositories by similarity score
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get top N most similar repositories (excluding itself)
    similar_repos = similarity_scores[1:n_similar+1]

    # Get the deployment types of the similar repositories
    similar_deployments = [y.iloc[idx] for idx, _ in similar_repos]

    # Predict the deployment type based on the most common deployment type among similar repositories
    predicted_deployment = Counter(similar_deployments).most_common(1)[0][0]

    return predicted_deployment

# Example usage
if __name__ == "__main__":
    # Example: Predict deployment for a repository
    sample_repo = "excalidraw/excalidraw"  # Replace with an actual repository name from your dataset
    predicted_deployment = predict_deployment(sample_repo, n_similar=5)

    print(f"\nPredicted deployment type for {sample_repo}: {predicted_deployment}")

# Print feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
})
print("\nFeature Importance:")
print(feature_importance.sort_values('importance', ascending=False))
