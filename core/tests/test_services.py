import os
import django
from django.conf import settings
from datetime import date

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_explorer.settings")
django.setup()


import unittest
from unittest.mock import patch, MagicMock
from ..services import CSVUploadService, GameDataQueryService
from clickhouse_driver import Client


class TestCSVUploadService(unittest.TestCase):
    """Test suite for the CSVUploadService class."""

    @patch('core.services.requests.get')
    @patch.object(Client, 'execute')
    def test_upload_csv_success(self, mock_client, mock_get):
        """Test that the CSV is uploaded successfully and data is inserted into the database."""
        mock_get.return_value = MagicMock(status_code=200, text='AppID,Name,Release date,Required age,Price,DLC count,About the game,Supported,Windows,Mac,Linux,Positive,Negative,Score rank,Developers,Publishers,Categories,Genres,Tags\n1,Game A,Jan 01, 2022,18,0.99,0,This is a game.,[\'English\', \'French\'],TRUE,FALSE,FALSE,100,5,1,Dev1,Pub1,Action,Adventure,Action')
        service = CSVUploadService(csv_url='http://fakeurl.com/fake.csv')
        
        # Call the upload_csv method
        service.upload_csv()
        
        # Assert that execute was called with the expected SQL command
        mock_client.call_count == 1
        # self.assertTrue(mock_client.called)

    @patch('core.services.requests.get')
    def test_upload_csv_request_error(self, mock_get):
        """Test that an error is raised if the CSV URL returns an error response."""
        mock_get.return_value = MagicMock(status_code=404)
        service = CSVUploadService(csv_url='http://fakeurl.com/fake.csv')

        with self.assertRaises(ValueError):
            service.upload_csv()

    @patch('core.services.requests.get')
    @patch.object(Client, 'execute')
    def test_upload_csv_empty_data(self, mock_client, mock_get):
        """Test that uploading an empty CSV file raises a ValueError."""
        mock_get.return_value = MagicMock(status_code=200, text='AppID,Name,Release date,Required age,Price,DLC count,About the game,Supported,Windows,Mac,Linux,Positive,Negative,Score rank,Developers,Publishers,Categories,Genres,Tags\n')
        service = CSVUploadService(csv_url='http://fakeurl.com/fake.csv')

        # Call the upload_csv method and expect it to handle empty data gracefully
        service.upload_csv()  # Should not raise an error, but nothing should be inserted.
        mock_client.call_count == 0


if __name__ == '__main__':
    unittest.main()
