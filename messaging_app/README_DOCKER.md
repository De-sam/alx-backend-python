# Docker Setup for Django Messaging App

This guide explains how to containerize and run your Django messaging app using Docker.

## What's Included

- **Dockerfile** - Multi-stage build for production-ready images
- **docker-compose.yml** - Easy orchestration with database and volumes
- **.dockerignore** - Optimized build context
- **docker-run.sh** - Unix/Linux/Mac script for easy deployment
- **docker-run.bat** - Windows script for easy deployment

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### Option 2: Using Docker Commands

```bash
# Build the image
docker build -t messaging-app .

# Run the container
docker run -d --name messaging-app-container -p 8000:8000 messaging-app

# Stop the container
docker stop messaging-app-container

# Remove the container
docker rm messaging-app-container
```

### Option 3: Using the Scripts

#### On Unix/Linux/Mac:
```bash
./docker-run.sh
```

#### On Windows:
```cmd
docker-run.bat
```

## File Structure

```
messaging_app/
├── Dockerfile              # Main Docker configuration
├── docker-compose.yml      # Multi-service orchestration
├── .dockerignore          # Files to exclude from build
├── docker-run.sh          # Unix/Linux/Mac run script
├── docker-run.bat         # Windows run script
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── messaging_app/         # Django project settings
```

## Dockerfile Features

- **Base Image**: Python 3.10-slim (lightweight)
- **Security**: Non-root user execution
- **Optimization**: Multi-layer caching
- **Health Check**: Built-in health monitoring
- **Port**: Exposes port 8000

## Accessing Your App

Once running, your Django app will be available at:
- **Local**: http://localhost:8000
- **Network**: http://your-ip:8000

## Useful Docker Commands

### Container Management
```bash
# List running containers
docker ps

# View container logs
docker logs messaging-app-container

# Access container shell
docker exec -it messaging-app-container bash

# Stop container
docker stop messaging-app-container

# Remove container
docker rm messaging-app-container
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi messaging-app

# Clean up unused images
docker image prune
```

### Volume Management
```bash
# List volumes
docker volume ls

# Remove volumes
docker volume rm messaging_app_static_volume messaging_app_media_volume
```

## Development Workflow

### 1. Make Code Changes
Edit your Django code in your local directory.

### 2. Rebuild and Restart
```bash
# Stop current container
docker stop messaging-app-container

# Remove old container
docker rm messaging-app-container

# Rebuild and start
docker build -t messaging-app .
docker run -d --name messaging-app-container -p 8000:8000 -v $(pwd):/app messaging-app
```

### 3. View Logs
```bash
docker logs -f messaging-app-container
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Use a different port
   docker run -p 8001:8000 messaging-app
   ```

2. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

3. **Database Issues**
   ```bash
   # Run migrations inside container
   docker exec -it messaging-app-container python manage.py migrate
   ```

4. **Static Files Not Loading**
   ```bash
   # Collect static files
   docker exec -it messaging-app-container python manage.py collectstatic
   ```

### Debug Mode

To run with debug output:
```bash
docker run -it --rm -p 8000:8000 messaging-app python manage.py runserver 0.0.0.0:8000
```

## Production Considerations

For production deployment, consider:

1. **Environment Variables**: Use `.env` files for sensitive data
2. **Database**: Use PostgreSQL or MySQL instead of SQLite
3. **Static Files**: Serve with Nginx or CDN
4. **Security**: Remove DEBUG=True, use HTTPS
5. **Monitoring**: Add logging and health checks
6. **Scaling**: Use Docker Swarm or Kubernetes

## Support

If you encounter issues:
1. Check the container logs: `docker logs messaging-app-container`
2. Verify Docker is running: `docker info`
3. Check port availability: `lsof -i :8000`
4. Ensure all files are in the correct location 