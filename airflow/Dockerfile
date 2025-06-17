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

# Create an entrypoint script that starts Xvfb and then execs the given CMD
RUN cat << 'EOF' > /entrypoint.sh
#!/usr/bin/env bash
# Start X virtual framebuffer on display :99, 1920×1080×24
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# Hand off to whatever command was provided
exec "$@"
EOF

RUN chmod +x /entrypoint.sh

# Switch back to airflow user for normal operation
USER airflow

# Copy your Python dependencies and install them
COPY ./requirements.txt .

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Use our wrapper entrypoint, letting docker-compose still supply the CMD
ENTRYPOINT ["/entrypoint.sh"]
