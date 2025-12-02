# Eli's Clothing Brand: A Containerized E-Commerce Platform

##  Final Case Study

**Course:** DS 2026: Systems 1  
**Submitted by:** Eli Johnson  
**Date:** November 30, 2025

---

## 1) Executive Summary

### Problem
Small fashion retailers need a modern, scalable e-commerce platform that can:
- Showcase products online with detailed information
- Provide a smooth shopping experience
- Allow customers to manage shopping carts
- Scale easily without complex infrastructure knowledge
- Deploy consistently across different environments

### Solution
My solution is a containerized full-stack e-commerce platform combining using Flask REST API for product catalog and cart management, responsive HTML/JavaScript web application, and a single Docker container for reproducible, portable deployment. These features combined create a polished storefront allowing users to select sizes, colors, and add products to their cart with real-time updates. The website features a section dedicated to the brands mission and statement. Shortcut buttons are available to help the user move around the store quickly. 

---

## 2) System Overview

### Module Concepts / Tools Used

- Flask (REST API)
- Docker (Containerization)
- HTML/CSS/JavaScript (Frontend)
- Flask-CORS (Cross-Origin Resource Sharing)
- Logging (Python logging module)
- pytest (Testing)
- JSON (Data storage)




### Architecture Diagram

```
┌─────────────────────────────┐
│        Browser (User)       │
│  home.html + JS/CSS         │
└─────────────┬───────────────┘
              │ HTTP/CORS
              ▼
┌─────────────────────────────────────────────┐
│         Docker Container (clothing-store)   │
│ ┌─────────────────────────────────────────┐ │
│ │         Flask Web Server (8080)        │ │
│ │ ┌───────────────┬────────────────────┐ │ │
│ │ │ /home.html    │ Static Assets      │ │ │
│ │ │ /assets/...   │ (images, CSS, JS)  │ │ │
│ │ └───────────────┴────────────────────┘ │ │
│ │ ┌─────────────────────────────────────┐ │ │
│ │ │ REST API Endpoints:                 │ │ │
│ │ │   GET /products                     │ │ │
│ │ │   GET /products/<id>                │ │ │
│ │ │   POST /cart/add                    │ │ │
│ │ │   GET /health                       │ │ │
│ │ └─────────────────────────────────────┘ │ │
│ │ ┌─────────────────────────────────────┐ │ │
│ │ │ Data: src/data/products.json        │ │ │
│ │ │ Cart: In-memory (per container)     │ │ │
│ │ └─────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

![Architecture Screenshot](assets/images/Screenshot.png)

### Data Sources

| Component | Source | Format | Items |
|-----------|--------|--------|-------|
| **Products** | `src/data/products.json` | JSON | 8 |
| **Models** | `src/models.py` | Python dataclass | 1 |
| **Tests** | `tests/test_products.py` | pytest | 15+ |
| **Frontend** | `home.html` | HTML/CSS/JS | Single page |

---


## 3) How to Build & Run

### Quick Start (Recommended)

```bash
# Build Docker image
docker build -t clothing-store .

# Run container (exposes port 8080)
docker run -p 8080:8080 clothing-store

# Test health endpoint
curl http://localhost:8080/health
```

### Local Development (No Docker)

```bash
pip install -r requirements.txt
cp .env.example .env
python3 -m src.main
```

### Accessing the App

- **Web:** Visit `http://localhost:8080/home.html` in your browser
- **API:** `http://localhost:8080/products`
- **Tests:** `pytest tests/test_products.py -v`


### Start in Docker

Open Docker Desktop, build the image from the Dockerfile, and run the container mapping port 8080, make sure to specify port 8080. Then access the app at `http://localhost:8080/home.html`.


### Data
- Product data is loaded from `src/data/products.json` (edit this file to change products)

### Notes
- Cart data is stored in memory and resets when the container/app restarts
- All static assets (images, CSS, JS) are served from `/assets`

---


## 4) Design Decisions

### Why this concept?
- I wanted to use Docker because it was fresh in my memory and seemed less aggravating than alternatives.  It’s the easiest way to make sure my code works the same on any machine, and it’s perfect for class projects and demos.

### Tradebacks
- Currently, the cart data is kept in memory for now. This works while displaying a mock site but it means the cart resets if the server restarts. For a real store, I’d use a database to save cart data between sessions.

### Security
- No secrets are stored in the code, and all user input is checked before it’s used. Errors are logged for debugging, but no personal info is ever written to logs. If I were building this for real customers, I’d add HTTPS and user authentication.

### Operations (Ops)
- For logs and metrics, I’m using Python’s built-in logging module to capture API requests and errors. 

- To scale, I would run multiple containers, but there are certainly limits to how far this simple design can go. 

- Known limitations: Cart data is lost on restart, no user authentication, and no persistent storage for orders. These are fine for a demo, but would need to be fixed for a production app.

---

## 5) Results & Evaluation


**All tests passing:**
```
✓ GET /products returns 200 with JSON list
✓ GET /products/<id> returns correct product
✓ GET /products/invalid returns 404
✓ POST /cart/add validates required fields
✓ Health check works
✓ CORS headers present
✓ All responses are valid JSON

===================== 15 passed in 0.45s =====================
```

### Performance

| Metric | Value |
|--------|-------|
| Image Size | ~150MB |
| Startup Time | <5s |
| Memory Usage | ~100MB |
| Response Time | ~5ms |
| Requests/sec | 100+ (single container) |


---

## 6) What's Next
- [ ] MongoDB for persistent storage
- [ ] Product filtering/search
- [ ] User registration/authorization
- [ ] Order history
- [ ] Payment integration (Stripe)
- [ ] Email registration popup

---

## 7) Links & References

### GitHub Repository
https://github.com/kbr8ey/FinalCase


## License

MIT License - See [LICENSE](LICENSE) for details.



