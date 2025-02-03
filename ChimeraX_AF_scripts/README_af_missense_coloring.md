
README
------

### Overview

This script fetches Alpha Missense data for a given UniProt ID and maps the corresponding missense scores onto a specified structure (chain/model). It labels each residue with its score, defines an averaged score attribute, colors the structure accordingly, and scales the cartoon representation to visualize regions with different missense propensities.

### Features

*  Labels each side chain in the target structure with a full amino acid substitution matrix colored by predicted pathogenicity (useful for detailes inspection)
*  Applies a color mapping and cartoon radius scaling to the the model (useful for overview images to identify potentially functionally important regions in your POI)

  Example output:
<img width="924" alt="image" src="https://github.com/user-attachments/assets/a747e1b4-9edd-4dd0-abf3-9fea2e4aa6dc" />


---
Installation and Setup
----------------------

1.  **Save the Scripts Locally:**  
    Save the provided `.cxc` script files (e.g., `analyse_af_screen_hit.cxc`, `analyse_af3_prediction.cxc`, and `analyse_auto-alphafold_prediction.cxc`) in a local directory on your computer.  
    _Example Path:_  
    `/Users/your.name/ChimeraX/scripts/`
    
2.  **Add Startup Aliases:**  
    To make it easy to run these scripts from the ChimeraX command line, add the following alias lines to your ChimeraX startup commands. In ChimeraX, these can be set under **Preferences > Startup**.  
    Replace the example path with the path to your scripts directory.
    
    ```
    alias map_missense runscript /PATH/TO/YOUR/scripts/af_missense_coloring.cxc $1 $2
    ```
    
3.  **Restart ChimeraX:**  
    After editing your startup preferences, restart ChimeraX to load the aliases.

    
### Usage

Run the script from within ChimeraX with the following command:

```bash
runscript map_missense [uniprot-id-to-fetch-scores-from] [chain-ID to apply mapping to]
```

#### Example:

To fetch missense scores for UniProt ID `P12345` and apply them to the alphafold model of P12345, assuming no other models are open when you run the script:


```
runscript map_missense P12345 #1/A
```

### Important Note

*   **Missense Scores Availability:**  
    The AlphaFold missense scores are currently available only for human proteins. Ensure that the provided UniProt ID corresponds to a human protein.


