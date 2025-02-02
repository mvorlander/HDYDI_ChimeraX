#!/usr/bin/env python3

import requests
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO
import argparse
import sys
import time
import logging
import warnings
import os
from typing import Dict, List, Optional

# Suppress matplotlib deprecation warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AVAILABLE_PALETTES = {
    'jet': 'jet',
    'viridis': 'viridis',
    'plasma': 'plasma',
    'inferno': 'inferno',
    'magma': 'magma',
    'rainbow': 'rainbow',
    'coolwarm': 'coolwarm',
    'RdYlBu': 'RdYlBu',
    'spectral': 'Spectral'
}

class StructureMapper:
    def __init__(self):
        self.pdb_api_url = "https://www.ebi.ac.uk/pdbe/api/mappings/uniprot"
        self.alphafold_api_url = "https://alphafold.ebi.ac.uk/api/prediction"

    def get_chain_uniprot_mapping(self, pdb_id: str) -> Dict[str, Dict]:
        """Get mapping of chains to UniProt IDs for a PDB structure"""
        url = f"{self.pdb_api_url}/{pdb_id.lower()}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            logging.debug(f"PDB API response: {data}")

            mapping = {}
            if pdb_id.lower() not in data:
                logging.error(f"No data found for PDB ID {pdb_id}")
                return {}

            # Process each UniProt entry
            for uniprot_id, uniprot_data in data[pdb_id.lower()]["UniProt"].items():
                # Each UniProt entry can map to multiple chains
                for mapping_data in uniprot_data["mappings"]:
                    chain_id = mapping_data["chain_id"]
                    mapping[chain_id] = {
                        'uniprot_id': uniprot_id,
                        'start': mapping_data['unp_start'],
                        'end': mapping_data['unp_end']
                    }
                    logging.info(f"Mapped chain {chain_id} to UniProt {uniprot_id} ({mapping_data['unp_start']}-{mapping_data['unp_end']})")

            return mapping

        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving chain mapping: {e}")
            return {}

    def download_missense_csv(self, uniprot_id: str) -> Optional[pd.DataFrame]:
        """Download the AlphaMissense CSV file for a UniProt ID"""
        url = f"{self.alphafold_api_url}/{uniprot_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            logging.debug(f"AlphaFold API response for {uniprot_id}: {data}")

            csv_url = None
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict) and "amAnnotationsUrl" in entry:
                        csv_url = entry["amAnnotationsUrl"]
                        break

            if not csv_url:
                logging.error(f"No AlphaMissense CSV URL found for UniProt ID {uniprot_id}")
                return None

            logging.info(f"Downloading AlphaMissense CSV for UniProt ID {uniprot_id} from {csv_url}")
            csv_response = requests.get(csv_url)
            csv_response.raise_for_status()

            csv_data = pd.read_csv(StringIO(csv_response.text))
            logging.info(f"Successfully downloaded AlphaMissense CSV for UniProt ID {uniprot_id}")
            return csv_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading AlphaMissense CSV for UniProt ID {uniprot_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error processing data for UniProt ID {uniprot_id}: {e}")
            return None

    def generate_key_command(self, color_map) -> str:
        """Generate a ChimeraX key command to display the color mapping"""
        min_score = 0.0
        max_score = 1.0
        num_steps = 10
        step_size = (max_score - min_score) / num_steps

        key_labels = [f"{min_score + i * step_size:.2f}" for i in range(num_steps + 1)]
        key_colors = [mcolors.to_hex(color_map(i / num_steps)) for i in range(num_steps + 1)]

        key_command = "key "
        for label, color in zip(key_labels, key_colors):
            key_command += f"{color}:{label} "

        return key_command.strip()

    def process_structure(self, pdb_id: str, color_map) -> List[str]:
        """Process PDB structure and generate ChimeraX coloring commands."""
        chimerax_script = [f"open {pdb_id}", "hide atoms", "show cartoon"]
        chain_uniprot_mapping = self.get_chain_uniprot_mapping(pdb_id)
        if not chain_uniprot_mapping:
            logging.error(f"No UniProt mappings found for PDB ID {pdb_id}")
            return chimerax_script

        uniprot_groups = {}
        for chain_id, mapping_info in chain_uniprot_mapping.items():
            uniprot_id = mapping_info['uniprot_id']
            if uniprot_id not in uniprot_groups:
                uniprot_groups[uniprot_id] = {'chains': [], 'ranges': set()}
            uniprot_groups[uniprot_id]['chains'].append(chain_id)
            uniprot_groups[uniprot_id]['ranges'].add((mapping_info['start'], mapping_info['end']))

        for uniprot_id, group_info in uniprot_groups.items():
            logging.info(f"Processing UniProt ID {uniprot_id} for {len(group_info['chains'])} chains")

            csv_data = self.download_missense_csv(uniprot_id)
            if csv_data is None:
                continue

            csv_data['position'] = csv_data['protein_variant'].str.extract(r'([A-Za-z]+\d+)')

            summary = csv_data.groupby('position', sort=False).apply(lambda x: pd.Series({
                'LPath_count': (x['am_class'] == 'LPath').sum(),
                'LBen_count': (x['am_class'] == 'LBen').sum(),
                'Amb_count': (x['am_class'] == 'Amb').sum(),
                'avg_pathogenicity': x['am_pathogenicity'].mean()
            })).reset_index()

            summary['overall_class'] = summary[['LPath_count', 'LBen_count', 'Amb_count']].idxmax(axis=1).map({
                'LPath_count': 'LPath',
                'LBen_count': 'LBen',
                'Amb_count': 'Amb'
            })

            for _, row in summary.iterrows():
                position_number = ''.join(filter(str.isdigit, row['position']))
                score = row['avg_pathogenicity']
                color = mcolors.to_hex(color_map(score))
                chain_list = ",".join(group_info['chains'])
                chimerax_script.append(f"color last-opened &/{chain_list}:{position_number} {color}")

        chimerax_script.extend([
            "lighting soft",
            "set bg_color white",
            self.generate_key_command(color_map),
            "key pos 0.036642,0.100632 size 0.0378814,0.835561"
        ])
        return chimerax_script

    def process_alphafold_model(self, uniprot_id: str, color_map) -> List[str]:
        """Process AlphaFold model and generate ChimeraX coloring commands."""
        chimerax_script = [f"alphafold fetch {uniprot_id}", "hide atoms", "show cartoon"]

        csv_data = self.download_missense_csv(uniprot_id)
        if csv_data is None:
            return chimerax_script

        csv_data['position'] = csv_data['protein_variant'].str.extract(r'([A-Za-z]+\d+)')

        summary = csv_data.groupby('position', sort=False).apply(lambda x: pd.Series({
            'LPath_count': (x['am_class'] == 'LPath').sum(),
            'LBen_count': (x['am_class'] == 'LBen').sum(),
            'Amb_count': (x['am_class'] == 'Amb').sum(),
            'avg_pathogenicity': x['am_pathogenicity'].mean()
        })).reset_index()

        summary['overall_class'] = summary[['LPath_count', 'LBen_count', 'Amb_count']].idxmax(axis=1).map({
            'LPath_count': 'LPath',
            'LBen_count': 'LBen',
            'Amb_count': 'Amb'
        })

        for _, row in summary.iterrows():
            position_number = ''.join(filter(str.isdigit, row['position']))
            score = row['avg_pathogenicity']
            color = mcolors.to_hex(color_map(score))
            chimerax_script.append(f"color last-opened & :{position_number} {color}")

        chimerax_script.extend([
            "lighting soft",
            "set bg_color white",
            self.generate_key_command(color_map),
            "key pos 0.036642,0.100632 size 0.0378814,0.835561"
        ])
        return chimerax_script

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate ChimeraX color map commands for AlphaFold2 missense scores. "
            "This script retrieves missense scores for protein residues from either"
            "PDB entries or using the ALphafold models of a Uniprot entry and creates "
            "a ChimeraX script to color the structure based on these scores."
        ),
        epilog=(
            "Example usage:\n"
            "  python script.py --pdb 7ZNJ\n"
            "  python script.py --uniprot P38919\n"
            "  python script.py --uniprot P38919 --palette viridis\n"
            "  python script.py --pdb 7ZNJ --debug"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--pdb", help="PDB ID of the structure to process")
    input_group.add_argument("--uniprot", help="UniProt ID for AlphaFold model")

    parser.add_argument("-o", "--output",
                       help="Output file for ChimeraX commands (default: <id>_missense_coloring_chimerax.cxc)")
    parser.add_argument("--palette", default="jet", choices=list(AVAILABLE_PALETTES.keys()),
                       help=f"Color palette to use (default: jet). Available palettes: {', '.join(AVAILABLE_PALETTES.keys())}")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug logging")

    args = parser.parse_args()

    # Generate default output filename based on input ID
    if not args.output:
        if args.pdb:
            args.output = f"{args.pdb}_missense_coloring_chimerax.cxc"
        else:
            args.output = f"{args.uniprot}_missense_coloring_chimerax.cxc"

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        mapper = StructureMapper()
        logging.info(f"Using color palette: {args.palette}")
        color_map = plt.get_cmap(AVAILABLE_PALETTES[args.palette])

        if args.pdb:
            logging.info(f"Processing PDB structure: {args.pdb}")
            chimerax_commands = mapper.process_structure(args.pdb, color_map)
        else:
            logging.info(f"Processing AlphaFold model for UniProt ID: {args.uniprot}")
            chimerax_commands = mapper.process_alphafold_model(args.uniprot, color_map)

        with open(args.output, 'w') as f:
            f.write('\n'.join(chimerax_commands))

        logging.info(f"ChimeraX script written to {args.output}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()