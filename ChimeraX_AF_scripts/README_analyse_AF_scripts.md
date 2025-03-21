ChimeraX AlphaFold Analysis Scripts
===================================

These ChimeraX scripts provide an automated way to analyze AlphaFold predictions. They are designed to process predictions from the Alphafold 3 webserver,  hits from VBC Alphafold2 screen implementation by Dominik Handler, and the `auto‐alphafold.sh` runs by Juraj Ahel. The scritps generate interface contact visualizations, save interface residues to files, align all predicitons and create interactive sliders to browse models easily.

**Note** The ChimeraX 1.9 Daily release from 2025/02/04 will contain a fix that prevents the scripts form stopping when analyzing AF predictions that have no contacting residues, please update your installation!

Overview
--------

There are three main scripts provided, depending on the source of the Alphafold predictions:

1.  **analysis\_af\_screen\_hit.cxc**
   
2.  **analyse\_af3\_prediction.cxc**

3.  **analyse\_auto-alphafold\_prediction.cxc**
    
     *   **Output:**
        -   Generates interface contact visualizations by drawing pseudobonds between contacting residues.
        -   Labels pseudobonds with residue names and numbers.
        -   Saves contact residue data to text files.
        -   Creates named selections for interface residues.
        -   Combines interface selections and creates an mseries slider for model comparison.

### Visual Outputs

*   **Pseudobonds and Labels:**  
    The scripts create pseudobonds between residues that are in spatial proximity and display labels with the residue names and numbers for each contacting pair.
    
*   **Named Selections:**  
    Each script creates frozen (named) selections for the interface residues (e.g., `interfaces_<unique-string>_rank_X`).
    
*   **Coloring and Slider:**  
    The models are colored (using the "rainbow" and "byhetero" schemes) to help visually distinguish chains and interfaces. An mseries slider is generated so that users can cycle through the different models easily.
    
![Artboard 1](https://github.com/user-attachments/assets/002f8248-10ca-48d2-9385-2e1070f21db5)

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
    alias analyse_af_screen_hit runscript /PATH/TO/YOUR/scripts/analysis_af_screen_hit.cxc $1 $2
    alias analyse_af3 runscript /PATH/TO/YOUR/scripts/analyse_af3_prediction.cxc $1 $2
    alias analyse_auto-AF runscript /PATH/TO/YOUR/scripts/analyse_auto-alphafold_prediction.cxc $1 $2
    ```
    
    For example, if your scripts are stored in `/Users/your.name/ChimeraX/scripts`, your startup commands might look like this:
    
    ```
    alias analyse_af_screen_hit runscript /Users/your.name/ChimeraX/scripts/analyse_af_screen_hit.cxc $1 $2
    alias analyse_af3 runscript /Users/your.name/ChimeraX/scripts/analyse_af3_prediction.cxc $1 $2
    alias analyse_auto-AF runscript /Users/your.name/ChimeraX/scripts/analyse_auto-alphafold_prediction.cxc $1 $2
    ```
    
3.  **Restart ChimeraX:**  
    After editing your startup preferences, restart ChimeraX to load the aliases.
    

Usage
-----

Once installed, you can run the scripts from the ChimeraX command line using the defined aliases. Each script requires two arguments:
* **Make sure to run the commands in a clean ChimeraX session without any models open!**  Otherwise, the alignment of predictions and combination into a slider might get messed up.
*   **First argument:** The path to the directory containing the AlphaFold prediction files.
*   **Second argument:** A unique string (e.g., a UniProt ID or hit name) that is used in the file name matching and output file naming.
* **Enclose file paths in quoation marks to avoid issues with spaces in file names or special characters!!** 

### Example Commands

*   **For an AlphaFold screen hit:**
    
    ```
    analyse_af_screen_hit "/path/to/AF/screen/directory" UNIQUE_HIT_STRING
    ```
    The UNIQUE_HIT_STRING might be the uniprot name or id of a protein identified in your screen that you want to analyse.
    
*   **For an AlphaFold 3 prediction:**
    
    ```
    analyse_af3 "/path/to/AF3/prediction/directory" CUSTOM_NAME
    ```
    The CUSTOM_NAME can be anything and is used for naming outputs.
*   **For an `auto-alphafold.sh` prediction:**
    
    ```
    analyse_auto-AF "/path/to/auto_AF/prediction/directory" CUSTOM_NAME
    ```
    The CUSTOM_NAME can be anything and is used for naming outputs.

    

After running the command, the script will process the files, display pseudobonds with labels, save output files (contact residue files based on buried area calculations, and pairwise residue contacts derived from the JSON file), and generate a slider to browse through the models.

Final Notes
-----------

*   **File Naming and Organization:**  
    Make sure to you the correct script depending on the source of your prediction. AF3 and auto-alphafold result    
    folders are expected to contain the results from one prediction only. 
    
*   **Customization:**  
    Feel free to modify the scripts as needed to fit your workflow or to add additional processing/visualization features.
    

