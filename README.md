# Game Data Explorer

This project is a game data explorer for a game analytics company. It provides a RESTful API for uploading and for querying game data, which is stored in a ClickHouse database. The data explorer supports CSV uploads via a public URL and allows users to query the game data based on various parameters like name, developer, etc.

This URL can be referred for sample csv data format [HERE](https://docs.google.com/spreadsheets/d/e/2PACX-1vSCtraqtnsdYd4FgEfqKsHMR2kiwqX1H9uewvAbuqBmOMSZqTAkSEXwPxWK_8uYQap5omtMrUF1UJAY/pub?gid=1439814054&single=true&output=csv)

## Problem Statement
- Provide an API to upload CSV data and store it.
- Provide an API to query the stored data with various filters.
- Create a Docker image for the project, which can be deployed on any cloud provider.

### Key Features
1. **Upload CSV Data**: Uploads a CSV file from a URL and stores the data in a ClickHouse database.
2. **Query Game Data**: Supports multiple filters for querying game data like developer, price range, release date, etc. This feature can be expanded to support more complex queries as well.
3. **Minimal UI**: Simple form-based UI to upload CSVs and query game data.

## Live Demo
The project is hosted on DigitalOcean: [Game Data Explorer](http://139.59.59.184/api/)

### Endpoints
1. **Upload CSV API (POST)**: `/api/upload/`
    - Accepts a CSV file URL and stores it in the ClickHouse database.
    - Sample Request:
    ```bash
    curl -X POST http://139.59.59.184/api/upload_csv/ -d "url=https://sample-csv-link.csv"
    ```
    - Response:
    ```json
    {
      "message": "File processed successfully."
    }
    ```
   
2. **Query Data API (GET)**: `/api/query_data/`
    - Query the game data with multiple filters.
    - Sample Request:
    ```bash
    curl http://139.59.59.184/api/query_data/?name=Cyberpunk&developer=CD%20Projekt&min_price=20
    ```
    - Response:
    ```json
    {
      "data": [
        {
          "app_id": 12345,
          "name": "Cyberpunk 2077",
          "developer": "CD Projekt",
          "price": 59.99,
          ...
        }
      ]
    }
    ```

---

## Running the Project Locally

### Prerequisites
- Python 3.9+
- Docker
- Docker Compose
- Git

### Step-by-Step Guide

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sajal-1999/data_explorer.git
   cd data_explorer

2. **Install Python**
    Download and install Python from [here](https://www.python.org/downloads/). Make sure you have version 3.9+.

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt

4. **Install Docker**
    Install Docker Desktop App from [here](https://www.docker.com/products/docker-desktop/) and allow it to update the PATH as well when prompted.

5. **Run the Project Using Docker**: Build and run the project using Docker:
   ```bash
   docker-compose up --build -d
   ```

6. **Access the Application**:
   The API will be available at http://localhost:8000/api/
   Open http://localhost:8000/api to access the web UI for CSV upload and data queries.

---

## Deployment on DigitalOcean (Using Docker)

### Prerequisites
- A DigitalOcean account 
- Docker and Docker Compose installed on your DigitalOcean droplet.

### Step-by-Step Guide for DigitalOcean Deployment

1. **Create a Droplet**:
   - Log in to your DigitalOcean account.
   - Create a new Droplet with Ubuntu as the operating system.
   - Set the size to a basic plan (e.g., 1GB RAM).

2. **Connect to the Droplet**: 
    Once the Droplet is created, connect via SSH:
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Update and Install Dependencies**: 
    Update the packages and install Docker:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install docker.io docker-compose -y
   ```

4. **Clone the Repository**: 
    Clone the repository to your Droplet:
   ```bash
   git clone https://github.com/sajal-1999/data_explorer.git
   cd data_explorer
   ```

5. **Build and Run the Docker Containers**: 
    Run the following command to start the Docker containers:
   ```bash
   docker-compose up --build -d
   ```

6. **Set Up Nginx**: 
    To make the app publicly available, configure Nginx as a reverse proxy.
   ```bash
   sudo apt install nginx
   sudo nano /etc/nginx/sites-available/data_explorer
   ```

7. **Add the following content to the file**:
   ```nginx
   server {
       listen 80;
       server_name <your_droplet_ip>;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Enable the site and restart Nginx**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/data_explorer /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

---

## Assumptions:
- The csv headers will be the SAME as given in the sample csv file.
- If any particular row has any data violations - (Example Release Date as May 20) - That particular row will not be inserted into the database. 
- This will be a read heavy system rather than a write heavy system. 

## API Documentation

### Upload CSV API

- **Method**: POST
- **URL**: /api/upload/
- **Parameters**:
  - url: The publicly accessible URL of the CSV file to be uploaded.
- **Response**:
  - **Success**: `{"message": "File processed successfully."}`
  - **Failure**: `{"error": "Error message."}`

### Query Game Data API

- **Method**: GET
- **URL**: /api/query/
- **Parameters**:
  - name: Game name (substring match)
  - developer: Developer name (substring match)
  - publisher: Publisher name (substring match)
  - min_price: Minimum price
  - max_price: Maximum price
  - release_after: Release date after
  - release_before: Release date before
  - required_age: Required age
  - min_positive_reviews: Minimum positive reviews
  - max_negative_reviews: Maximum negative reviews
  - supported_languages: Supported languages (comma-separated or matching)
  - tags: Tags (comma-separated or matching)
  - categories: Categories (comma-separated or matching)
  - genres: Genres (comma-separated or matching)
- **Response**:
  - **Success**: List of matching game data.
  - **Failure**: `{"error": "Error message."}`

## Future Optimisations
1. Adding basic auth
2. Fixing & Prettifying UI
3. Writing integration tests for end to end testing
4. Async uploads
