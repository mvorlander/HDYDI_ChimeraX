
README
------

### Overview

This script fetches AlphaFold data for a given UniProt ID and maps the corresponding missense scores onto a specified structure (chain/model). It labels each residue with its score, defines an averaged score attribute, colors the structure accordingly, and scales the cartoon representation to visualize regions with different missense propensities.

### Features

*   **Data Fetching:** Downloads AlphaFold data for the specified UniProt ID.
*   **Missense Score Retrieval:** Opens missense score data from the AlphaFold database.
*   **Mapping:** Associates the missense data with the target chain/model.
*   **Labeling:** Labels each residue with its missense score using a blue-to-red color palette.
*   **Score Averaging:** Computes an average substitution score ("avg") for each residue.
*   **Visualization:** Colors the structure and scales the cartoon representation based on the averaged score.

### Usage

Run the script from within ChimeraX with the following command:

```bash
runscript map_missense [uniprot-id-to-fetch-scores-from] [chain-ID to apply mapping to]
```

#### Example:

To fetch missense scores for UniProt ID `P12345` and apply them to chain A in model `A`:


```
runscript map_missense P12345 #1/A
```

### Important Note

*   **Missense Scores Availability:**  
    The AlphaFold missense scores are currently available only for human proteins. Ensure that the provided UniProt ID corresponds to a human protein.

### Installation

1.  **Save the Script:**  
    Save the `map_missense.cxc` script to your local directory (e.g., `~/ChimeraX/scripts/`).
    
2.  **(Optional) Create an Alias:**  
    To simplify running the script, add an alias to your ChimeraX startup commands (under **Preferences > Startup**). For example:
    
    ```bash
    alias map_missense runscript /PATH/TO/YOUR/scripts/map_missense.cxc $1 $2
    ```
    
    Replace `/PATH/TO/YOUR/scripts/` with the actual path where you saved the script.
    
3.  **Restart ChimeraX:**  
    After updating your startup commands, restart ChimeraX to enable the alias.

4.  **Run the script**
Run the script through the ChimeraX command line. If you have an empty session, the following command will fetch the Alphafold model for P12345 and color and label it by missense scores
  
```
map_missense P12345 #1
``` 

