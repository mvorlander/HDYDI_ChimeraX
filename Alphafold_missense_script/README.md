# AlphaMissense Structure Coloring Tool

This tool generates ChimeraX coloring scripts based on AlphaMissense pathogenicity scores for both PDB structures and AlphaFold models.

## Setup Instructions

### 1. Install Conda
If you don't have conda installed, download and install Miniconda:
- Linux/Mac: https://docs.conda.io/en/latest/miniconda.html
- Windows: https://docs.conda.io/en/latest/miniconda.html#windows-installers

### 2. Create Conda Environment
```bash
# Clone or download this repository
git clone <repository-url>
cd <repository-directory>

# Create conda environment from yml file
conda env create -f environment.yml

# Activate the environment
conda activate missense_color