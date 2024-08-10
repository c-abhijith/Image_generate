# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeneratedImage
from .tasks import generate_image
from .serializers import GeneratedImageSerializer

class GenerateImagesView(APIView):

    def get(self, request):
        images = GeneratedImage.objects.all()
        serializer = GeneratedImageSerializer(images, many=True, context={'request': request})
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        prompts = request.data.get('prompts', [])
        if len(prompts) < 1:
            return Response({'message': 'At least one prompt is required.'}, status=status.HTTP_400_BAD_REQUEST)

        task_ids = []
        for prompt in prompts:
            print("Starting task for prompt:", prompt)
            task = generate_image.delay(prompt)
            print("Task ID:", task.id)
            task_ids.append(task.id)

        return Response({'status': 'success', 'data': task_ids}, status=status.HTTP_202_ACCEPTED)

# class RetrieveImagesView(APIView):
#     def get(self, request, *args, **kwargs):
#         task_ids = request.query_params.getlist('task_id')
#         if not task_ids:
#             return Response({'error': 'No task IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         images = GeneratedImage.objects.filter(task_id__in=task_ids)
#         if not images:
#             return Response({'error': 'No images found for the provided task IDs.'}, status=status.HTTP_404_NOT_FOUND)
        
#         data = [{'task_id': img.task_id, 'image_url': img.image} for img in images]
#         return Response(data, status=status.HTTP_200_OK)
