## Description

This tool uses cosine similarity and feature analysis to predict deployment types for repositories. It works by:
1. Loading and preprocessing repository data
2. Computing similarity scores between repositories
3. Making predictions based on the most common deployment types among similar repositories

## Requirements

- Python 3.x
- pandas
- numpy
- scikit-learn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/deployment-predictor.git
   cd deployment-predictor
   ```
2. Install the required dependencies:
   ```bash
   pip install pandas numpy scikit-learn
   ```

## Usage

### Basic Usage

The predictor requires a CSV dataset with repository features. The dataset should contain:
- A `repository` column with repository names
- A `deployment` column with deployment types
- Feature columns (binary 0/1 values)

### Methods

#### `predict_deployment(repository_name, n_similar=5)`
Predicts deployment type for a given repository name by finding similar repositories in the dataset.

**Parameters:**
- `repository_name` (str): Name of the repository (e.g., "owner/repo")
- `n_similar` (int): Number of similar repositories to consider (default: 5)

#### `predict_from_vector(feature_vector, n_similar=5)`
Predicts deployment type for a custom feature vector.

**Parameters:**
- `feature_vector` (list/array): Binary feature vector matching the training data features
- `n_similar` (int): Number of similar repositories to consider (default: 5)

## Dataset Format

The required CSV file should have the following structure:

```csv
repository,deployment,feature1,feature2,...,featureN
owner/repo1,type1,1,0,1,...,0
owner/repo2,type2,0,1,0,...,1
```
