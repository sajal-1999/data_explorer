import csv
import requests
from data_explorer import settings
from datetime import datetime
from .models import GameData
from clickhouse_driver import Client  
from typing import List
from io import StringIO
import logging

logger = logging.getLogger(__name__)

class CSVUploadService:
    """
    This service handles uploading and querying CSV data.
    """
    def __init__(self, csv_url):
        self.csv_url = csv_url
        self.client = Client(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )

    def upload_csv(self):
        """
        Reads the CSV and saves data into the GameData model.
        This method consolidates both CSV upload and storage logic.
        """
        try:
            response = requests.get(self.csv_url)
            response.raise_for_status()  # Raise an error for bad responses
            csv_data = StringIO(response.text)  # Use StringIO to read the CSV data
            reader = csv.DictReader(csv_data)

            rows_to_insert = []
            for row in reader:
                try:
                    rows_to_insert.append((
                        self.parse_int(row['AppID']),
                        row['Name'],
                        self.parse_date(row.get('Release date')),
                        self.parse_int(row.get('Required age')),
                        self.parse_float(row.get('Price')),
                        self.parse_int(row.get('DLC count')),
                        row.get('About the game', ''),
                        self.process_supported_languages(row.get('Supported languages', '')),
                        self.parse_bool(row.get('Windows')),
                        self.parse_bool(row.get('Mac')),
                        self.parse_bool(row.get('Linux')),
                        self.parse_int(row.get('Positive')),
                        self.parse_int(row.get('Negative')),
                        self.parse_int(row.get('Score rank')),
                        row.get('Developers', '').lower(),
                        row.get('Publishers', '').lower(),
                        row.get('Categories', '').lower(), 
                        row.get('Genres', '').lower(), 
                        row.get('Tags', '').lower() 
                    ))
                except Exception as e:
                    logger.error(f"Insertion of row - {row} failed with error: {e}")

            # Execute the insert statement
            if rows_to_insert:
                self.client.execute(
                    'INSERT INTO game_data (app_id, name, release_date, required_age, price, dlc_count, about_the_game, supported_languages, windows, mac, linux, positive_reviews, negative_reviews, score_rank, developer, publisher, categories, genres, tags) VALUES',
                    rows_to_insert
                )
        except Exception as e:
            raise ValueError(f"Error uploading CSV file: {e}")

    @staticmethod
    def parse_date(date_string: str):
        return datetime.strptime(date_string, "%b %d, %Y").date()
        
    @staticmethod
    def parse_int(value: str) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0 

    @staticmethod
    def parse_float(value: str) -> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0 

    @staticmethod
    def parse_bool(value: str) -> int:
        return 1 if value == 'TRUE' else 0 
    
    @staticmethod
    def process_supported_languages(supported_languages: str) -> str:
        # Remove leading/trailing whitespace and join languages
        supported_languages = supported_languages.replace('[','')
        supported_languages = supported_languages.replace(']','')
        supported_languages = supported_languages.replace('\'','')

        languages_list = [lang.strip() for lang in supported_languages.split(',')]
        return ','.join(languages_list).lower() 


class GameDataQueryService:
    """
    Service for querying data from ClickHouse.
    """
    def __init__(self):
        self.client = Client(
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME']
        )

    def query_data(self, search_params: dict) -> List[dict]:
        """
        Queries the GameData model based on search parameters and returns data in dictionary format.
        """
        query = "SELECT * FROM game_data WHERE 1=1"
        params = []
        logger.info("SEARCH PARAMS: ")
        logger.info(search_params)

        # Name filter (exact match or substring)
        if 'name' in search_params and search_params['name']:
            query += f" AND name ILIKE '%{search_params['name']}%'"
        
        # Developer filter
        if 'developer' in search_params and search_params['developer']:
            query += f" AND developer ILIKE '%{search_params['developer']}%'"
        
        # Publisher filter
        if 'publisher' in search_params and search_params['publisher']:
            query += f" AND publisher ILIKE '%{search_params['publisher']}%'"

        # Price filter (min and max price)
        if 'min_price' in search_params and search_params['min_price']:
            query += f" AND price >= {search_params['min_price']}"
        if 'max_price' in search_params and search_params['max_price']:
            query += f" AND price <= {search_params['max_price']}"

        # Release date filter (before/after date)
        if 'release_after' in search_params and search_params['release_after']:
            query += f" AND release_date >= '{search_params['release_after']}'"
        if 'release_before' in search_params and search_params['release_before']:
            query += f" AND release_date <= '{search_params['release_before']}'"

        # Required age filter
        if 'required_age' in search_params and search_params['required_age']:
            query += f" AND required_age >= {search_params['required_age']}"

        # Positive and negative reviews filter
        if 'min_positive_reviews' in search_params and search_params['min_positive_reviews']:
            query += f" AND positive_reviews >= {search_params['min_positive_reviews']}"
        if 'max_negative_reviews' in search_params and search_params['max_negative_reviews']:
            query += f" AND negative_reviews <= {search_params['max_negative_reviews']}"

        # Supported languages (comma-separated, match any)
        if 'supported_languages' in search_params and search_params['supported_languages']:
            languages = "','".join(search_params['supported_languages'].split(',')).lower()
            query += f" AND arrayExists(x -> x IN ('{languages}'), splitByString(',', supported_languages))"

        # Tags filter (comma-separated, match any)
        if 'tags' in search_params and search_params['tags']:
            tags = "','".join(search_params['tags'].split(',')).lower()
            query += f" AND arrayExists(x -> x IN ('{tags}'), splitByString(',', tags))"

        # Categories filter (comma-separated, match any)
        if 'categories' in search_params and search_params['categories']:
            categories = "','".join(search_params['categories'].split(',')).lower()
            query += f" AND arrayExists(x -> x IN ('{categories}'), splitByString(',', categories))"

        # Genres filter (comma-separated, match any)
        if 'genres' in search_params and search_params['genres']:
            genres = "','".join(search_params['genres'].split(',')).lower()
            query += f" AND arrayExists(x -> x IN ('{genres}'), splitByString(',', genres))"

        logger.info("Executing query: %s", query)
        results = self.client.execute(query)

        game_data_list = [GameData(*result) for result in results]
        return [game_data.to_dict() for game_data in game_data_list]

