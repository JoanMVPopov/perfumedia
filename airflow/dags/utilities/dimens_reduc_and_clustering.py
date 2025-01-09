import ast
import os

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap
from sklearn.neighbors import NearestNeighbors
from scipy.signal import argrelextrema
from kneed import KneeLocator
from sklearn.cluster import (KMeans, MeanShift, AffinityPropagation,
                             AgglomerativeClustering, DBSCAN, HDBSCAN, OPTICS,
                             SpectralClustering)
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, mean_squared_error
from sklearn.model_selection import ParameterGrid
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, LocallyLinearEmbedding, MDS, Isomap

# ==== ADDED CODE START (DUNN & DAVIES-BOULDIN) ====
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import pairwise_distances


def multi_replace(mat, delta=None):
    """
    Performs multiplicative replacement on compositional data to handle zeros.
    Crucial for compositional data analysis where zeros can't be processed directly.
    """
    mat = closure(mat)
    z_mat = mat == 0

    num_feats = mat.shape[-1]
    tot = z_mat.sum(axis=-1, keepdims=True)

    if delta is None:
        delta = (1.0 / num_feats) ** 2

    zcnts = 1 - tot * delta
    if np.any(zcnts < 0):
        raise ValueError("The multiplicative replacement created negative proportions. Consider using a smaller delta.")
    mat = np.where(z_mat, delta, zcnts * mat)
    return mat.squeeze()


def closure(mat):
    """
    Applies closure operation to ensure compositional data sums to 1.
    Essential for maintaining the constant sum constraint of compositional data.
    """
    mat = np.atleast_2d(mat)
    if np.any(mat < 0):
        raise ValueError("Cannot have negative proportions")
    if mat.ndim > 2:
        raise ValueError("Input matrix can only have two dimensions or less")
    if np.all(mat == 0, axis=1).sum() > 0:
        raise ValueError("Input matrix cannot have rows with all zeros")
    mat = mat / mat.sum(axis=1, keepdims=True)
    return mat.squeeze()


def clr(mat):
    """
    Applies centered log-ratio transformation to compositional data.
    Makes the data suitable for standard statistical analyses while preserving compositional properties.
    """
    mat = closure(mat)
    lmat = np.log(mat)
    gm = lmat.mean(axis=-1, keepdims=True)
    return (lmat - gm).squeeze()

def estimate_dbscan_params(data, min_pts_method='default', plot=True):
    """
    Estimate DBSCAN parameters (eps and min_samples)

    Parameters:
    data: array-like of shape (n_samples, n_features)
    min_pts_method: str, 'default' or 'dims'
        'default': uses 4 for 2D data
        'dims': uses 2 * dimensions
    plot: bool, whether to show the k-distance plot

    Returns:
    dict with estimated parameters and metrics
    """
    # Calculate min_samples (MinPts)
    dims = data.shape[1]
    if min_pts_method == 'default':
        min_samples = 4 if dims == 2 else dims
    else:  # 'dims'
        min_samples = 2 * dims

    # Calculate distances to k-nearest neighbors
    neighbors = NearestNeighbors(n_neighbors=min_samples)
    neighbors_fit = neighbors.fit(data)
    distances, _ = neighbors_fit.kneighbors(data)

    # Calculate mean of distances excluding the point itself (distance=0)
    mean_distances = np.mean(distances[:, 1:], axis=1)

    # Sort distances for knee detection
    sorted_distances = np.sort(mean_distances)

    # Find the knee point using multiple methods
    # 1. Kneed library
    knee_locator = KneeLocator(
        range(len(sorted_distances)),
        sorted_distances,
        curve='convex',
        direction='increasing'
    )
    knee_distance = sorted_distances[knee_locator.elbow] if knee_locator.elbow else None

    # 2. Local maxima of curvature
    # Calculate first derivative
    first_derivative = np.gradient(sorted_distances)
    # Calculate second derivative
    second_derivative = np.gradient(first_derivative)
    # Find local maxima of second derivative (points of maximum curvature)
    local_maxima_idx = argrelextrema(second_derivative, np.greater)[0]

    # Select the most prominent local maximum in the first half of the curve
    first_half_maxima = local_maxima_idx[local_maxima_idx < len(sorted_distances) // 2]
    if len(first_half_maxima) > 0:
        curvature_distance = sorted_distances[first_half_maxima[0]]
    else:
        curvature_distance = None

    # Choose epsilon based on available methods
    if knee_distance is not None:
        eps = knee_distance
        method = 'knee'
    elif curvature_distance is not None:
        eps = curvature_distance
        method = 'curvature'
    else:
        # Fallback: use the mean of the k-distances
        eps = np.mean(sorted_distances)
        method = 'mean'

    # if plot:
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(range(len(sorted_distances)), sorted_distances, 'b-')
    #     plt.axhline(y=eps, color='r', linestyle='--',
    #                label=f'Estimated eps ({method})')
    #     plt.xlabel('Points sorted by distance')
    #     plt.ylabel(f'Mean distance to {min_samples} nearest neighbors')
    #     plt.title('K-distance Graph for DBSCAN Parameter Estimation')
    #     plt.legend()
    #     plt.show()

    return {
        'min_samples': min_samples,
        'eps': eps,
        'estimation_method': method,
        'knee_distance': knee_distance,
        'curvature_distance': curvature_distance
    }


def dunn_index(X, labels):
    """
    Computes the Dunn Index for a given dataset X and cluster labels.
    Dunn Index = min(inter-cluster distance) / max(intra-cluster diameter).

    - If there's only 1 cluster (or all points in noise for density-based methods),
      returns -1 as an invalid result.
    - Ignores noise points labeled as -1.
    """
    unique_clusters = np.unique(labels)
    # Remove noise if present
    if -1 in unique_clusters:
        unique_clusters = unique_clusters[unique_clusters != -1]

    # If there's fewer than 2 clusters, Dunn Index is undefined
    if len(unique_clusters) < 2:
        return -1

    # Precompute all pairwise distances once
    dist = pairwise_distances(X)

    # Calculate the diameter (max intra-cluster distance) for each cluster
    diameters = []
    for cluster in unique_clusters:
        points_in_cluster = np.where(labels == cluster)[0]
        if len(points_in_cluster) <= 1:
            # If the cluster has only 1 point, diameter is 0
            diameters.append(0)
        else:
            cluster_distances = dist[np.ix_(points_in_cluster, points_in_cluster)]
            diameters.append(cluster_distances.max())

    # Calculate the minimum inter-cluster distance
    # by looking at all pairs of clusters
    inter_cluster_dists = []
    for i in range(len(unique_clusters)):
        for j in range(i + 1, len(unique_clusters)):
            c1_points = np.where(labels == unique_clusters[i])[0]
            c2_points = np.where(labels == unique_clusters[j])[0]
            inter_cluster_dists.append(dist[np.ix_(c1_points, c2_points)].min())

    if len(inter_cluster_dists) == 0:
        return -1

    min_inter_dist = np.min(inter_cluster_dists)
    max_diameter = np.max(diameters)

    if max_diameter == 0:  # Avoid division by zero
        return -1

    return min_inter_dist / max_diameter


# ==== ADDED CODE END (DUNN & DAVIES-BOULDIN) ====


# def preprocess_data(df):
#     """
#     Preprocesses the data by applying CLR transformation to compositional data
#     and standardizing only the non-compositional features.
#     """
#     X = None

#     exploded_dict = {}

#     for index, category_row in enumerate(df['Category'])

#     # Process compositional data (Categories)
#     for i in range(1, 5):
#         category_data = np.vstack(df[f'Category{i}'].apply(
#             lambda x: clr(multi_replace(np.array(x)))
#         ))
#         if i == 1:
#             X = category_data
#         else:
#             X = np.hstack([X, category_data])


#     # Process non-compositional data (Ratings)
#     ratings = df[['Rating1', 'Rating2', 'Rating3', 'Rating4', 'Rating5']].values
#     scaler = StandardScaler()
#     ratings_scaled = scaler.fit_transform(ratings)

#     # Combine the CLR-transformed compositional data with scaled ratings
#     X = np.hstack([X, ratings_scaled])

#     return X

def preprocess_data(df, categories, rating_names):
    """
    Preprocesses the data by applying CLR transformation to compositional data
    and standardizing only the non-compositional features.
    """
    X = pd.DataFrame()

    for category in categories:
        exploded_dict = {}

        df_type = df[category].apply(lambda x: ast.literal_eval(x))
        df_type_nums = df[f'{category}_numbers'].apply(lambda x: ast.literal_eval(x))

        df_type_nums_rescaled = df_type_nums.apply(lambda x: clr(multi_replace(np.array(x))))

        for index, category_row in enumerate(df_type):
            for index_cat, category_curr_name in enumerate(category_row):
                if category_curr_name not in exploded_dict:
                    exploded_dict[category_curr_name] = [0] * len(df_type_nums_rescaled)

                exploded_dict[category_curr_name][index] = df_type_nums_rescaled.iloc[index][index_cat]

        X = pd.concat([X, pd.DataFrame(exploded_dict)], axis=1)

    scaler = StandardScaler()
    ratings = df[rating_names].values
    ratings_scaled = scaler.fit_transform(ratings)

    rescaled_ratings_df = pd.DataFrame(ratings_scaled, columns=rating_names)

    X = pd.concat([X, rescaled_ratings_df], axis=1)

    return X.to_numpy(), X.columns.tolist()


def get_clustering_algorithms():
    """
    Returns a dictionary of clustering algorithms with their parameters.
    Each algorithm is configured with appropriate parameter ranges and constraints.
    """
    return {
        "KMeans": {
            "model": KMeans(random_state=42),
            "params": {
                "n_clusters": range(2, 15),
                "init": ["k-means++"],
                "n_init": [10]
            }
        },
        # "MeanShift": {
        #     "model": MeanShift(),
        #     "params": {
        #         "bandwidth": list(np.arange(0.1, 5, 0.25)) + [None],
        #         "bin_seeding": [False, True]
        #     }
        # },
        "AffinityPropagation": {
            "model": AffinityPropagation(random_state=42),
            "params": {
                "damping": np.arange(0.5, 1, 0.05)
            }
        },
        "Agglomerative": {
            "model": AgglomerativeClustering(),
            "params": {
                "n_clusters": range(2, 15),
                "linkage": ["ward", "complete", "average"],
                "metric": ["euclidean"]
            }
        },
        "DBSCAN": {
            "model": DBSCAN(),
            "params": {
                "eps": np.arange(0.1, 2.1, 0.2),
                "min_samples": [3, 5, 7, 10],
                "metric": ["euclidean"]
            }
        },
        "HDBSCAN": {
            "model": HDBSCAN(),
            "params": {
                "min_cluster_size": np.arange(5, 30, 5),
                "min_samples": np.arange(1, 3, 1),
                "cluster_selection_epsilon": np.arange(0.2, 4, 0.2),
            }
        },
        "GaussianMixture": {
            "model": GaussianMixture(random_state=42),
            "params": {
                "n_components": range(2, 8),
                "covariance_type": ["full", "tied", "diag", "spherical"]
            }
        },
        "SpectralClustering": {
            "model": SpectralClustering(random_state=42),
            "params": {
                "n_clusters": range(2, 8),
                "affinity": ["rbf", "nearest_neighbors"],
                "n_neighbors": range(2, 8)
            }
        },
        # "OPTICS": {
        #     "model": OPTICS(),
        #     "params": {
        #         "min_samples": np.arange(2, 10, 1),
        #         "max_eps": [np.inf],
        #         "metric": ["euclidean"],
        #         "cluster_method": ["xi", "dbscan"]
        #     }
        # }
    }


def apply_dimensionality_reduction(X, method='pca', random_state=42, n_components=2,
                                   tsne_perplexity=30, umap_n_neighbors=30, umap_min_dist=0.0):
    """
    Applies specified dimensionality reduction technique and returns both
    the reducer model and the reduced data.
    """
    if method == 'pca':
        reducer = PCA(n_components=n_components)
    elif method == 'tsne':
        reducer = TSNE(n_components=n_components, random_state=random_state,
                       perplexity=tsne_perplexity)
    elif method == 'umap':
        reducer = umap.UMAP(n_components=n_components, random_state=random_state,
                            n_neighbors=umap_n_neighbors, min_dist=umap_min_dist)
    elif method == 'lle':
        reducer = LocallyLinearEmbedding(n_components=n_components, random_state=random_state)
    elif method == 'mds':
        reducer = MDS(n_components=n_components, random_state=random_state)
    elif method == "isomap":
        reducer = Isomap(n_components=n_components)
    else:
        raise ValueError(f"Unknown dimensionality reduction method: {method}")

    X_reduced = reducer.fit_transform(X)
    return reducer, X_reduced


def evaluate_clustering(model, X):
    """
    Evaluates clustering using multiple metrics.
    Returns scores and labels, handling special cases for different algorithms.
    """
    labels = None

    if isinstance(model, GaussianMixture):
        labels = model.fit_predict(X)
    else:
        labels = model.fit_predict(X)

    unique_labels = np.unique(labels)
    n_noise = np.sum(labels == -1) if -1 in labels else 0

    # If there's effectively 1 cluster (or 0 valid clusters), we can't compute these metrics
    if len(unique_labels) < 2 or (len(unique_labels) == 2 and -1 in labels):
        return {
            'silhouette': -1,
            'calinski_harabasz': -1,
            # ==== ADDED CODE START (DUNN & DAVIES-BOULDIN) ====
            'davies_bouldin': -1,
            'dunn_index': -1,
            'n_clusters': -1,
            'n_noise': 0,
            # ==== ADDED CODE END (DUNN & DAVIES-BOULDIN) ====
            'labels': labels
        }

    # Remove noise points for score calculation if present
    if -1 in labels:
        mask = labels != -1
        X_clean = X[mask]
        labels_clean = labels[mask]
    else:
        X_clean = X
        labels_clean = labels

    try:
        sil_score = silhouette_score(X_clean, labels_clean)
        ch_score = calinski_harabasz_score(X_clean, labels_clean)
        # ==== ADDED CODE START (DUNN & DAVIES-BOULDIN) ====
        db_score = davies_bouldin_score(X_clean, labels_clean)
        dunn_score = dunn_index(X_clean, labels_clean)
        # ==== ADDED CODE END (DUNN & DAVIES-BOULDIN) ====
    except:
        sil_score = -1
        ch_score = -1
        # ==== ADDED CODE START (DUNN & DAVIES-BOULDIN) ====
        db_score = -1
        dunn_score = -1
        # ==== ADDED CODE END (DUNN & DAVIES-BOULDIN) ====

    # print(len(unique_labels) - (1 if -1 in labels else 0))

    return {
        'silhouette': sil_score,
        'calinski_harabasz': ch_score,
        # ==== ADDED CODE START (DUNN & DAVIES-BOULDIN) ====
        'davies_bouldin': db_score,
        'dunn_index': dunn_score,
        # ==== ADDED CODE END (DUNN & DAVIES-BOULDIN) ====
        'labels': labels,
        'n_clusters': len(unique_labels) - (1 if -1 in labels else 0),
        'n_noise': n_noise
    }


def plot_clusters(X_reduced, labels, title, ax=None):
    """
    Creates a scatter plot of clusters in 2D space.
    Handles noise points (-1 labels) differently from regular clusters.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(20, 20))

    unique_labels = np.unique(labels)
    # colors = plt.cm.viridis(np.linspace(0, 1, len(unique_labels)))
    colors = sns.husl_palette(n_colors=len(unique_labels), h=.5)

    for label, color in zip(unique_labels, colors):
        mask = labels == label
        if label == -1:
            ax.scatter(X_reduced[mask, 0], X_reduced[mask, 1],
                       c='gray', marker='x', label='Noise')
        else:
            ax.scatter(X_reduced[mask, 0], X_reduced[mask, 1],
                       c=[color], label=f'Cluster {label}')

    ax.set_title(title)
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    return ax


def pca_explained_variance_info(X, feature_names,
                                decade, gender, current_dir, folder_name,
                                pca_target_explained_var=0.95):
    current_explained_var = -1
    current_pca_dim = 1

    explained_variance_ratio = None
    pca_mse = None
    reducer = None
    X_reduced = None

    while current_explained_var < pca_target_explained_var:
        reducer, X_reduced = apply_dimensionality_reduction(X, method="pca",
                                                            n_components=current_pca_dim)

        X_pca_inv = reducer.inverse_transform(X_reduced)
        pca_mse = mean_squared_error(X, X_pca_inv)
        print("PCA Reconstruction Error (MSE):", pca_mse)

        # Get explained variance ratio for each component
        explained_variance_ratio = reducer.explained_variance_ratio_
        cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

        current_explained_var = cumulative_variance_ratio[-1]

        current_pca_dim += 1

    current_pca_dim -= 1

    # Create plots
    plt.figure(figsize=(6, 8))

    # Bar plot for individual explained variance
    plt.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio)
    plt.xticks(np.arange(1, len(explained_variance_ratio) + 1), np.arange(len(explained_variance_ratio)))
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance Ratio')
    plt.title('Individual Explained Variance')

    # Add reconstruction error text below plot
    plt.figtext(0.5, 0.02, f'Reconstruction Error (MSE): {pca_mse:.4f}',
                ha='center', va='center', fontsize=10)

    # Adjust layout to prevent text overlap
    plt.subplots_adjust(bottom=0.15)

    # plt.show()

    file_name = f'{decade}_{gender}_{current_pca_dim}d_bar_explained_variance.png'
    file_path_bar_explained_variance = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_bar_explained_variance, bbox_inches='tight')

    # Get and show loadings (contributions of features to components)
    loadings = reducer.components_.T

    n_features = len(loadings[:, 0])

    # TODO: NEED TO CHANGE THIS FOR PERFUMEDIA
    # feature_names = [f"Feature {i+1}" for i in range(n_features)]
    # feature_names = X_df.columns.tolist()

    # Visualize loadings for the first two components
    # plt.figure(figsize=(18, 6))
    # x_labels = np.arange(len(feature_names))

    #width = 0.4

    #plt.bar(x_labels - width / 2, loadings[:, 0], width, label='PC1')
    #plt.bar(x_labels + width / 2, loadings[:, 1], width, label='PC2')

    # # Calculate bar width based on number of components
    # # Ensure bars don't overlap but also don't get too thin
    # width = min(0.8 / current_pca_dim, 0.35)  # Adjust these values as needed
    # offsets = np.linspace(-(width * current_pca_dim) / 2,
    #                       (width * current_pca_dim) / 2,
    #                       current_pca_dim)
    #
    # # Plot bars for each principal component
    # for i in range(current_pca_dim):
    #     plt.bar(x_labels + offsets[i],
    #             loadings[:, i],
    #             width,
    #             label=f'PC{i + 1}')

    width = 0.4
    x_labels = np.arange(len(feature_names))

    for i in range(current_pca_dim):
        plt.figure(figsize=(18, 6))

        plt.bar(x_labels,
                loadings[:, i],
                width,
                label=f'PC{i + 1}')

        plt.xticks(x_labels, feature_names, rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Loadings')
        plt.title(f'Feature Loadings for PC{i+1}')
        plt.legend()
        plt.tight_layout()
        # plt.show()

        file_name = f'{decade}_{gender}_{current_pca_dim}d_component_{i}_loadings.png'
        file_path_pca_loadings = os.path.join(current_dir, folder_name, file_name)
        plt.savefig(file_path_pca_loadings, bbox_inches='tight')

    return reducer, X_reduced


def perform_clustering_algos_permutations(do_plots, method, reducer, X_reduced, clustering_algorithms,
                                          results, decade, gender, method_idx,
                                          current_dir, folder_name):

    fig, axs = plt.subplots(5, 2, figsize=(30, 40)) if do_plots else (None, None)

    if method == "tsne":
        # t-SNE internally minimizes the KL divergence. After fitting, you can access:
        tsne_kl = reducer.kl_divergence_
        print("t-SNE KL Divergence (not an MSE in original space):", tsne_kl)

    if method == "lle":
        lle_error = reducer.reconstruction_error_
        print("LLE Reconstruction Error (internal measure):", lle_error)

    if method == "mds":
        mds_stress = reducer.stress_
        print("MDS Stress (distance-based error, not MSE):", mds_stress)

    for algo_idx, (algo_name, algo_info) in enumerate(clustering_algorithms.items()):
        print(f"Testing {algo_name}...")
        model = algo_info["model"]
        param_grid = algo_info["params"]

        best_score = -1
        best_result = None

        current_algo_results = []
        max_sil_score = -1
        min_sil_score = np.inf
        max_cal_score = -1
        min_cal_score = np.inf
        max_db_score = -1
        min_db_score = np.inf
        max_dunn_score = -1
        min_dunn_score = np.inf

        # do the DBSCAN parameter optimization
        if algo_name == 'DBSCAN':
            print("+ Estimating DBSCAN params..")
            best_params = estimate_dbscan_params(X_reduced)

            range_eps = [best_params['eps'] + (best_params['eps'] / 100) * i for i in range(-2, 3, 1)]
            range_min_samples = [best_params['min_samples'] + i for i in range(-2, 2, 1)]

            param_grid = {
                'eps': range_eps,
                'min_samples': range_min_samples
            }

        # iterate through all possible permutations
        for params in ParameterGrid(param_grid):
            model.set_params(**params)
            try:
                scores = evaluate_clustering(model, X_reduced)

                if scores['silhouette'] > max_sil_score:
                    max_sil_score = scores['silhouette']
                if scores['silhouette'] < min_sil_score:
                    min_sil_score = scores['silhouette']
                if scores['calinski_harabasz'] > max_cal_score:
                    max_cal_score = scores['calinski_harabasz']
                if scores['calinski_harabasz'] < min_cal_score:
                    min_cal_score = scores['calinski_harabasz']
                if scores['davies_bouldin'] > max_db_score:
                    max_db_score = scores['davies_bouldin']
                if scores['davies_bouldin'] < min_db_score:
                    min_db_score = scores['davies_bouldin']
                if scores['dunn_index'] > max_dunn_score:
                    max_dunn_score = scores['dunn_index']
                if scores['dunn_index'] < min_dunn_score:
                    min_dunn_score = scores['dunn_index']

                current_algo_results.append(
                    {
                        "algorithm": algo_name,
                        "params": params,
                        "scores": scores,
                        "reduction_method": method
                    }
                )

            except Exception as e:
                print(f"Error with {algo_name} and params {params}: {e}")

        fin_score = -1
        best_index = -1

        # do the min-max leaderboard
        for index_res, res in enumerate(current_algo_results):
            if max_sil_score == min_sil_score:
                continue
            min_max_sil_score = 100 * (
                    (res['scores']['silhouette'] - min_sil_score) / (max_sil_score - min_sil_score))
            if max_cal_score == min_cal_score:
                continue
            min_max_cal_score = 100 * (
                    (res['scores']['calinski_harabasz'] - min_cal_score) / (max_cal_score - min_cal_score))
            if max_db_score == min_db_score:
                continue
            # LOWER IS BETTER FOR DB
            min_max_db_score = 100 * (
                    (res['scores']['davies_bouldin'] - max_db_score) / (max_db_score - min_db_score))
            if max_dunn_score == min_dunn_score:
                continue
            min_max_dunn_score = 100 * (
                    (res['scores']['dunn_index'] - min_dunn_score) / (max_dunn_score - min_dunn_score))

            final_score = min_max_cal_score + min_max_sil_score + min_max_db_score + min_max_dunn_score
            final_score = final_score - (
                        final_score * (res['scores']['n_noise'] / len(res['scores']['labels'])))

            if final_score > fin_score:
                fin_score = final_score
                best_index = index_res

        if best_index != -1:
            best_result = current_algo_results[best_index]
            best_result['final_score'] = fin_score
        else:
            # if all results are the same, it will not show up, that's why we need this else statement
            # also, we need more than 1 cluster
            if current_algo_results[0]['scores']['n_clusters'] > 1:
                best_result = current_algo_results[0]
                best_result['final_score'] = 400.0

        if best_result:
            results.append(best_result)
            if do_plots:
                plot_clusters(
                    X_reduced,
                    best_result['scores']['labels'],
                    f"{method.upper()} + {algo_name}",
                    ax=axs[algo_idx // 2][algo_idx % 2]
                )
        else:
            if do_plots:
                axs[algo_idx // 2][algo_idx % 2].text(0.5, 0.5,
                                                      "Only 1 cluster found\nResults invalidated",
                                                      horizontalalignment='center',
                                                      verticalalignment='center',
                                                      transform=axs[algo_idx // 2][algo_idx % 2].transAxes,
                                                      fontsize=14,
                                                      fontweight='bold',
                                                      color='red')

                axs[algo_idx // 2][algo_idx % 2].set_title(f"{method.upper()} + {algo_name}")
                axs[algo_idx // 2][algo_idx % 2].set_xlabel('Component 1')
                axs[algo_idx // 2][algo_idx % 2].set_ylabel('Component 2')

    if do_plots:
        plt.tight_layout()
        # plt.show()

        file_name = f'{decade}_{gender}_{method}_{method_idx}_2D_all_clustering_algos.png'
        file_path_2D_all_clustering_algos = os.path.join(current_dir, folder_name, file_name)
        plt.savefig(file_path_2D_all_clustering_algos, bbox_inches='tight')


def min_max_all_indices(results):
    max_sil_score = -1
    min_sil_score = np.inf
    max_cal_score = -1
    min_cal_score = np.inf
    max_db_score = -1
    min_db_score = np.inf
    max_dunn_score = -1
    min_dunn_score = np.inf

    for res in results:
        if res['scores']['silhouette'] > max_sil_score:
            max_sil_score = res['scores']['silhouette']
        if res['scores']['silhouette'] < min_sil_score:
            min_sil_score = res['scores']['silhouette']
        if res['scores']['calinski_harabasz'] > max_cal_score:
            max_cal_score = res['scores']['calinski_harabasz']
        if res['scores']['calinski_harabasz'] < min_cal_score:
            min_cal_score = res['scores']['calinski_harabasz']
        if res['scores']['davies_bouldin'] > max_db_score:
            max_db_score = res['scores']['davies_bouldin']
        if res['scores']['davies_bouldin'] < min_db_score:
            min_db_score = res['scores']['davies_bouldin']
        if res['scores']['dunn_index'] > max_dunn_score:
            max_dunn_score = res['scores']['dunn_index']
        if res['scores']['dunn_index'] < min_dunn_score:
            min_dunn_score = res['scores']['dunn_index']

    for index_res, res in enumerate(results):
        # Higher is better. It measures how well-separated and compact clusters are
        if max_sil_score == min_sil_score:
            continue
        min_max_sil_score = 100 * ((res['scores']['silhouette'] - min_sil_score) / (max_sil_score - min_sil_score))
        # Higher is better. It assesses cluster separation and compactness relative to within-cluster variance.
        if max_cal_score == min_cal_score:
            continue
        min_max_cal_score = 100 * (
                    (res['scores']['calinski_harabasz'] - min_cal_score) / (max_cal_score - min_cal_score))
        # Higher is better. It evaluates the minimum inter-cluster distance relative to the maximum intra-cluster distance.
        if max_db_score == min_db_score:
            continue
        min_max_db_score = 100 * ((res['scores']['davies_bouldin'] - min_db_score) / (max_db_score - min_db_score))
        # Lower is better. It measures average similarity between each cluster and the most similar one.
        if max_dunn_score == min_dunn_score:
            continue
        min_max_dunn_score = 100 * ((res['scores']['dunn_index'] - max_dunn_score) / (min_dunn_score - max_dunn_score))

        final_score = min_max_cal_score + min_max_sil_score + min_max_db_score + min_max_dunn_score

        final_score = final_score - (
                final_score * (res['scores']['n_noise'] / len(res['scores']['labels'])))

        results[index_res]['final_score'] = final_score

    return results

def perform_all_clustering_analysis(X,
                                decade, gender, current_dir, folder_name):
    """
    Performs comprehensive clustering analysis using multiple algorithms
    and dimensionality reduction techniques.
    """
    # X, feature_names = preprocess_data(df, categories, rating_names)
    #dim_reduction_methods = ['pca', 'tsne', 'umap', 'lle', 'mds']

    # pca is unreliable given that explained variance for 2d is ~55%
    # tsne is for visualization, probably should not use it


    # dim_reduction_methods = ['umap'] * 5
    # umap_temp = [10, 20, 30, 40, 50]

    dim_reduction_methods = ['umap', 'lle', 'isomap', 'mds']

    clustering_algorithms = get_clustering_algorithms()

    results = []

    for method_idx, method in enumerate(dim_reduction_methods):
        print(f"\nApplying {method.upper()} dimensionality reduction...")

        reducer, X_reduced = apply_dimensionality_reduction(X, method=method,
                                                            tsne_perplexity=90, umap_n_neighbors=50,
                                                            umap_min_dist=0.0)

        perform_clustering_algos_permutations(True, method, reducer, X_reduced, clustering_algorithms,
                                              results, decade, gender, method_idx,
                                              current_dir, folder_name)

    return results


def perform_curated_choice(X, feature_names, pca_tev,
                decade, gender, current_dir, folder_name):

    clustering_algorithms = get_clustering_algorithms()

    curated_pca_results = []

    pca_reducer, X_pca_reduced = pca_explained_variance_info(X, feature_names,
                                                             decade, gender, current_dir, folder_name,
                                                             pca_target_explained_var=pca_tev)

    perform_clustering_algos_permutations(False, "pca", pca_reducer, X_pca_reduced, clustering_algorithms,
                                          curated_pca_results, decade, gender, -1,
                                          current_dir, folder_name)

    return curated_pca_results


def select_final_candidates(sorted_res, dimens_methods):

    final_candidates = []

    # for method in ['pca', 'tsne', 'umap', 'lle', 'mds']:
    # for method in ['pca', 'lle', 'mds']:
    for method in dimens_methods:
        method_results = [r for r in sorted_res if r['reduction_method'] == method]
        n_clusters_majority = {}
        candidate_without_noise = []
        if method_results:
            for curr_result in method_results:
                curr_num_cl = curr_result['scores']['n_clusters']
                #if curr_result['scores']['n_noise'] == 0:

                # if the noise is <= than 5% of all data, consider for results
                if curr_result['scores']['n_noise']/len(curr_result['scores']['labels']) <= 0.05:
                    candidate_without_noise.append(curr_result)
                if curr_num_cl in n_clusters_majority:
                    n_clusters_majority[curr_num_cl] += 1
                else:
                    n_clusters_majority[curr_num_cl] = 1

            sorted_dic = sorted(n_clusters_majority.items(), key=lambda item: (-item[1], -item[0]))
            proper_num_clusters = sorted_dic[0][0]

            print(f"For method {method}, the majority number of clusters is {proper_num_clusters}")

            final_candidate = None

            for candidate in candidate_without_noise:
                if candidate['scores']['n_clusters'] == proper_num_clusters:
                    final_candidate = candidate
                    break

            if final_candidate:
                final_candidates.append(final_candidate)
                print(f"FINAL SELECTION:\n{final_candidate}")
            else:
                print("NO CANDIDATE FOUND")

    return final_candidates

def reduce_and_cluster(df, categories, rating_names,
                       decade, gender, current_dir, folder_name):

    # Preprocess the data (rescaling)
    # Categories are exploded and scaled according to CLR (Centered log ratio)
    # Ratings are scaled using the StandardScaler
    X, feature_names = preprocess_data(df, categories, rating_names)

    dimens_methods_curated = ['pca']
    dimens_methods_curated_visualization = ['tsne', 'umap', 'lle']
    dimens_methods_all = ['pca', 'tsne', 'umap', 'lle', 'mds']

    #######
    ## SECTION THAT EXAMINES CURATED CHOICE
    #######

    # a) Use PCA to get 90% variance (pca_tev), cluster based on those dimensions
    # b) Label that data to original dimensions
    # c) Do all dimens red (mainly UMAP, TSNE, LLE) to 2D and visualize with said labels

    # Based on pca 90% variance, perform all possible clustering techniques
    results_curated = perform_curated_choice(X, feature_names, 0.90,
                                                  decade, gender, current_dir, folder_name)
    # Get min max scores on all 4 indices
    results_curated = min_max_all_indices(results_curated)

    sorted_res_curated = sorted(results_curated, key=lambda x: x['final_score'], reverse=True)

    for r in sorted_res_curated:
        print(r)

    final_candidates_curated = select_final_candidates(sorted_res_curated, dimens_methods_curated)

    fig, axs = plt.subplots(len(dimens_methods_curated_visualization), 1, figsize=(30, 40))

    for method_idx, method in enumerate(dimens_methods_curated_visualization):
        print(f"\nApplying {method.upper()} dimensionality reduction...")

        reducer, X_reduced = apply_dimensionality_reduction(X, method=method,
                                                            tsne_perplexity=90, umap_n_neighbors=15,
                                                            umap_min_dist=0.0)

        plot_clusters(
            X_reduced,
            final_candidates_curated[0]['scores']['labels'],
            f"{method.upper()}, curated PCA 90% explained variance",
            ax=axs[method_idx]
        )

    file_name = f'{decade}_{gender}_2D_first_curated_pca_then_reduced.png'
    file_path_2D_first_curated_pca_then_reduced = os.path.join(current_dir, folder_name, file_name)
    plt.savefig(file_path_2D_first_curated_pca_then_reduced, bbox_inches='tight')

    #######
    ## SECTION THAT EXAMINES ALL PERMUTATIONS IN 2D ONLY
    #######

    # Perform all possible clustering techniques, on all possbile dimens reduction techniques
    results_all = perform_all_clustering_analysis(X, decade, gender,
                                                  current_dir, folder_name)

    results_all = min_max_all_indices(results_all)

    sorted_res_all = sorted(results_all, key=lambda x: x['final_score'], reverse=True)

    final_candidates_all = select_final_candidates(sorted_res_all, dimens_methods_all)


