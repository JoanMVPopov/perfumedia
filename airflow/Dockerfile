FROM apache/airflow:2.10.1

# Switch to root to install packages and add our entrypoint
USER root

# Install only the essential dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    xvfb \
    libnss3 \
    libxss1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER root

# Create the entrypoint script that launches Xvfb and then runs the main command
RUN echo '#!/usr/bin/env bash' > /entrypoint_xvfb.sh && \
    echo '# Start X virtual framebuffer in the background' >> /entrypoint_xvfb.sh && \
    echo 'Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset & ' >> /entrypoint_xvfb.sh && \
    echo 'export DISPLAY=:99' >> /entrypoint_xvfb.sh && \
    echo '' >> /entrypoint_xvfb.sh && \
    echo '# Wait a moment for Xvfb to start (optional, but can help prevent race conditions)' >> /entrypoint_xvfb.sh && \
    echo 'sleep 2' >> /entrypoint_xvfb.sh && \
    echo '' >> /entrypoint_xvfb.sh && \
    echo '# Execute the command passed into the container (e.g., airflow scheduler, worker, webserver)' >> /entrypoint_xvfb.sh && \
    echo 'exec "$@"' >> /entrypoint_xvfb.sh

# Make the new entrypoint script executable
RUN chmod +x /entrypoint_xvfb.sh

# Switch back to the airflow user
USER airflow 

# Set the new entrypoint
# This will be used by all services using this image, unless overridden in docker-compose.yml
ENTRYPOINT ["/entrypoint_xvfb.sh"]
