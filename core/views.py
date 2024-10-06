from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .services import CSVUploadService, GameDataQueryService
import logging

logger = logging.getLogger(__name__)

def index(request):
    data = [] 
    if request.method == 'POST':
        csv_url = request.POST.get('url')
        if csv_url:
            try:
                csv_service = CSVUploadService(csv_url)
                csv_service.upload_csv()
                return render(request, 'core/index.html', {'message': 'File processed successfully.'})
            except Exception as e:
                logger.error(f"Error processing CSV: {e}")
                return render(request, 'core/index.html', {'error': str(e)})

    elif request.method == 'GET':
        search_params = {
            'name': request.GET.get('name'),
            'developer': request.GET.get('developer'),
            'publisher': request.GET.get('publisher'),
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
            'release_after': request.GET.get('release_after'),
            'release_before': request.GET.get('release_before'),
            'required_age': request.GET.get('required_age'),
            'min_positive_reviews': request.GET.get('min_positive_reviews'),
            'max_negative_reviews': request.GET.get('max_negative_reviews'),
            'supported_languages': request.GET.get('supported_languages'),
            'tags': request.GET.get('tags'),
            'categories': request.GET.get('categories'),
            'genres': request.GET.get('genres')
        }
        game_data_service = GameDataQueryService()
        try:
            data = game_data_service.query_data(search_params)
        except Exception as e:
            logger.error(f"Error querying data: {e}")

    return render(request, 'core/index.html', {'data': data})

class CSVUploadView(APIView):
    def post(self, request):
        logger.info("Request to process data received!")
        csv_url = request.data.get('url')
        if csv_url:
            try:
                csv_service = CSVUploadService(csv_url)
                csv_service.upload_csv()
                return JsonResponse({"message": "File processed successfully."}, status=201)
            except Exception as e:
                logger.error(f"Error processing CSV: {e}")
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "No URL provided."}, status=400)

class QueryDataView(APIView):
    def get(self, request):
        search_params = {
            'name': request.GET.get('name'),
            'developer': request.GET.get('developer'),
            'publisher': request.GET.get('publisher'),
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
            'release_after': request.GET.get('release_after'),
            'release_before': request.GET.get('release_before'),
            'required_age': request.GET.get('required_age'),
            'min_positive_reviews': request.GET.get('min_positive_reviews'),
            'max_negative_reviews': request.GET.get('max_negative_reviews'),
            'supported_languages': request.GET.get('supported_languages'),
            'tags': request.GET.get('tags'),
            'categories': request.GET.get('categories'),
            'genres': request.GET.get('genres')
        }

        try:
            game_data_service = GameDataQueryService()
            query_results = game_data_service.query_data(search_params)
            return JsonResponse({"data": query_results}, safe=False, status=200)
        except Exception as e:
            logger.error(f"Error querying data: {e}")
            return JsonResponse({"error": str(e)}, status=400)
