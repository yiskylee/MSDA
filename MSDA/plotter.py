from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def setup_pca_plot(exp_var, labels=None, is3d=True):
    fig = plt.figure(figsize=(15, 10))
    if is3d:
        ax = fig.add_subplot(111, projection='3d')
    else:
        ax = fig.add_subplot(111)
    plt.ticklabel_format(style='sci', scilimits=(0, 0))
    plt.tick_params(
        axis='both',
        which='both',  # both major and minor ticks are affected
        bottom='on',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        left='on',
        right='off',
        labelbottom='on',
        labelleft='on')
    all_colors = ['red', 'yellow', 'blue', 'purple', 'orange', 'black', 'grey'] * 5
    all_markers = ['.', '*', 'D', '*', 'v', '^', '<', '>', 'D', 'd']
    all_markers = ['o'] * 20

    label_colors = {}
    label_markers = {}

    # If labels are presented, they represent samples and we are setting up
    # a pca plot
    if labels is not None:
        for i, label in enumerate(set(labels)):
            label_colors[label] = all_colors[i]
            label_markers[label] = all_markers[i]
    # If there are no labels passed to this method, we are setting up
    # a pca loading plot. label_colors and label_markers essentially are equal
    # to all_colors and all_markers
    else:
        for i, color in enumerate(all_colors):
            label_colors[i] = color
        for i, marker in enumerate(all_markers):
            label_markers[i] = marker

    if is3d:
        ax.set_xlabel('PC1 ' + '{:.2%}'.format(exp_var[0]))
        ax.set_ylabel('PC2 ' + '{:.2%}'.format(exp_var[1]))
        ax.set_zlabel('PC3 ' + '{:.2%}'.format(exp_var[2]))
    else:
        ax.set_xlabel('PC1 ' + '{:.2%}'.format(exp_var[0]))
        ax.set_ylabel('PC2 ' + '{:.2%}'.format(exp_var[1]))
    return fig, ax, label_colors, label_markers


def save_pca_plot(fig, ax, plot_range, path):
    if plot_range is not None:
        ax.set_xlim(left=plot_range[0], right=plot_range[1])
        ax.set_ylim(bottom=plot_range[2], top=plot_range[3])
    if path is not None:
        fig.savefig(path)


def pca(exp_var_ratio, x_reduced, num_buckets_per_sample, labels, is3d=False, plot_range=None, path=None):
    #     km = AgglomerativeClustering(n_clusters=3, linkage='ward')
    #     km.fit(xReduced)
    # Get cluster assignment labels
    #     labels = km.labels_
    # Set up pca plot
    fig, ax, label_colors, label_markers = setup_pca_plot(exp_var_ratio, labels, is3d)
    # Each row is a bucket and one sample contains num_buckets rows
    # Each sample is labeled differently but we do not have enough colors and markers
    num_samples = x_reduced.shape[0] / num_buckets_per_sample
    for i in np.arange(num_samples):
        label = labels[i]
        ax.scatter(x_reduced[i * num_buckets_per_sample:(i + 1) * num_buckets_per_sample, 0],
                   x_reduced[i * num_buckets_per_sample:(i + 1) * num_buckets_per_sample, 1],
                   label=label,
                   c=label_colors[label],
                   marker=label_markers[label])
                   #alpha=0.5)
    legend_handles, legend_labels = ax.get_legend_handles_labels()
    unique_labels, ids = np.unique(legend_labels, return_index=True)
    unique_handles = [legend_handles[id] for id in ids]
    plt.legend(unique_handles, unique_labels, loc='best')
    save_pca_plot(fig, ax, plot_range, path)
    # Some annotation code
    # if an == 1:
    #         anno(xReduced, merged, ax, 1)
    #     elif an == 2:
    #         anno(xReduced, merged, ax, 2)
    #     ax.annotate(extractId(merged.index[0]), xy=(xReduced[0,0], xReduced[0,1]+0.02e8),
    #                 xytext=(xReduced[0,0], xReduced[0,1]+0.1e8),
    #                 arrowprops=dict(facecolor='black'),
    #                 horizontalalignment='center', verticalalignment='top')


# return labels


def pca_loadings(pc_scores, loadings, is3d, plot_range=None, path=None):
    fig, ax, label_colors, label_markers = setup_pca_plot(pc_scores, is3d=is3d)
    num_features = loadings.shape[0]
    for i in np.arange(num_features):
        ax.scatter(loadings[i, 0],
                   loadings[i, 1],
                   # c=label_colors[i%len(label_colors)],
                   # marker=label_markers[i%len(label_markers)],
                   alpha=0.5)
    save_pca_plot(fig, ax, plot_range, path)


def plotPCA3D(pc_scores, x_reduced, num_buckets=97, path=None):
    fig, ax, colors, markers = setup_pca_plot(pc_scores, True)
    num_samples = x_reduced.shape[0] / num_buckets
    for i in np.arange(num_samples):
        ax.scatter(x_reduced[i * num_buckets:(i + 1) * num_buckets, 0],
                   x_reduced[i * num_buckets:(i + 1) * num_buckets, 1],
                   x_reduced[i * num_buckets:(i + 1) * num_buckets, 2],
                   c=colors[i % len(colors)],
                   marker=markers[i % len(markers)],
                   alpha=0.5)
    save_pca_plot(fig, ax, None, path)