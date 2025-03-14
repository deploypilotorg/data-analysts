import warnings
from collections import Counter
import numpy as np
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder, StandardScaler
from dplibraries.generators.deployment_generator import DeploymentGenerator
from dplibraries.generators.diagram_generator import DiagramGenerator

# Feature-to-Provider Mapping
FEATURE_PROVIDER_MAPPING = {
    "authentication": {"AWS": "Cognito", "GCP": "Identity Platform", "Firebase": "Firebase Auth"},
    "uses_containerization": {"AWS": "ECS, EKS", "GCP": "GKE, Cloud Run", "Vercel": "Serverless Functions"},
    "database": {"AWS": "RDS, DynamoDB", "GCP": "Cloud SQL, Firestore", "Firebase": "Firestore, RTDB"},
    "caching": {"AWS": "ElastiCache", "GCP": "Cloud Memorystore", "Firebase": "CDN Caching"},
    "ci_cd": {"AWS": "CodePipeline, CodeDeploy", "GCP": "Cloud Build, Cloud Deploy", "Vercel": "Git Deploy"},
    "serverless": {"AWS": "Lambda, Fargate", "GCP": "Cloud Functions", "Vercel": "Serverless Functions"},
    "realtime_events": {"AWS": "Kinesis, IoT Core", "GCP": "Pub/Sub", "Firebase": "Realtime Database, Firestore"},
}

class DeploymentPredictor:
    def __init__(self, dataset_path):
        # Load the dataset
        self.df = pd.read_csv(dataset_path)

        # Preprocess data
        self.df = self.df.infer_objects(copy=False)
        self.df = self.df.replace({"Yes": 1, "No": 0})

        # Separate features and target
        self.X = self.df.drop(["repository", "deployment"], axis=1)
        self.y = self.df["deployment"]

        # Encode the target variable
        self.le = LabelEncoder()
        self.y_encoded = self.le.fit_transform(self.y)

        # Convert boolean strings to integers (if needed)
        self.X = self.X.astype(int)

        # Initialize and fit the scaler
        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(self.X)

        # Calculate cosine similarity matrix
        self.similarity_matrix = cosine_similarity(self.X_scaled)

    def predict_deployment(self, repository_name, n_similar=5):
        try:
            idx = self.df[self.df["repository"] == repository_name].index[0]
        except IndexError:
            return "Repository not found", "No justification available"

        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similar_repos = similarity_scores[1:n_similar + 1]
        similar_deployments = [self.y.iloc[idx] for idx, _ in similar_repos]
        deployment_prediction = Counter(similar_deployments).most_common(1)[0][0]

        matched_features = []
        repo_features = self.X.iloc[idx]

        for feature, providers in FEATURE_PROVIDER_MAPPING.items():
            if repo_features.get(feature, 0) == 1 and deployment_prediction in providers:
                matched_features.append(f"{feature} → {providers[deployment_prediction]}")

        justification = f"Based on the most similar repositories, the predicted deployment type for {repository_name} is {deployment_prediction}."
        if matched_features:
            justification += "\nFeatures that contributed to this recommendation:\n" + "\n".join(matched_features)
        else:
            justification += "\nNo strong feature matches found."

        return deployment_prediction, justification

    def analyze_and_generate(self, repo_name, project_structure):
        """
        Analyze project structure, generate deployment files, and create architecture diagrams.
        """
        generator = DeploymentGenerator()
        diagram_generator = DiagramGenerator()

        service_mapping = generator.analyze_project_services(repo_name, project_structure)
        architecture_diagram = diagram_generator.generate_architecture_diagram(repo_name, project_structure)
        
        return service_mapping, architecture_diagram 