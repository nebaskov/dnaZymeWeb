from Bio.SeqUtils import (
    GC,
    molecular_weight,
    MeltingTemp
)


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
