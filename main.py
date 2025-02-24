from collections import Counter

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the dataset
df = pd.read_csv("dataset.csv")

# Preprocess data
# Convert Yes/No to 1/0 for features
df = df.replace({"Yes": 1, "No": 0})
df = df.infer_objects(copy=False)

# Separate features and target
X = df.drop(["repository", "deployment"], axis=1)
y = df["deployment"]

# Encode the target variable
le = LabelEncoder()
y_encoded = le.fit_transform(y)

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
    idx = df[df["repository"] == repository_name].index[0]

    # Get similarity scores for this repository
    similarity_scores = list(enumerate(similarity_matrix[idx]))

    # Sort repositories by similarity score
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get top N most similar repositories (excluding itself)
    similar_repos = similarity_scores[1 : n_similar + 1]

    # Get the deployment types of the similar repositories
    similar_deployments = [y.iloc[idx] for idx, _ in similar_repos]

    # Predict deployment type based on the most common deployment type among similar repositories
    deployment_prediction= Counter(similar_deployments).most_common(1)[0][0]

    return deployment_prediction


# Example usage
if __name__ == "__main__":
    # Example: Predict deployment for a repository
    sample_repo = "excalidraw/excalidraw"  # Replace with actual repository
    predicted_deployment = predict_deployment(sample_repo, n_similar=5)

    print(f"\nPredicted deployment type for {sample_repo}: {predicted_deployment}")
