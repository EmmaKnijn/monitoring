# Knowledge Hub - System Monitoring

A distributed system monitoring application consisting of three components:
1.  **Agent:** Collects system statistics (CPU, RAM, Disk, Network) and reports them to the API.
2.  **API Receiver:** A Flask-based REST API that stores received statistics in a MySQL database.
3.  **Web UI:** A Flask-based dashboard that displays the collected statistics in a clean, responsive interface.

## Prerequisites
- Docker and Docker Compose installed.

## Deployment

To deploy the entire stack locally:

```bash
docker-compose up -d --build
```

This will start:
- **MySQL Database** on port 3306.
- **API Receiver** on port 5000.
- **Web UI Dashboard** on port 8080.
- **Monitoring Agent** (running as a container, reporting its own stats).

## Configuration

The application can be configured using environment variables in `docker-compose.yml`:

### Agent
- `API_URL`: The full URL of the API endpoint (e.g., `http://api:5000/api/v1/stats`).
- `REPORT_INTERVAL`: Frequency of reporting in seconds (default: `10`).
- `HOST_HOSTNAME`: The hostname to report. In `docker-compose.yml`, this is mapped to `${HOSTNAME}` to capture the actual host machine's name.

### API Receiver
- `DB_USER`: MySQL username (default: `root`).
- `DB_PASSWORD`: MySQL password (default: `password`).
- `DB_HOST`: MySQL hostname (default: `db`).
- `DB_NAME`: MySQL database name (default: `system_stats`).

### Web UI
- `API_URL`: The internal URL used by the web server to fetch stats from the API (default: `http://api:5000/api/v1/stats`).

## Accessing the Application

- **Dashboard:** Open [http://localhost:8080](http://localhost:8080) in your browser.
- **API Documentation (Swagger):** Open [http://localhost:5000/api/v1/docs](http://localhost:5000/api/v1/docs).
- **OpenAPI Spec:** Available at [http://localhost:5000/static/OpenAPI.yml](http://localhost:5000/static/OpenAPI.yml).

## Project Structure

- `/agent`: Python agent using `psutil`.
- `/api`: Flask REST API with SQLAlchemy.
- `/web`: Flask web application with Bootstrap.
- `/db`: Database initialization scripts.
- `OpenAPI.yml`: API specification.

## Multi-Device Support
The system supports multiple reporting agents. Each agent reports using its own hostname, and the dashboard displays statistics aggregated by device.

## Coding Style
This project follows **PEP-8** coding standards for all Python components.
