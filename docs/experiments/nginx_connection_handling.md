# Nginx Connection Handling Experiment

## Objective
Understand how Nginx decouples client connections from backend (Gunicorn) connections.

## Setup
- Gunicorn running with 2 workers
- Nginx as reverse proxy
- Keep-alive enabled

## Observations

### Without Nginx
- Each client request directly consumes a Gunicorn worker
- Slow clients increase worker occupancy time
- Limited scalability

### With Nginx
- Nginx handles multiple client connections efficiently
- Backend connections are reused
- Gunicorn workers are freed faster

## Key Insight
Nginx acts as a connection broker, reducing backend load and improving scalability.