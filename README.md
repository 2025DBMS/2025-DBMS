# 🛠️ House Rental Search Platform

A modern, user-friendly house rental search platform inspired by 591, designed for efficient property discovery with natural query processing and hybrid search capabilities. Built with Flask and PostgreSQL, the platform features a responsive UI, vector-based similarity search, and app-level caching.

## 🚀 Overview

This project provides a comprehensive frontend for house rental search, supporting both traditional and smart (NLP/image-based) search modes. Users can filter listings by `location`, `price`, `area`, `facilities`, and `rental rules`, or leverage natural language and image similarity for more intuitive discovery.

## 🏠 Features

- **Keyword SearchBox & Filtering SideBar**: Mathcing with listing title, then filter by city, district, price, area, facilities, and rental rules
- **Smart Search Mode**: Use natural language as query and image-based search with hybrid similarity scoring
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Image Galleries**: Multiple property images with carousel view
- **Vector Search Ready**: Integration with pgvector for similarity search
- **Pagination**: Efficient listing navigation
- **Caching**: Redis/in-memory caching for improve filtering performance

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 13+ with pgvector extension (backend handled separately)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd 2025-DBMS
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Edit `.env` and configure your environment variables as needed.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```


### 4. Run the Application
```bash
python main.py
```
The application will be available at `http://localhost:5000`

## 🏗️ Project Structure

- `main.py` — Application entry point
- `app.py` — Flask app configuration and initialization
- `cache.py` — Caching configuration (Redis/SimpleCache)
- `models.py` — SQLAlchemy ORM models
- `routes.py` — API and page routes (search, filtering, smart search)
- `static/` — Static assets (CSS, JS)
  - `css/style.css` — Custom styles
  - `js/main.js` — Frontend logic (search, filters, API integration)
- `templates/` — HTML templates
  - `index.html` — Main search page
  - `listing_detail.html` — Property detail page
- `requirements.txt` — Python dependencies

## ⚙️ Basic Functionalities & File Locations

### Backend Logic
- **Search & Filtering**: `routes.py` — Main listings endpoint with comprehensive filtering
- **Smart Search (NLP/Image)**: `routes.py` — Endpoints for NLP query parsing and image embedding
- **Database Models**: `models.py` — Property, facilities, rules, and image models
- **Caching**: `cache.py` — Redis/SimpleCache setup and usage

### Frontend Logic
- **Search Interface**: `templates/index.html` — Search form, filters, smart search UI
- **Listing Display**: `static/js/main.js` — Dynamic listing card generation
- **Filter Management**: `static/js/main.js` — Filter application and clearing
- **API Integration**: `static/js/main.js` — Dropdown population, search execution
- **Image Gallery**: `templates/listing_detail.html` — Bootstrap carousel for property images

### API Endpoints
- `GET /` — Main search interface
- `GET /listings` — Paginated listings with filters and smart search support
- `GET /listing/<id>` — Detailed property view
- `GET /api/cities` — Available cities for dropdown
- `GET /api/districts/<city>` — Districts for selected city
- `GET /api/building_types` — Available building types
- `GET /api/layouts` — Available property layouts
- `POST /api/parse_nlp_query` — NLP query parsing for smart search
- `POST /api/upload_reference_image` — Reference image upload and embedding

## 🧠 Smart Search Implementation Plan

- **NLP Query Processing**: Extracts structured filters and generates text embeddings from user queries
- **Image Processing**: Generates image embeddings for similarity search
- **Hybrid Search**: Combines structured filters with aggregated similarity scores for most relevant results

`final_score = α * text_score + (1 - α) * max(image_score)`  
Where `α` can be tunable, and the displayed results are also cut by a tunable `threshold`.
> We store `listing_embedding` and `image_embedding` as `VECTOR(512)` using pgvector.

---

For backend/database setup, please refer to the backend's documentation. This readme focuses on the frontend and API integration for a seamless development.