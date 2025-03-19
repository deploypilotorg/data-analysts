#!/usr/bin/env python3
"""
DeployPilot - Deployment automation service

This is the main entry point for the DeployPilot application.
"""

from dplibraries.models.deployment_predictor import DeploymentPredictor
from dplibraries.generators.deployment_generator import DeploymentGenerator
from dplibraries.generators.diagram_generator import DiagramGenerator

def main():
    """Main function to run the DeployPilot application."""
    print("DeployPilot - Deployment Automation Service")
    print("===========================================")
    
    # Example usage
    predictor = DeploymentPredictor("dataset.csv")
    generator = DeploymentGenerator()
    diagram_generator = DiagramGenerator()
    
    sample_repo = "excalidraw/excalidraw"
    predicted_deployment, justification = predictor.predict_deployment(sample_repo, n_similar=5)
    print(f"\nPredicted deployment type for {sample_repo}: {predicted_deployment}")
    print(f"Justification: {justification}")
    
    project_structure = "server/api.py\n database/models.py\n authentication/login.py"
    service_mapping, architecture_diagram = predictor.analyze_and_generate(sample_repo, project_structure)
    print(f"\nRecommended Cloud Services for {sample_repo}:\n{service_mapping}")
    print(f"\nGenerated Architecture Diagram:\n{architecture_diagram}")
    
    generated_files = generator.generate_files(predicted_deployment, sample_repo, project_structure)
    print("\nGenerated Deployment Files:")
    for file_name, file_content in generated_files.items():
        print(f"\n{file_name}:\n{file_content}\n")

if __name__ == "__main__":
    main() 