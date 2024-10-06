from django.http import JsonResponse
from rest_framework.views import APIView
from .services import CSVUploadService
from .services import GameDataQueryService
import logging

logger = logging.getLogger(__name__)

class CSVUploadView(APIView):
    def post(self, request):
        logger.info("Request to process data received!")
        csv_url = request.data.get('url')  # Get the URL from the request data
        if csv_url:
            # Process the CSV file from the provided URL
            try:
                csv_service = CSVUploadService(csv_url)  # Pass the URL to your service        
                csv_service.upload_csv()  # Use the upload_csv method
                return JsonResponse({"message": "File processed successfully."}, status=201)
            except Exception as e:
                logger.error(f"Error processing CSV: {e}")
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "No URL provided."}, status=400)

class QueryDataView(APIView):
    """
    View to handle querying the data from ClickHouse based on search parameters.
    """
    def get(self, request):
        # Extract query parameters from the request
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
            # Query the data using the service
            game_data_service = GameDataQueryService()  # Service does not need CSV URL for querying
            query_results = game_data_service.query_data(search_params)

            # Return the query results as JSON
            return JsonResponse({"data": query_results}, safe=False, status=200)
        except Exception as e:
            logger.error(f"Error querying data: {e}")
            return JsonResponse({"error": str(e)}, status=400)