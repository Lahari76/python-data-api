# Python Data Processing REST API

A production-style REST API built with **Python, FastAPI, PostgreSQL, Pandas, SQLAlchemy, and Docker** for ingesting, validating, processing, storing, retrieving, and analyzing structured sales data.

## Features

- RESTful API built with FastAPI
- PostgreSQL persistent data storage
- SQLAlchemy ORM for database operations
- Pydantic request and response validation
- Pandas-based batch data cleaning and transformation
- Single and batch sales-record ingestion
- Pagination for record retrieval
- Sales analytics and category-wise revenue aggregation
- Structured API, service, schema, model, and database layers
- Exception handling with appropriate HTTP responses
- Dockerized FastAPI and PostgreSQL services
- Automated API validation tests using Pytest
- Interactive Swagger API documentation

## Tech Stack

- Python 3.9
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pandas
- Pydantic
- Docker
- Docker Compose
- Pytest
- HTTPX
- Uvicorn

## Architecture

```text
Client
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
  +----> Pandas Data Processing
  |
  v
SQLAlchemy ORM
  |
  v
PostgreSQL
