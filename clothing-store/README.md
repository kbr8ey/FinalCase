# Clothing Store

A Python-based clothing store application.

## Project Structure

```
clothing-store/
├─ src/              # Source code
├─ assets/
│  └─ images/        # Image assets
├─ tests/            # Test files
├─ requirements.txt  # Python dependencies
├─ Dockerfile        # Docker configuration
├─ .env.example      # Environment variables template
└─ README.md         # This file
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```

3. Run the application:
   ```bash
   python -m src.main
   ```

## Docker

Build and run with Docker:
```bash
docker build -t clothing-store .
docker run clothing-store
```
