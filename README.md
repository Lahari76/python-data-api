# Python Data Processing REST API

A containerized REST API built with **Python, FastAPI, PostgreSQL, Pandas, SQLAlchemy, and Docker** for ingesting, validating, processing, storing, retrieving, and analyzing structured sales data.

## Features

- RESTful API development using FastAPI
- PostgreSQL persistent data storage
- SQLAlchemy ORM for database operations
- Pydantic request validation
- Pandas-based batch data cleaning and transformation
- Single-record and batch data ingestion
- Paginated record retrieval
- Sales analytics and category-wise revenue summary
- Structured API, service, schema, model, and database layers
- Exception handling with meaningful HTTP responses
- Dockerized FastAPI and PostgreSQL services
- Automated API validation tests using Pytest
- Interactive Swagger API documentation

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pandas | Batch data cleaning and transformation |
| Pydantic | Request and data validation |
| Uvicorn | ASGI application server |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Pytest | Automated testing |

## Project Structure

```text
python-data-api/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── record.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── record.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_api.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Architecture

The application follows a layered structure to separate API handling, business logic, validation, and database operations.

```text
Client Request
      |
      v
FastAPI Routes
      |
      v
Pydantic Validation
      |
      v
Service Layer
      |
      +------> Pandas Processing
      |
      v
SQLAlchemy ORM
      |
      v
PostgreSQL Database
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns basic API information |
| GET | `/health` | Checks API health |
| POST | `/records` | Creates a single sales record |
| POST | `/records/batch` | Processes and creates multiple sales records |
| GET | `/records` | Retrieves sales records with pagination |
| GET | `/records/{record_id}` | Retrieves a specific record by ID |
| GET | `/analytics/summary` | Returns sales analytics summary |

## Create a Sales Record

### Request

```http
POST /records
```

Example request body:

```json
{
  "product_name": "Laptop",
  "category": "Electronics",
  "quantity": 2,
  "unit_price": 55000,
  "customer_name": "Aduri Lahari",
  "region": "South"
}
```

### Response

The API stores the record in PostgreSQL and calculates the total amount.

Example response:

```json
{
  "product_name": "Laptop",
  "category": "Electronics",
  "quantity": 2,
  "unit_price": 55000.0,
  "customer_name": "Aduri Lahari",
  "region": "South",
  "id": 1,
  "created_at": "2026-09-02T10:00:00",
  "total_amount": 110000.0
}
```

## Batch Data Processing

Multiple sales records can be submitted through:

```http
POST /records/batch
```

The batch-processing service uses **Pandas** to clean and transform incoming data before it is persisted in PostgreSQL.

Processing includes:

- Trimming leading and trailing whitespace
- Standardizing category names
- Standardizing region names
- Detecting empty text fields after trimming
- Converting processed records into database entities
- Persisting the processed batch in PostgreSQL

Example input:

```json
[
  {
    "product_name": "  Smartphone  ",
    "category": "electronics",
    "quantity": 3,
    "unit_price": 30000,
    "customer_name": "  Ravi Kumar  ",
    "region": "south"
  },
  {
    "product_name": "Office Chair",
    "category": "furniture",
    "quantity": 2,
    "unit_price": 7500,
    "customer_name": "Priya Reddy",
    "region": "west"
  }
]
```

Example processed values:

```json
[
  {
    "product_name": "Smartphone",
    "category": "Electronics",
    "customer_name": "Ravi Kumar",
    "region": "South"
  },
  {
    "product_name": "Office Chair",
    "category": "Furniture",
    "customer_name": "Priya Reddy",
    "region": "West"
  }
]
```

## Pagination

The records endpoint supports pagination using `skip` and `limit`.

Example:

```http
GET /records?skip=0&limit=10
```

Validation rules:

- `skip` must be `0` or greater
- `limit` must be between `1` and `500`

## Sales Analytics

The analytics endpoint is:

```http
GET /analytics/summary
```

It calculates:

- Total number of sales records
- Total quantity sold
- Total revenue
- Average order value
- Revenue grouped by category

Example response:

```json
{
  "total_records": 3,
  "total_quantity": 7,
  "total_revenue": 215000.0,
  "average_order_value": 71666.67,
  "revenue_by_category": {
    "Electronics": 200000.0,
    "Furniture": 15000.0
  }
}
```

The analytics calculations are performed using **Pandas**.

## Data Validation

Pydantic schemas validate incoming API requests.

Current validation includes:

- Product name is required
- Category is required
- Customer name is required
- Region is required
- Quantity must be greater than `0`
- Unit price must be greater than `0`
- Text fields have defined length restrictions

Invalid request data automatically receives an HTTP `422` validation response from FastAPI.

## Exception Handling

The API includes handling for common error scenarios.

Examples include:

- Invalid request data → HTTP `422`
- Empty batch request → HTTP `400`
- Whitespace-only text after batch cleaning → HTTP `400`
- Record not found → HTTP `404`
- Database operation failure → HTTP `500`

Database transactions are rolled back when SQLAlchemy database operations fail.

## PostgreSQL Persistence

Sales records are persisted in the PostgreSQL `sales_records` table using SQLAlchemy.

Stored information includes:

- Record ID
- Product name
- Category
- Quantity
- Unit price
- Customer name
- Region
- Creation timestamp

The API also exposes a calculated `total_amount` value based on:

```text
quantity × unit_price
```

## Running with Docker

### Prerequisites

Make sure the following are installed:

- Docker
- Docker Compose

### Environment Configuration

Use `.env.example` as a reference for the database configuration.

Example:

```env
DB_NAME=python_data_api
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```

Do not commit your actual `.env` file.

### Start the Application

Run:

```bash
docker compose up --build -d
```

Check the running containers:

```bash
docker compose ps
```

The FastAPI application will be available at:

```text
http://localhost:8000
```

PostgreSQL is exposed to the host on port:

```text
5434
```

### Stop the Containers

```bash
docker compose down
```

## Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Lahari76/python-data-api.git
cd python-data-api
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create the database:

```text
python_data_api
```

Configure the required database environment variables for your local PostgreSQL installation.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## Swagger API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

```text
http://localhost:8000/docs
```

Swagger UI can be used to test the API endpoints directly from the browser.

## Testing

The project includes automated tests using **Pytest** and FastAPI's `TestClient`.

Run:

```bash
pytest -q
```

The current automated test suite verifies:

- Health endpoint response
- Root endpoint response
- Invalid quantity validation
- Empty batch validation

Expected result:

```text
4 passed
```

## Example Health Check

Request:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "healthy",
  "service": "python-data-api"
}
```

## Docker Data Flow

The complete containerized flow is:

```text
Client
   |
   v
FastAPI Container
   |
   v
Validation / Service Layer
   |
   v
SQLAlchemy
   |
   v
PostgreSQL Container
```

Docker Compose manages both the FastAPI application and PostgreSQL database services.

## Key Learning Outcomes

This project demonstrates practical experience with:

- Building REST APIs using FastAPI
- Designing layered backend applications
- Validating request data using Pydantic
- Persisting structured data in PostgreSQL
- Performing database operations with SQLAlchemy
- Processing batch data using Pandas
- Implementing API error handling
- Creating analytics from persisted data
- Containerizing an API and database using Docker
- Managing multiple containers using Docker Compose
- Writing automated API validation tests using Pytest
- Using Git and GitHub for version control
