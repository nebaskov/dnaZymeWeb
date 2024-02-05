import base64
from io import BytesIO

import numpy as np
from sklearn.manifold import MDS
from Levenshtein import distance
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import AgglomerativeClustering

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from database.models import MainDnaDataBase

# from seqfold import fold, dot_bracket
# import forgi.visual.mplotlib as fvm
# import forgi


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def _get_positions(sequence: str) -> np.array:
    sequences = [item.sequence for item in MainDnaDataBase.objects.all()]
    sequences.append(sequence)
    distances = np.zeros((len(sequences), len(sequences)))
    for i in range(len(sequences)):
        for j in range(i + 1, len(sequences)):
            distances[i, j] = distance(sequences[i], sequences[j])
            distances[j, i] = distances[i, j]

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(distances)
    sample = pos[-1]
    pos = pos[:-2, :]

    k = 2
    connectivity = kneighbors_graph(pos, n_neighbors=k, include_self=False)
    model = AgglomerativeClustering(
        n_clusters=k,
        linkage='ward',
        connectivity=connectivity
    )
    model.fit(pos)
    return model, pos, sample


def plot_levenshtein(sequence: str):
    model, pos, sample = _get_positions(sequence)

    cmap = ListedColormap(["#2E4451", "#9C5551"])
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 6))
    plt.scatter(
        x=pos[:, 0],
        y=pos[:, 1],
        c=model.labels_,
        cmap=cmap
    )
    plt.scatter(
        x=[sample[0]],
        y=[sample[1]],
        c='r',
        marker='*'
    )
    plt.tight_layout()
    return get_graph()


# def plot_structure(sequence: str):
#     seq_f = fold(sequence)
#     dot_seq = dot_bracket(sequence, seq_f)
#     rnas = forgi.load_rna(dot_seq)
#     if not rnas:
#         return
#     plt.switch_backend('AGG')
#     fig = plt.figure(figsize=(10, 6))
#     fvm.plot_rna(
#         rnas[0],
#         text_kwargs={"fontweight": "black"},
#         lighten=0.7,
#         backbone_kwargs={"linewidth": 3}
#     )
#     plt.tight_layout()
#     return get_graph()

