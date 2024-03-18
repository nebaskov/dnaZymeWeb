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
PYMATGEN_FEATURES = [
    'electron_affinity',
    'ionic_radii',
    'charge'
]

SEQUANT_FEATURES = [
    'exactmw',
    'amw',
    'lipinskiHBD',
    'NumRotatableBonds',
    'NumAtoms',
    'FractionCSP3',
    'CrippenMR',
    'chi0v',
    'kappa3'
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
   'exactmw',
   'amw',
   'lipinskiHBD',
   'NumRotatableBonds',
   'NumAtoms',
   'FractionCSP3',
   'CrippenMR',
   'chi0v',
   'kappa3',
   'NaCl',
   'pH',
   'KCl',
   'cofactor concentration',
   'temperature',
   'charge',
   'electron_affinity',
   'ionic_radii'
]

CHARGES: dict[str, int] = {
    'Mg': 2,
    'Zn': 2,
    'Pb': 2,
    'Na': 1,
    'Ca': 2,
    'Mn': 2,
    'Ce': 3,
    'Co': 2,
    'Ni': 2,
    'Cd': 2,
    'Cu': 2,
    'Tm': 3,
    'Er': 3,
    'Gd': 3,
    'Ag': 1,
}


def get_pymatgen_desc(element: str) -> dict[str, float]:
    element_obj = Element(element)
    desc_dict: dict[str, float] = {
        'electron_affinity': element_obj.electron_affinity,
        'ionic_radii': element_obj.ionic_radii,
        'charge': CHARGES.get(element, 0)
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
        sequant_desc_raw: pd.DataFrame = seqtools.generate_latent_representations()
        for column in sequant_desc_raw.columns:
            sequant_desc_raw.rename(columns={column: column.replace('_repr', '')}, inplace=True)
        sequant_desc = sequant_desc_raw[SEQUANT_FEATURES]

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
    for key, value in sequence_kmers.items():
        descriptors[key] = value

    return descriptors


def make_prediction(descriptors: pd.DataFrame) -> float:
    model = joblib.load(
        os.path.join(MAIN_MODELS_PATH, 'kobs_model.pkl')
    )
    feature_renaming = {
        'ph': 'pH',
        'temp': 'temperature',
        'k_cl': 'KCl',
        'na_cl': 'NaCl',
        'cofactor_concentration': 'cofactor concentration' 
    }
    descriptors.rename(columns=feature_renaming, inplace=True)
    prediction = model.predict(descriptors[ALL_FEATURES])
    return round(prediction[0], 4)
