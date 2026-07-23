# Django Contact Management System

## Project Overview & Architecture
This is a production-ready Contact Management System built with Django and Django REST Framework. It allows users to manage their contacts while seamlessly integrating with external weather APIs to display current weather conditions based on each contact's city.

**Architecture Highlights:**
- **Backend**: Django 4.2+ processing HTTP requests and handling the business logic.
- **API**: Django REST Framework providing a RESTful JSON API.
- **Database**: SQLite (default) for local data storage.
- **Frontend**: Django templates styled with Bootstrap 5 and Bootstrap Icons for a responsive, modern UI.
- **Caching**: Django Local Memory Cache minimizes the number of outgoing requests to third-party APIs.
- **Deployment**: Configured for both standard Virtual Environment and Docker/Docker Compose.

## Feature List
- **Contact Management (CRUD)**: Create, Read, Update, and Delete contacts with validation.
- **Weather API Integration**: Automatically fetches and displays real-time temperature and windspeed for each contact's city using OpenStreetMap Nominatim Geocoding and Open-Meteo APIs.
- **Caching**: Weather data is cached for 45 minutes to prevent hitting API rate limits and ensure fast page loads.
- **CSV Import**: Easily import large sets of contacts using a CSV file upload modal.
- **RESTful Endpoints (DRF)**: Full API access to manage contacts programmatically.
- **Docker Ready**: Fully containerized using `python:3.11-slim` and `docker-compose` for rapid local deployment.

## Installation and Execution Guide

### Option 1: Standard Virtual Environment (Local)

1. **Clone the repository** (if applicable) and navigate to the project directory:
   ```bash
   cd contacts_project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **(Optional) Create a superuser to access the Django Admin:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Open `http://localhost:8000/` in your browser.

### Option 2: Docker & Docker Compose

1. **Ensure you have Docker and Docker Compose installed.**
2. **Navigate to the project root.**
3. **Build and start the container:**
   ```bash
   docker-compose up --build
   ```
4. **Access the application:**
   Open `http://localhost:8000/` in your browser.

*Note: Migrations are applied manually inside the container if needed by running:*
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints
The REST API is available at `/api/contacts/`.
- `GET /api/contacts/` — List all contacts
- `POST /api/contacts/` — Create new contact
- `PUT /api/contacts/{id}/` — Update contact
- `DELETE /api/contacts/{id}/` — Delete contact
