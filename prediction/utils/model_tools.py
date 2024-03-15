import os
import re
from dotenv import load_dotenv

import joblib
import pandas as pd
from pymatgen.core import Element
from prediction.src.SeQuant.app.sequant_tools import SequantTools

load_dotenv()
SEQUANT_MODELS_PATH = os.environ['SEQUANT_MODELS_PATH']
MAIN_MODELS_PATH = os.getenv('MAIN_MODELS_PATH')

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

KMERS = ['AC', 'AT', 'CC', 'CG', 'TA', 'TC', 'TT']

ALL_FEATURES = [
    'AC',
    'AT',
    'CC',
    'CG',
    'TA',
    'TC',
    'TT',
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


def get_kmers(sequence: str) -> dict[str, int]:
    output: dict[str, int] = dict()
    for kmer in KMERS:
        output[kmer] = len(re.findall(kmer, sequence))
    return output


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
        seqtools = SequantTools(
            sequences=[sequence],
            polymer_type=POLYMER_TYPE,
            max_sequence_length=MAX_PEPTIDE_LENGTH,
            model_folder_path=SEQUANT_MODELS_PATH,
        )
        sequant_desc: pd.DataFrame = seqtools.generate_latent_representations()

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

    sequence_kmers: dict[str, int] = get_kmers(sequence)
    for key, value in sequence_kmers:
        descriptors[key] = value

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
