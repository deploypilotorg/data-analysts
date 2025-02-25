# Data Analysts Repository

## Overview
This repository is designed for analyzing and predicting cloud deployment strategies based on a dataset of repositories and their configurations. It contains scripts for processing data, generating deployment recommendations, and creating architecture diagrams using OpenAI models.

## Repository Structure

```
.
├── dataset.csv               # Dataset of repositories with deployment attributes
├── deployment_generator.py   # Script for analyzing project services and generating deployment files
├── diagram_generator.py      # Script for generating architecture diagrams using OpenAI
├── deployment_predictor.py   # Machine learning model to predict deployment strategy
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

3. **Set up your OpenAI API Key:**
   - Create a `.env` file in the root directory and add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

### Deployment Prediction
Use `deployment_predictor.py` to predict the deployment strategy for a given repository:
```bash
python deployment_predictor.py
```

### Generate Deployment Files
Call `deployment_generator.py` to generate deployment configurations:
```bash
python deployment_generator.py
```

### Generate Architecture Diagrams
Use `diagram_generator.py` to create architecture diagrams:
```bash
python diagram_generator.py
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

## License
This project is licensed under the MIT License.

## Contact
For inquiries or contributions, contact:
- **Team Name:** DeployPilotOrg
- **Email:** [Your Contact Email]
