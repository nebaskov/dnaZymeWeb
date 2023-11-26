import os
import base64
from io import BytesIO
from dotenv import load_dotenv

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from pymatgen.core import Element
from Bio.SeqUtils import (
    GC,
    molecular_weight,
    MeltingTemp
)

import matplotlib.pyplot as plt

from .src.SeQuant_user.Funcs import (
    generate_rdkit_descriptors,
    generate_latent_representations,
    SeQuant_encoding,
)

load_dotenv()
SEQUANT_MODELS_PATH = os.environ['SEQUANT_MODELS_PATH']
MAIN_MODELS_PATH = os.getenv('MAIN_MODELS_PATH')

print(f'{SEQUANT_MODELS_PATH=}')
print(f'{MAIN_MODELS_PATH=}')

POLYMER_TYPE = 'DNA'
MAX_PEPTIDE_LENGTH = 96
NUCLEOTIDES = ['dA', 'dT', 'dG', 'dC']

USER_FEATURES = [
    'temp',
    'ph',
    'na_cl',
    'k_cl',
    'cofactor',
    'cofactor_concentration'
]
PYMATGEN_FEATURES = ['electron_affinity']

SEQUANT_FEATURES = [
    'exactmw',
    'amw',
    'lipinskiHBD',
    'NumRotatableBonds',
    'NumAtoms',
    'FractionCSP3',
    'NumBridgeheadAtoms',
    'CrippenMR',
    'chi0n'
]

ALL_FEATURES = [
    'Temperature',
    'pH',
    'NaCl',
    'KCl',
    'cofactor_conc',
    'electron_affinity',
    'exactmw',
    'amw',
    'lipinskiHBD',
    'NumRotatableBonds',
    'NumAtoms',
    'FractionCSP3',
    'NumBridgeheadAtoms',
    'CrippenMR',
    'chi0n'
]


def get_pymatgen_desc(element: str) -> dict[str, float]:
    element_obj = Element(element)
    desc_dict: dict[str, float] = {
        'electron_affinity': element_obj.electron_affinity
    }
    return desc_dict


def get_sequant_descriptors(sequences: list[str]) -> dict[str, float]:
    raw_rdkit_descriptors: pd.DataFrame = generate_rdkit_descriptors(
        normalize=None
    )
    rdkit_descriptors = raw_rdkit_descriptors.loc[NUCLEOTIDES]
    descriptor_names: list[str] = rdkit_descriptors.columns.tolist()
    encoded_sequences: tf.Tensor = SeQuant_encoding(
        sequences_list=sequences,
        polymer_type=POLYMER_TYPE,
        descriptors=rdkit_descriptors,
        num=MAX_PEPTIDE_LENGTH
    )
    latent_representation = generate_latent_representations(
        sequences_list=sequences,
        sequant_encoded_sequences=encoded_sequences,
        polymer_type=POLYMER_TYPE,
        add_peptide_descriptors=False,
        path_to_model_folder=SEQUANT_MODELS_PATH
    )
    repr_df = pd.DataFrame(latent_representation, columns=descriptor_names)
    return repr_df[SEQUANT_FEATURES]


def get_descriptors(
    user_input: dict,
    use_sequant: bool = True,
    use_pymatgen: bool = True
) -> pd.DataFrame:
    sequence = user_input.get('sequence')
    cofactor = user_input.get('cofactor_element')
    cofactor_conc = user_input.get('cofactor_concentration')
    pymatgen_desc: dict[str, float] = {}
    sequant_desc: pd.DataFrame = pd.DataFrame()

    if sequence is None:
        return

    if cofactor is not None and use_pymatgen:
        pymatgen_desc: dict[str, float] = get_pymatgen_desc(cofactor)

    if use_sequant:
        sequant_desc: pd.DataFrame = get_sequant_descriptors(
            sequences=[sequence]
        )

    descriptors: pd.DataFrame = sequant_desc.copy()
    for feature in PYMATGEN_FEATURES:
        desc_value = pymatgen_desc.get(feature)
        if desc_value is not None:
            descriptors[feature] = desc_value

    for feature in USER_FEATURES:
        desc_value = user_input.get(feature)
        if desc_value is not None:
            descriptors[feature] = desc_value

    descriptors['cofactor_concentration'] = cofactor_conc

    return descriptors


def make_prediction(descriptors: pd.DataFrame) -> float:
    model = joblib.load(
        os.path.join(MAIN_MODELS_PATH, 'kobs_model.pkl')
    )
    feature_renaming = {
        'ph': 'pH',
        'temp': 'Temperature',
        'k_cl': 'KCl',
        'na_cl': 'NaCl',
        'cofactor_concentration': 'cofactor_conc',
    }
    descriptors.rename(columns=feature_renaming, inplace=True)
    prediction = model.predict(descriptors[ALL_FEATURES])
    return round(prediction[0], 4)


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_seq_properties(sequence: str) -> dict:
    return {
        'seq_length': len(sequence),
        'gc_content': round(GC(sequence), 2),
        'mol_weight': round(molecular_weight(sequence), 2),
        'melting_temp': round(MeltingTemp.Tm_Wallace(sequence), 2)
    }


def process_buffer(user_input: dict) -> str:
    buffer = 'HEPES pH {ph}, {na_cl} mM NaCl, {k_cl} mM KCl'
    return buffer.format(
        ph=user_input.get('ph'),
        na_cl=user_input.get('na_cl'),
        k_cl=user_input.get('k_cl')
    )
