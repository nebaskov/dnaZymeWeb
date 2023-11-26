from Bio.SeqUtils import (
    GC,
    molecular_weight,
    MeltingTemp
)
from django.db import connection


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


def get_clones(sequence: str) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM '
            '(SELECT id, sequence FROM dnazyme) AS t '
            'WHERE LEVENSHTEIN(%s, t.sequence) > 30',
            [sequence]
        )
        count = cursor.fetchone()
    if count is not None and len(count) >= 1:
        return count[0]
    return 0
