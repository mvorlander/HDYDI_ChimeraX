# AF Missense Coloring Script

This Python script generates ChimeraX color mapping commands for AlphaFold missense scores. It retrieves missense data for protein residues from either PDB entries or AlphaFold models (via a UniProt ID) and produces a ChimeraX script that colors the structure based on these scores.

## Features

- **Chain Mapping:** Uses the PDBe API to map chains of a PDB structure to UniProt IDs.
- **Data Retrieval:** Downloads AlphaMissense CSV data for a given UniProt ID from the AlphaFold API.
- **Data Processing:** Processes missense data to compute average pathogenicity scores and determine the predominant mutation class.
- **ChimeraX Command Generation:** Produces ChimeraX commands to color specific residues according to the computed scores using a specified color palette.
- **Flexible Input:** Supports processing either a PDB structure (via the `--pdb` option) or an AlphaFold model using a UniProt ID (via the `--uniprot` option).

## Usage

Run the script from the command line:

```bash
# Process a PDB structure
python af_missense_coloring.py --pdb 7ZNJ

# Process an AlphaFold model for a given UniProt ID using a specific palette
python af_missense_coloring.py --uniprot P38919 --palette viridis
```

Additional options:

*   `-o, --output`: Specify the output filename for the generated ChimeraX commands (default: `<id>_missense_coloring_chimerax.cxc`).
*   `--palette`: Choose a color palette (default: `jet`). Available options: `jet`, `viridis`, `plasma`, `inferno`, `magma`, `rainbow`, `coolwarm`, `RdYlBu`, `spectral`.
*   `--debug`: Enable debug logging for more verbose output.

Installation
------------

### Requirements

*   Python 3.6 or later

The required Python packages are listed in `requirements.txt`.

### Using pip

Install the required packages by running:

```bash
pip install -r requirements.txt
```

### Using Conda

Alternatively, create a Conda environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate af_missense
```

Files
-----

*   **`af_missense_coloring.py`**: The main Python script.
*   **`requirements.txt`**: Lists the required Python packages.
*   **`environment.yml`**: Conda environment configuration for this project.
*   **`README.md`**: This file.
