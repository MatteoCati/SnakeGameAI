from typing import List
import matplotlib.pyplot as plt
import pickle as pkl
import numpy as np


def show_graph(file_names: List[str], avg_length: int):
    """Draw a graph with scores from the given list of files, and with a sliding average of length `avg_length`

    Parameters
    ----------
    file_names: list(str)
        a list containing the paths of all files to draw in the graph
    avg_length: int
        the size of the sliding window for the average
    """
    scores_tmp = []
    for file in file_names:
        with open(file, "rb") as fin:
            scores_tmp += pkl.load(fin)
    scores = np.array(scores_tmp)
    cum_sum = np.cumsum(scores)
    cum_sum[avg_length:] = cum_sum[avg_length:] - cum_sum[:-avg_length]
    avgs = cum_sum[avg_length-1:] / avg_length
    plt.plot(range(len(avgs)), avgs)
    plt.show()
