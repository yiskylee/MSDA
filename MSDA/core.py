import numpy as np
import os
import time
import pandas as pd
import re
import math
import scipy.sparse as scisp
from sklearn.utils.extmath import randomized_svd
from sklearn.utils.sparsefuncs import mean_variance_axis, inplace_column_scale
import sys
import sklearn.decomposition as sk_decomp


def csc_npz_to_txt(input_file_path):
    root_dir = os.path.split(input_file_path)[0]
    file_name, file_extension = \
        os.path.splitext(os.path.basename(input_file_path))
    loader = np.load(input_file_path)
    for component in ['data', 'indices', 'indptr', 'shape']:
        comp_file_name = file_name + '_' + component + '.txt'
        comp_file_path = os.path.join(root_dir, comp_file_name)
        print 'output path: ', comp_file_path
        if component == 'data':
            print loader[component].shape
            np.savetxt(comp_file_path, loader[component])
        else:
            np.savetxt(comp_file_path, loader[component], fmt='%d')


def save_sparse_csc(filename, array):
    np.savez(filename, data=array.data, indices=array.indices,
             indptr=array.indptr, shape=array.shape)


def load_sparse_csc(filename):
    loader = np.load(filename)
    return scisp.csc_matrix((loader['data'], loader['indices'],
                             loader['indptr']), shape=loader['shape'])


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def pat_mat(df, DA):
    num_bins = math.ceil(float(df.mass.max() - df.mass.min()) / float(DA))
    labels = pd.cut(df.mass, num_bins)
    max_idx = df.groupby([labels])['intensity'].agg(
        lambda x: x.idxmax()).dropna()
    merged_mass = df.mass[max_idx.values]
    pivot_df = df.pivot('mass', 'sampleId', 'intensity').fillna(0)
    labels = pd.cut(pivot_df.index, num_bins)
    merged_df = pivot_df.groupby([labels]).max().dropna()
    merged_df.index = merged_mass
    #     mergedDf.dropna(how='all', inplace=True)
    return merged_df.T


def gen_pat_mat_old(peak_dir, DA, neg_or_pos):
    pattern = '.*' + neg_or_pos + '$'
    sample_lists = []
    start = time.time()
    i = 0
    id_list = []
    for root, dirs, filenames in os.walk(peak_dir):
        for filename in filenames:
            if root[-1] == '/':
                input_file = root + filename
            else:
                input_file = root + '/' + filename
            if re.match(pattern, root.lower(), re.M | re.I):
                if 'binned' in input_file.lower():
                    id1 = root.split('_')[-2]
                    id2 = ''
                    for s in filename.split('.')[0].split('_'):
                        if id1 != '9':
                            if is_number(s) and len(s) < 6:
                                id2 = s
                        else:
                            if is_number(s):
                                if len(s) > 2:
                                    id2 = id2 + s[-2:]
                                if len(s) == 2:
                                    id2 = id2 + s
                    id_list.append(id1 + '_' + id2)
                    feat_list = pd.read_csv(input_file)
                    feat_list['sampleId'] = id1 + '_' + id2
                    sample_lists.append(feat_list)
                    i = i + 1
    df = pd.concat(sample_lists, ignore_index=True)
    pm = pat_mat(df, DA)
    print time.time() - start
    print 'number of samples', i
    return pm


def gen_pat_mat(sample_mat, buckets, bins):
    sample_mat[np.isnan(sample_mat)] = 0
    scan_num = sample_mat[:, 0]
    mass = sample_mat[:, 1]
    num_buckets = len(buckets)
    num_bins = len(bins) - 1
    bucket_idx = np.bincount(np.digitize(scan_num, buckets)).cumsum()[:-1]
    bucket_arrays = np.split(sample_mat, bucket_idx)[1:]
    pat_mat = np.zeros((int(num_buckets), int(num_bins)), dtype=np.float32)
    # patMat = csc_matrix((int(numBuckets), int(numBins)))
    for i, bucket in enumerate(bucket_arrays):
        mass = bucket[:, 1]
        intensity = bucket[:, 2]
        pat_mat[i, :] = np.histogram(mass, bins=bins, weights=intensity)[0]
    return pat_mat

def gen_master_peak_list(sample_mat, buckets, bins):
    sample_mat[np.isnan(sample_mat)] = 0
    scan_num = sample_mat[:, 0]
    mass = sample_mat[:, 1]
    num_buckets = len(buckets)
    num_bins = len(bins) - 1
    bucket_idx = np.bincount(np.digitize(scan_num, buckets)).cumsum()[:-1]
    bucket_arrays = np.split(sample_mat, bucket_idx)[1:]
    bucket = bucket_arrays[0]
    mass = bucket[:, 1]
    intensity = bucket[:, 2]
    accu_intensity = np.histogram(mass, bins=bins, weights=intensity)[0]
    master_peak_list = pd.DataFrame(data={'mass': mass, 
                                          'intensity': intensity})
    return master_peak_list.sort_values(by='mass')[['mass', 'intensity']]


def gen_big_pat_mat(root_dir, bucket_size, bin_size, first_scan, last_scan, excluded_mass=None):
#     min_mass = 50.01068878
#     max_mass = 800.21398926
    if not os.path.exists(root_dir):
        print "Directory ", root_dir, " does not exist, exiting..."
        sys.exit(-1)
    min_mass = 50
    max_mass = 550
    bins = np.arange(min_mass, max_mass + bin_size, bin_size)
    buckets = np.arange(first_scan, last_scan, bucket_size)
    pat_mats = []
    times = []
    filenames = [x for x in os.listdir(root_dir) if '.csv' in x]
    for i, filename in enumerate(filenames):
        start = time.time()
        input_file_path = os.path.join(root_dir, filename)
        print i
        sample = pd.read_csv(input_file_path, header=None).as_matrix().astype(np.float32)
        dense_pat_mat = gen_pat_mat(sample, buckets, bins)
        # pat_mat = csc_matrix(dense_pat_mat)
        pat_mats.append(scisp.csc_matrix(dense_pat_mat))
        del dense_pat_mat
        times.append(time.time() - start)
    pat_mat_all = scisp.vstack(pat_mats, format='csc')
    print 'pat_mat_all type: ', type(pat_mat_all)
    # Take out columns that contain excluded mass if exclude_mass exists
    print 'before exclusion: ', pat_mat_all.shape
    if excluded_mass is not None:
        excluded_idx = np.digitize(excluded_mass, bins) - 1
        # Delete the excluced_idx, can also use np.delete
        # see: https://docs.scipy.org/doc/numpy/reference/generated/numpy.delete.html
        mask = np.ones(pat_mat_all.shape[1], dtype=bool)
        mask[excluded_idx] = False
        pat_mat_all = pat_mat_all[:, mask]
    # Take out columns that have only zeroes
    print 'after exclusion of mass: ', pat_mat_all.shape
    mask = (np.diff(pat_mat_all.indptr) != 0)
    pat_mat_all = pat_mat_all[:, mask]
    # Another way to delete zero columns is to use all, but it does not work on sparse array
    # pat_mat_all = pat_mat_all[:, ~np.all(pat_mat_all==0, axis=0)]
    # store the pattern matrix in a csc format because it is very sparse
    print 'after exclusion of non zero: ', pat_mat_all.shape
    return pat_mat_all


def gen_labels(root_dir, label_file_path):
    if not os.path.exists(root_dir):
        print "Directory ", root_dir, " does not exist, exiting..."
        sys.exit(-1)
    label_file = pd.read_csv(label_file_path)
    label_by_file = dict(zip(label_file['Raw File Name'], label_file['Birth Outcome']))
    labels = []
    for root, dirs, filenames in os.walk(root_dir):
        for filename in [x for x in filenames if '.csv' in x]:
            label = label_by_file[os.path.splitext(filename)[0]]
            labels.append(label)
    return labels

def truncated_svd(x, n_components):
    u, sigma, v_t = randomized_svd(x, n_components, n_iter=5, random_state=42)
    x_trans = np.dot(u, np.diag(sigma))
    loading = np.transpose(v_t)
    exp_var = np.var(x_trans, axis=0)
    _, full_var = mean_variance_axis(x, axis=0)
    full_var = full_var.sum()
    exp_var_ratio = exp_var / full_var
    # exp_var_ratio = sigma / u.shape[0]
#     svd = TruncatedSVD(n_components=n_components)
#     xReduced = svd.fit_transform(patMat)
    return x_trans, loading, exp_var_ratio


def dense_pca(x, n_components):
    pca = sk_decomp.PCA(n_components=n_components)
    x_trans = pca.fit_transform(x)
    loading = np.transpose(pca.components_)
    return x_trans, loading, pca.explained_variance_ratio_


def scaling(pat_mat):
    mean, var = mean_variance_axis(pat_mat, axis=0)
    # var[var == 0.0] = 1.0
    inplace_column_scale(pat_mat, 1 / np.sqrt(var))