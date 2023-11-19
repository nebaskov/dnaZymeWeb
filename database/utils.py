import base64
from io import BytesIO

import matplotlib.pyplot as plt
# import forgi.visual.mplotlib as fvm
# import forgi


def gc_count(sequence: str):
    pass


def second_structure_plot(sequence: str) -> None:
    pass


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
