# URL Shortener API

A simple Django-based API to shorten URLs.

## Features

*   Shorten long URLs.
*   Redirect to the original URL using the short code.
*   Track the number of clicks for each short URL.
*   View statistics for each short URL.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10.4
*   Django 5
*   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <url-shortner-api>
    cd url_shortner_api
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install requirements.txt
    ```
    *(Note: It is recommended to have a `requirements.txt` file for production environments.)*

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

### 1. Shorten a URL

*   **URL:** `/api/shorten`
*   **Method:** `POST`
*   **Body:**
    ```json
    {
        "url": "https://www.example.com/a-very-long-url-to-shorten"
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
        "short_code": "abcdef",
        "short_url": "http://127.0.0.1:8000/abcdef"
    }
    ```
*   **Error Response (400 Bad Request):**
    ```json
    {
        "error": "Invalid JSON"
    }
    ```
    or
    ```json
    {
        "error": "{\"url\": [{\"message\": \"Enter a valid URL.\", \"code\": \"invalid\"}]}"
    }
    ```

### 2. Redirect to Original URL

*   **URL:** `/<short_code>`
*   **Method:** `GET`
*   **Description:** Redirects to the original URL associated with the `short_code`. This also increments the click counter for the URL.

### 3. Get URL Statistics

*   **URL:** `/api/stats/<short_code>`
*   **Method:** `GET`
*   **Success Response (200 OK):**
    ```json
    {
        "url": "https://www.example.com/a-very-long-url-to-shorten",
        "clicks": 15,
        "created_at": "2025-07-25T10:30:00Z"
    }
    ```
*   **Error Response (404 Not Found):**
    If the `short_code` does not exist.

## Example Usage

Using `curl`:

**1. Shorten a URL:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}' http://127.0.0.1:8000/api/shorten
```

**2. Visit the short URL (in a browser or with curl):**
```bash
curl -L http://127.0.0.1:8000/xxxxxx # Replace xxxxxx with the actual short_code
```

**3. Get stats for the URL:**
```bash
curl http://127.0.0.1:8000/api/stats/xxxxxx # Replace xxxxxx with the actual short_code
```
