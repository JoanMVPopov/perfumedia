import ast
import base64
import gc
import json
import os
import sys
import tracemalloc
from pathlib import Path

import pandas as pd
import torch
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from sentence_transformers import CrossEncoder
from torch.ao.quantization import quantize_dynamic

from .models import Product, Perfume
from .serializer import ProductSerializer
from .utils.ModelSingleton import Model
from .utils.generateDescriptionsFallback import generateDescriptions
from .utils.manh_jac_sim import calculate_notes_jaccard, calculate_manhattan
from .utils.streamingModelSimilarity import streaming_inference_generator


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class EDADataRatings(APIView):
    def get(self, request):
        # # Parse the JSON body
        # body_data = json.loads(request.body)
        #
        # # Extract parameters
        # decade = body_data.get('decade')
        # gender = body_data.get('gender')

        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)

        if not decade or not gender:
            return Response(
                {"error": "Both 'decade' and 'gender' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            return Response({'error': 'Folder not found'},
                            status=status.HTTP_404_NOT_FOUND)

        # List image files in the folder
        image_files = []

        files_needed = [
            f"{decade}_{gender}",
            f"{decade}_{gender}_box_plots",
            f"{decade}_{gender}_qq_plots",
            f"{decade}_{gender}_violin_plots",
            f"{decade}_{gender}_pairplots"
        ]

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                split_text = os.path.splitext(filename)
                if split_text[1] != '.png':
                    continue
                filename_no_ext = split_text[0]

                if filename_no_ext in files_needed:
                    image_files.append(os.path.join(folder_path, filename))
                # split_no_ext = filename_no_ext.split('_')
                #
                # if split_no_ext[0] == decade and split_no_ext[1] == gender:
                #     image_files.append(os.path.join(folder_path, filename))

        if len(image_files) == 0:
            return Response({'error': 'No images found'},
                            status=status.HTTP_404_NOT_FOUND)

        # Convert images to Base64
        images_base64 = []
        for image_file in image_files:
            with open(image_file, "rb") as img_file:
                base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                images_base64.append({
                    "filename": os.path.basename(image_file),
                    "base64": base64_str
                })

        return Response({"images": images_base64}, status=status.HTTP_200_OK)


class EDADataRatingsProgression(APIView):
    def get(self, request):
        # # Parse the JSON body
        # body_data = json.loads(request.body)
        #
        # # Extract parameters
        # decade = body_data.get('decade')
        # gender = body_data.get('gender')

        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)

        if not decade or not gender:
            return Response(
                {"error": "Both 'decade' and 'gender' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            return Response({'error': 'Folder not found'},
                            status=status.HTTP_404_NOT_FOUND)

        # List image files in the folder
        image_files = []

        files_needed = [
            f"{decade}_{gender}_avg_rubric_progression"
        ]

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                split_text = os.path.splitext(filename)
                if split_text[1] != '.png':
                    continue
                filename_no_ext = split_text[0]

                if filename_no_ext in files_needed:
                    image_files.append(os.path.join(folder_path, filename))
                # split_no_ext = filename_no_ext.split('_')
                #
                # if split_no_ext[0] == decade and split_no_ext[1] == gender:
                #     image_files.append(os.path.join(folder_path, filename))

        if len(image_files) == 0:
            return Response({'error': 'No images found'},
                            status=status.HTTP_404_NOT_FOUND)

        # Convert images to Base64
        images_base64 = []
        for image_file in image_files:
            with open(image_file, "rb") as img_file:
                base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                images_base64.append({
                    "filename": os.path.basename(image_file),
                    "base64": base64_str
                })

        return Response({"images": images_base64}, status=status.HTTP_200_OK)

class EDADataCategoriesNotes(APIView):
    def get(self, request):
        # # Parse the JSON body
        # body_data = json.loads(request.body)
        #
        # # Extract parameters
        # decade = body_data.get('decade')
        # gender = body_data.get('gender')

        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)

        if not decade or not gender:
            return Response(
                {"error": "Both 'decade' and 'gender' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            return Response({'error': 'Folder not found'},
                            status=status.HTTP_404_NOT_FOUND)

        # List image files in the folder
        image_files = []

        files_needed = [
            f"{decade}_{gender}_avg_categories_piecharts",
            f"{decade}_{gender}_notes_histogram"
        ]

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                split_text = os.path.splitext(filename)
                if split_text[1] != '.png':
                    continue
                filename_no_ext = split_text[0]

                if filename_no_ext in files_needed:
                    image_files.append(os.path.join(folder_path, filename))
                # split_no_ext = filename_no_ext.split('_')
                #
                # if split_no_ext[0] == decade and split_no_ext[1] == gender:
                #     image_files.append(os.path.join(folder_path, filename))

        if len(image_files) == 0:
            return Response({'error': 'No images found'},
                            status=status.HTTP_404_NOT_FOUND)

        # Convert images to Base64
        images_base64 = []
        for image_file in image_files:
            with open(image_file, "rb") as img_file:
                base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                images_base64.append({
                    "filename": os.path.basename(image_file),
                    "base64": base64_str
                })

        return Response({"images": images_base64}, status=status.HTTP_200_OK)

class EDADataCorrelation(APIView):
    def get(self, request):
        # # Parse the JSON body
        # body_data = json.loads(request.body)
        #
        # # Extract parameters
        # decade = body_data.get('decade')
        # gender = body_data.get('gender')

        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)

        if not decade or not gender:
            return Response(
                {"error": "Both 'decade' and 'gender' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            return Response({'error': 'Folder not found'},
                            status=status.HTTP_404_NOT_FOUND)

        # List image files in the folder
        image_files = []

        files_needed = [
            f"{decade}_{gender}_categories_rubrics_correlation",
            f"{decade}_{gender}_notes_categories_correlation",
            f"{decade}_{gender}_notes_rubrics_correlation"
        ]

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                split_text = os.path.splitext(filename)
                if split_text[1] != '.png':
                    continue
                filename_no_ext = split_text[0]

                if filename_no_ext in files_needed:
                    image_files.append(os.path.join(folder_path, filename))
                # split_no_ext = filename_no_ext.split('_')
                #
                # if split_no_ext[0] == decade and split_no_ext[1] == gender:
                #     image_files.append(os.path.join(folder_path, filename))

        if len(image_files) == 0:
            return Response({'error': 'No images found'},
                            status=status.HTTP_404_NOT_FOUND)

        # Convert images to Base64
        images_base64 = []
        for image_file in image_files:
            with open(image_file, "rb") as img_file:
                base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                images_base64.append({
                    "filename": os.path.basename(image_file),
                    "base64": base64_str
                })

        return Response({"images": images_base64}, status=status.HTTP_200_OK)


class EDADataBrands(APIView):
    def get(self, request):
        # # Parse the JSON body
        # body_data = json.loads(request.body)
        #
        # # Extract parameters
        # decade = body_data.get('decade')
        # gender = body_data.get('gender')

        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)

        if not decade or not gender:
            return Response(
                {"error": "Both 'decade' and 'gender' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            return Response({'error': 'Folder not found'},
                            status=status.HTTP_404_NOT_FOUND)

        # List image files in the folder
        image_files = []

        files_needed = [
            f"{decade}_{gender}_brands_stats"
        ]

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                split_text = os.path.splitext(filename)
                if split_text[1] != '.png':
                    continue
                filename_no_ext = split_text[0]

                if filename_no_ext in files_needed:
                    image_files.append(os.path.join(folder_path, filename))
                # split_no_ext = filename_no_ext.split('_')
                #
                # if split_no_ext[0] == decade and split_no_ext[1] == gender:
                #     image_files.append(os.path.join(folder_path, filename))

        if len(image_files) == 0:
            return Response({'error': 'No images found'},
                            status=status.HTTP_404_NOT_FOUND)

        # Convert images to Base64
        images_base64 = []
        for image_file in image_files:
            with open(image_file, "rb") as img_file:
                base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                images_base64.append({
                    "filename": os.path.basename(image_file),
                    "base64": base64_str
                })

        return Response({"images": images_base64}, status=status.HTTP_200_OK)

class PFNotes(APIView):
    def get(self, request):
        try:
            queryset = Perfume.objects.all().values()
            df = pd.DataFrame.from_records(queryset)
            # Convert the 'notes' column (if stored as a string representation of a list)
            #df['notes'] = df['notes'].apply(lambda x: ast.literal_eval(x))
            # To get a set of all unique notes:
            # Explode the 'notes' column (flatten lists)
            exploded_notes = df['notes'].explode()

            # Drop any NaNs introduced by explode
            exploded_notes = exploded_notes.dropna()

            # Now get unique notes from the cleaned series
            unique_notes = exploded_notes.unique().tolist()

            #print(unique_notes)

            return Response({'notes': unique_notes}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':"Could not retrieve notes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PFPieItems(APIView):
    def get(self, request):
        try:
            queryset = Perfume.objects.all().values()
            df = pd.DataFrame.from_records(queryset)

            categories = ['type', 'style', 'season', 'occasion']

            exploded_categories = []

            for outer_index, category in enumerate(categories):
                unique_subcategories = []

                for index, category_row in enumerate(df[category]):
                    for index_cat, category_curr_name in enumerate(category_row):
                       if category_curr_name not in unique_subcategories:
                           unique_subcategories.append(category_curr_name)

                exploded_categories.append(unique_subcategories)

            return Response({'piechart_items': exploded_categories}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': "Could not retrieve piechart items"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PFDefaultSimilarity(APIView):
    def post(self, request):
        try:
            body_data = json.loads(request.body)

            # Extract parameters
            notes_request = body_data.get('notes')
            categories_request = body_data.get('categories')
            w_notes_request = body_data.get('w_notes')
            w_categories_request = body_data.get('w_categories')

            queryset = Perfume.objects.all().values()
            data = pd.DataFrame.from_records(queryset).reset_index(drop=True)

            categories = ['type', 'style', 'season', 'occasion']

            exploded_categories = None

            for category in categories:
                exploded_dict = {}

                df_type = data[category]
                df_type_nums = data[f'{category}_numbers']

                for index, category_row in enumerate(df_type):
                    for index_cat, category_curr_name in enumerate(category_row):
                        if category_curr_name not in exploded_dict:
                            exploded_dict[category_curr_name] = [0] * len(df_type_nums)

                        exploded_dict[category_curr_name][index] = df_type_nums.iloc[index][index_cat]

                exploded_categories = pd.concat([exploded_categories, pd.DataFrame(exploded_dict)], axis=1)

            # encode the categories
            categories_request_encoded = []

            for col in exploded_categories.columns:
                found = False
                for segment in categories_request:
                    if col == segment['selectedItem']['name']:
                        categories_request_encoded.append(segment['percentage'])
                        found = True
                        break
                if not found:
                    categories_request_encoded.append(0)

            notes = data['notes']
            notes_dummies = notes.explode().str.get_dummies().groupby(level=0).max()

            # one-hot encode notes from request
            notes_request_onehot = [1 if col in notes_request else 0 for col in notes_dummies.columns]

            similarities = []

            for i in range(len(data)):
                notes_similarity = calculate_notes_jaccard(notes_request_onehot,
                                                           notes_dummies.iloc[i, :].tolist())
                categories_similarity = calculate_manhattan(categories_request_encoded,
                                                            exploded_categories.iloc[i, :].tolist(), 800.0)

                sim = w_notes_request * notes_similarity + w_categories_request * categories_similarity
                similarities.append({
                    "similarity": sim,
                    "link": data.iloc[i]["link"],
                    "description": data.iloc[i]["description"],
                    "image": data.iloc[i]["image"],
                    "scent": data.iloc[i]['scent'],
                    "longevity": data.iloc[i]['longevity'],
                    "sillage": data.iloc[i]['sillage'],
                    "bottle": data.iloc[i]['bottle'],
                    "value_for_money": data.iloc[i]['value_for_money']
                })

            similarities = sorted(similarities, key=lambda x: x['similarity'], reverse=True)

            # return top 20 most similar
            return Response(similarities[:20], status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': "Could not calculate similarities"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PFModelSimilarity(APIView):
    def post(self, request):
        try:
            body_data = json.loads(request.body)
            # Extract parameters
            query = body_data.get('query')

            perfumes_ordered = Perfume.objects.all().order_by('id')
            queryset = perfumes_ordered.values()
            data = pd.DataFrame.from_records(queryset).reset_index(drop=True)

            print("Loading model")
            # Load the model into memory once
            MODEL = Model()
            # MODEL = None

            print("Model initialized\n")

            if 'generated_descriptions' not in data.columns or data.at[0, 'generated_descriptions'] == "No description":
                print("Fallback activated")
                categories = ['type', 'style', 'season', 'occasion']
                ratings = ['scent', 'longevity', 'sillage', 'bottle', 'value_for_money']

                # this also updates data in-place
                generateDescriptions(data, categories, ratings)

                perfumes = list(perfumes_ordered)

                # Update each perfume instance
                for idx, perfume in enumerate(perfumes):
                    perfume.generated_descriptions = data.iloc[idx]['generated_descriptions']

                # Perform bulk update in a single query
                Perfume.objects.bulk_update(perfumes, ['generated_descriptions'])

            print("After if fallback")

            number_of_perfumes = len(perfumes_ordered)
            step = 100

            # Create a streaming generator
            generator = streaming_inference_generator(query, data, MODEL, number_of_perfumes, step)

            # Return a StreamingHttpResponse with SSE content
            response = StreamingHttpResponse(generator, content_type='text/event-stream')
            response["Cache-Control"] = "no-cache"
            response["X-Accel-Buffering"] = "no"  # Helps with Nginx proxies


            return response
        except Exception as e:
            print(e)
            return Response({'error': "Could not calculate similarities"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- NEW CLUSTERING ENDPOINTS ---

def generate_clustering_title(filename_no_ext, decade, gender, dr_method_selected=None):
    """
    Generates a more descriptive title from the filename.
    This function will need significant customization based on your exact filenames.
    """
    parts = filename_no_ext.split('_')
    base_info = f"{decade}, {gender}"

    # PCA Variance/Loadings
    if "d_bar_explained_variance" in filename_no_ext:
        dim = parts[-4][:-1]  # e.g. "2d" -> "2"
        return f"PCA Explained Variance ({dim}D) - {base_info}"
    if "d_component" in filename_no_ext and "loadings" in filename_no_ext:
        comp_num_part = [p for p in parts if p.startswith("component")]
        comp_num = comp_num_part[0].replace("component_", "") if comp_num_part else "N/A"
        dim = parts[parts.index(comp_num_part[0]) - 1][:-1] if comp_num_part else "N/A"
        return f"PCA Loadings for Component {comp_num} ({dim}D) - {base_info}"

    # Curated (PCA based) analysis
    if "curated" in filename_no_ext:
        algo = "UnknownAlgo"
        try:  # Try to extract algo
            if "all_clustering_algos" in filename_no_ext:  # Main visualization plot
                viz_method_curated = parts[parts.index("curated") - 1]
                return f"{viz_method_curated.upper()} Viz of Curated PCA Results - {base_info}"
            # Cluster detail plots
            # e.g., 1990_Feminine_violin_plots_curated_cluster0_pca_KMeans.png
            cluster_idx = filename_no_ext.find("cluster")
            cluster_num = filename_no_ext[cluster_idx + len("cluster")]
            plot_type_str = filename_no_ext.split('_curated_cluster')[0]
            plot_type = plot_type_str[len(decade) + len(gender) + 2:].replace("_", " ").title()  # e.g. Violin Plots
            algo = parts[-1]  # Last part is algo
            return f"{algo} (Curated PCA) - Cl. {cluster_num}: {plot_type} - {base_info}"
        except Exception:
            return f"Curated PCA Analysis: {filename_no_ext.replace('_', ' ')} - {base_info}"

    # Other DR (non-curated) analysis
    if dr_method_selected:  # This implies we are in the "Other DR" section
        if f"_{dr_method_selected}_2D_all_clustering_algos" in filename_no_ext:
            return f"{dr_method_selected.upper()} 2D Visualizations Overview - {base_info}"
        # Cluster detail plots
        # e.g., 1990_Feminine_violin_plots_cluster0_umap_KMeans.png
        try:
            cluster_idx = filename_no_ext.find("cluster")
            cluster_num = filename_no_ext[cluster_idx + len("cluster")]

            # Find plot type (e.g. violin_plots)
            plot_type_parts = []
            temp_parts = filename_no_ext.split(f"_cluster{cluster_num}_")[0].split('_')
            # plot_type is parts after decade and gender
            plot_type = "_".join(temp_parts[2:]).replace("_", " ").title()

            # Algo is the last part
            algo = parts[-1]
            # DR method is before algo
            dr_in_file = parts[-2]

            if dr_in_file == dr_method_selected:  # Make sure it's for the DR method we requested
                return f"{algo} ({dr_in_file.upper()}) - Cl. {cluster_num}: {plot_type} - {base_info}"
            else:  # Should not happen if filtering is correct, but good to have a fallback
                return f"DR: {dr_in_file.upper()}, Algo: {algo} - Cl. {cluster_num}: {plot_type} - {base_info}"

        except Exception:
            return f"Other DR ({dr_method_selected.upper()}) Analysis: {filename_no_ext.replace('_', ' ')} - {base_info}"

    return f"Analysis: {filename_no_ext.replace('_', ' ')} - {base_info}"  # Generic fallback


class CuratedClusteringInformation(APIView):
    def get(self, request):
        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)
        clustering_method = request.query_params.get('clustering_method', None)
        dr_method = request.query_params.get('dr_method', None)

        supported_clustering_methods = ["KMeans", "AffinityPropagation", "Agglomerative", "DBSCAN", "HDBSCAN", "GaussianMixture", "SpectralClustering"]
        supported_curated_dr_methods = ['tsne', 'umap', 'lle', 'isomap']

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")
        if not os.path.exists(folder_path):
            return Response({'error': 'Uploads folder not found'}, status=status.HTTP_404_NOT_FOUND)

        images_data = []
        prefix = f"{decade}_{gender}_"

        print(clustering_method)
        print(dr_method)

        # f'{decade}_{gender}_violin_plots_curated_cluster{label}_{curated_result_dr}_{curated_result_algo}.png'
        # f'{decade}_{gender}_avg_categories_piecharts_curated_cluster{label}_{curated_result_dr}_{curated_result_algo}.png'
        # f'{decade}_{gender}_notes_histogram_curated_cluster{label}_{curated_result_dr}_{curated_result_algo}.png'

        for filename in sorted(os.listdir(folder_path)):
            if filename.startswith(prefix) and filename.endswith(".png"):
                filename_no_ext = os.path.splitext(filename)[0]

                is_violin = "violin_plots_curated_cluster" in filename_no_ext
                is_avg_cat_pie = "avg_categories_piecharts_curated_cluster" in filename_no_ext
                is_notes_histograms = "notes_histogram_curated_cluster" in filename_no_ext

                if ((is_violin or is_avg_cat_pie or is_notes_histograms)
                        and clustering_method in filename_no_ext and dr_method in filename_no_ext):
                    file_path = os.path.join(folder_path, filename)

                    try:
                        with open(file_path, "rb") as img_file:
                            base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                            images_data.append({
                                "base64": base64_str,
                                "filename": filename  # Keep for debugging or potential future use
                            })
                    except Exception as e:
                        print(f"Error processing PCA file {filename}: {e}")

        if not images_data:
            return Response({'error': 'No images found for given curated clustering algorithm and dr method'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"images": images_data}, status=status.HTTP_200_OK)

class ClusteringPcaAnalysis(APIView):
    def get(self, request):
        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)

        # if not decade or not gender or decade == 'All' or gender == 'All':
        #     return Response(
        #         {"error": "Specific 'decade' and 'gender' (not 'All') are required for PCA analysis."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")
        if not os.path.exists(folder_path):
            return Response({'error': 'Uploads folder not found'}, status=status.HTTP_404_NOT_FOUND)

        images_data = []
        prefix = f"{decade}_{gender}_"

        for filename in sorted(os.listdir(folder_path)):
            if filename.startswith(prefix) and filename.endswith(".png"):
                filename_no_ext = os.path.splitext(filename)[0]

                is_pca_variance = "d_bar_explained_variance" in filename_no_ext
                is_pca_loadings = "d_component_" in filename_no_ext and "loadings" in filename_no_ext
                is_curated_viz = "_curated_2D_all_clustering_algos" in filename_no_ext
                # is_curated_cluster_detail = "_curated_cluster" in filename_no_ext and \
                #                             ("violin_plots" in filename_no_ext or \
                #                              "avg_categories_piecharts" in filename_no_ext or \
                #                              "notes_histogram" in filename_no_ext)

                if is_pca_variance or is_pca_loadings or is_curated_viz:
                    file_path = os.path.join(folder_path, filename)
                    try:
                        with open(file_path, "rb") as img_file:
                            base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                            images_data.append({
                                "title": generate_clustering_title(filename_no_ext, decade, gender),
                                "base64": base64_str,
                                "filename": filename  # Keep for debugging or potential future use
                            })
                    except Exception as e:
                        print(f"Error processing PCA file {filename}: {e}")

        if not images_data:
            return Response({'error': 'No PCA-based clustering images found for the selected filters.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"images": images_data}, status=status.HTTP_200_OK)


class ClusteringOtherDrAnalysis(APIView):
    def get(self, request):
        decade = request.query_params.get('decade', None)
        gender = request.query_params.get('gender', None)
        dr_method = request.query_params.get('dr_method', None)  # e.g., 'umap', 'tsne'

        # if not decade or not gender or decade == 'All' or gender == 'All' or not dr_method:
        #     return Response(
        #         {"error": "Specific 'decade', 'gender' (not 'All'), and 'dr_method' are required."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        folder_path = os.path.join(settings.MEDIA_ROOT, "uploads")
        if not os.path.exists(folder_path):
            return Response({'error': 'Uploads folder not found'}, status=status.HTTP_404_NOT_FOUND)

        images_data = []
        prefix = f"{decade}_{gender}_"

        for filename in sorted(os.listdir(folder_path)):
            if filename.startswith(prefix) and filename.endswith(".png"):
                filename_no_ext = os.path.splitext(filename)[0]

                # Ensure it's NOT a curated file (to avoid overlap with PCA section)
                if "curated" in filename_no_ext:
                    continue

                # Check if it's related to the selected dr_method
                # Main visualization: e.g. 1990_Masculine_umap_2D_all_clustering_algos.png
                is_other_dr_viz = f"_{dr_method}_2D_all_clustering_algos" in filename_no_ext

                # Cluster details: e.g. 1990_Masculine_violin_plots_cluster0_umap_KMeans.png
                is_other_dr_cluster_detail = (
                        f"_cluster" in filename_no_ext and
                        f"_{dr_method}_" in filename_no_ext and  # Check if the DR method is in the name before algo
                        (filename_no_ext.endswith(dr_method + "_" + parts[-1]) for parts in
                         [filename_no_ext.split('_')]) and  # More robust check
                        ("violin_plots" in filename_no_ext or \
                         "avg_categories_piecharts" in filename_no_ext or \
                         "notes_histogram" in filename_no_ext)
                )
                # Refined check for cluster detail (ensure dr_method is directly before algo)
                if "_cluster" in filename_no_ext and (
                        "violin_plots" in filename_no_ext or "avg_categories_piecharts" in filename_no_ext or "notes_histogram" in filename_no_ext):
                    parts_for_detail_check = filename_no_ext.split('_')
                    try:
                        # Assuming format ..._clusterX_DRMETHOD_ALGO.png
                        if len(parts_for_detail_check) > 2 and parts_for_detail_check[-2] == dr_method:
                            is_other_dr_cluster_detail = True
                        else:
                            is_other_dr_cluster_detail = False  # Reset if pattern not met
                    except IndexError:
                        is_other_dr_cluster_detail = False

                if is_other_dr_viz or is_other_dr_cluster_detail:
                    file_path = os.path.join(folder_path, filename)
                    try:
                        with open(file_path, "rb") as img_file:
                            base64_str = base64.b64encode(img_file.read()).decode('utf-8')
                            images_data.append({
                                "title": generate_clustering_title(filename_no_ext, decade, gender,
                                                                   dr_method_selected=dr_method),
                                "base64": base64_str,
                                "filename": filename
                            })
                    except Exception as e:
                        print(f"Error processing Other DR file {filename}: {e}")

        if not images_data:
            return Response({'error': f'No {dr_method.upper()} based clustering images found for selected filters.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"images": images_data}, status=status.HTTP_200_OK)