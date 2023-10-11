import os

import joblib
import pandas as pd
import tensorflow as tf

from pymatgen.core import Element
from .src.SeQuant_user.Funcs import (
    generate_rdkit_descriptors,
    generate_latent_representations,
    SeQuant_encoding,
)


SEQUANT_MODELS_PATH = os.getenv('SEQUANT_MODELS_PATH')
MAIN_MODELS_PATH = os.getenv('MAIN_MODELS_PATH')

POLYMER_TYPE = 'DNA'
MAX_PEPTIDE_LENGTH = 96
NUCLEOTIDES = ['dA', 'dT', 'dG', 'dC']

USER_FEATURES = [
    'Temperature',
    'pH',
    'NaCl',
    'KCl',
    'Mg2+'
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


def get_pymatgen_desc(element: str) -> dict[str, float]:
    element_obj = Element(element)
    desc_dict: dict[str, float] = {
        'electron_affinity': element_obj.electron_affinity()
    }
    return desc_dict


def get_sequant_descriptors(sequences: list[str]) -> dict[str, float]:
    raw_rdkit_descriptors: pd.DataFrame = generate_rdkit_descriptors(
        normalize=None
    )
    rdkit_descriptors = raw_rdkit_descriptors.iloc[NUCLEOTIDES]
    encoded_sequences: tf.Tensor = SeQuant_encoding(
        sequences_list=sequences,
        polymer_type=POLYMER_TYPE,
        descriptors=rdkit_descriptors,
        num=MAX_PEPTIDE_LENGTH
    )
    raw_latent_representation: pd.DataFrame = generate_latent_representations(
        sequences_list=sequences,
        sequant_encoded_sequences=encoded_sequences,
        polymer_type=POLYMER_TYPE,
        add_peptide_descriptors=False,
        path_to_model_folder=SEQUANT_MODELS_PATH
    )
    latent_representation = raw_latent_representation[SEQUANT_FEATURES]
    return latent_representation


def get_descriptors(
    user_input: dict[str, float | str | int],
    use_sequant: bool = True,
    use_pymatgen: bool = True
) -> pd.DataFrame:
    sequence = user_input.get('sequence')
    cofactor = user_input.get('cofactor')
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

    return descriptors


def make_prediction(descriptors: pd.DataFrame) -> float:
    model = joblib.load(
        os.path.join(MAIN_MODELS_PATH, 'kobs_model.pkl')
    )
    prediction = model.predict(descriptors)
    return prediction[0]
