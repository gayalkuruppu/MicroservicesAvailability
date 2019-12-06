import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd


def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=["black", "white"], threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


data = pd.read_csv('/home/gayal/Downloads/ExploringLimitsOMS/Availability of Micro services'
                   ' based system with replicates - nlog2n.csv')
dataFiltered = data.iloc[27:38, 1:8]
dataNumpy = dataFiltered.to_numpy()
dataInt = dataNumpy.astype('int8')

dimx = dataInt.shape[0]
dimy = dataInt.shape[1]

data2Filtered = data.iloc[53:64, 1:8]
data2Numpy = data2Filtered.to_numpy()
data2Int = data2Numpy.astype('int8')
outArray = np.empty([dimx, dimy], dtype=str)

outArray = dataInt*data2Int

no_of_nodes = ["Monolithic System", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024"]
software_class = ["A_SW class 1", "A_SW class 2", "A_SW class 3", "A_SW class 4", "A_SW class 5", "A_SW class 6",
                  "A_SW class 7"]

fig, ax = plt.subplots()

im, cbar = heatmap(outArray, no_of_nodes, software_class, ax=ax,cmap="YlGn", cbarlabel="Overall Availability Class")

texts = annotate_heatmap(im, valfmt="{x}")
# texts = annotate_heatmap(im, valfmt="t")
plt.ylabel("No of nodes")
plt.xlabel("f(N) = NlogN")
plt.title("Software Availability Classes, If it has improved it's class; else 0")


fig.tight_layout()
plt.show()