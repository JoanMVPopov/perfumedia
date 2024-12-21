import base64
import json
import os

from django.conf import settings
from django.http import HttpResponse
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializer import ProductSerializer

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class EDAData(APIView):
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

        for filename in os.listdir(folder_path):
            print(filename)
            if os.path.isfile(os.path.join(folder_path, filename)):
                split_text = os.path.splitext(filename)
                print(split_text)
                if split_text[1] != '.png':
                    continue
                filename_no_ext = split_text[0]
                print(filename_no_ext)
                split_no_ext = filename_no_ext.split('_')
                print(split_no_ext)

                if split_no_ext[0] == decade and split_no_ext[1] == gender:
                    image_files.append(os.path.join(folder_path, filename))

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
