# TheSocialNetwork

This is a Django REST Framework project implementing user authentication, friend request functionality, and custom throttling for certain endpoints.

## Postman Collection

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/12298080-d0fb1fc3-e8a6-4e03-8970-e9ad198a877c?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D12298080-d0fb1fc3-e8a6-4e03-8970-e9ad198a877c%26entityType%3Dcollection%26workspaceId%3Db9068140-f88f-4d60-8b6c-3b1e4ac1a037)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- pip

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/PSNAppz/TheSocialNetwork.git
    cd TheSocialNetwork
    ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

5. **Start the Development Server**

    ```bash
    python manage.py runserver
    ```

6. **Access the API**

    The API will be available at `http://localhost:8000`.

## Running with Docker (Optional)

If you prefer running the application in a Docker container, follow these steps:

1. **Build and Run with Docker Compose**

    ```bash
    docker-compose up --build
    ```

2. **Access the Application**

    The application will be accessible at `http://localhost:8000`.

## Built With

- Django
- Django REST Framework

## Database

- Sqlite (default)
- Postgres Config added (settings.py)

## Authors

- PS Narayanan
