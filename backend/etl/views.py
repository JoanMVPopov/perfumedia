import ast
import base64
import json
import os

import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Perfume
from .serializer import ProductSerializer

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
class PFModelSimilarity(APIView):
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

