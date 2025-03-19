# DeployPilot - Data Analysts Repository

## Overview
This repository is designed for analyzing and predicting cloud deployment strategies based on a dataset of repositories and their configurations. It contains scripts for processing data, generating deployment recommendations, and creating architecture diagrams using OpenAI models.

## Repository Structure

```
.
├── dataset.csv               # Dataset of repositories with deployment attributes
├── main.py                   # Main entry point for the application
├── dplibraries/              # Core library package
│   ├── generators/           # Deployment and diagram generators
│   │   ├── deployment_generator.py  # Generates deployment configurations
│   │   └── diagram_generator.py     # Generates architecture diagrams
│   ├── models/               # Machine learning models
│   │   └── deployment_predictor.py  # Predicts deployment platforms
│   └── utils/                # Utility functions
├── docs/                     # Documentation
├── examples/                 # Example notebooks and scripts
├── tests/                    # Test files
├── setup.py                  # Package installation configuration
├── requirements.txt          # List of required dependencies
├── .gitignore                # Ignored files and directories
└── README.md                 # Documentation for the repository
```

## Features
- **Deployment Prediction:** Predicts cloud deployment strategies based on repository characteristics.
- **Architecture Diagram Generation:** Creates architecture diagrams using OpenAI's models.
- **Cloud Service Mapping:** Maps repository components to recommended cloud services.
- **Machine Learning Model:** Uses similarity analysis to determine the best deployment platform.

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- Pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deploypilotorg/data-analysts.git
   cd data-analysts
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

4. **Set up your OpenAI API Key:**
   - Create a `.env` file in the root directory and add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Or set it as an environment variable:
     ```bash
     export OPENAI_API_KEY="your_api_key_here"
     ```

## Usage

### Running the Application
Use the main script to run the full application:
```bash
python main.py
```

This will:
1. Predict the deployment platform for a sample repository
2. Generate cloud service recommendations
3. Create an architecture diagram
4. Generate deployment configuration files

### Using Individual Components

#### Deployment Prediction
```python
from dplibraries.models.deployment_predictor import DeploymentPredictor

predictor = DeploymentPredictor("dataset.csv")
deployment, justification = predictor.predict_deployment("your-repo/name")
print(f"Predicted deployment: {deployment}")
print(f"Justification: {justification}")
```

#### Generate Deployment Files
```python
from dplibraries.generators.deployment_generator import DeploymentGenerator

generator = DeploymentGenerator()
files = generator.generate_files("AWS", "your-repo/name", "project structure")
```

#### Generate Architecture Diagrams
```python
from dplibraries.generators.diagram_generator import DiagramGenerator

diagram_generator = DiagramGenerator()
diagram = diagram_generator.generate_architecture_diagram("your-repo/name", "project structure")
```

## Data

### `dataset.csv`
- **Contains:** A structured dataset of repositories and their deployment attributes.
- **Columns:**
  - `repository`: GitHub repository name.
  - `deployment`: Deployment platform (AWS, Vercel, Firebase, etc.).
  - `already_deployed`: Whether the project is already deployed.
  - `uses_containerization`: Whether the project uses Docker or Kubernetes.
  - `database`: Whether the project includes a database.
  - **More features** related to cloud architecture and deployment.

## Contributing
We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

## Contact
For inquiries or contributions, contact:
- **Team Name:** DeployPilotOrg

