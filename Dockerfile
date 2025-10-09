FROM python:3.12-slim

WORKDIR /app

# Install uv with pip install --no-cache-dir ti redyce suze
RUN pip install --no-cache-dir uv

# Copy requirements file
COPY requirements.txt .

# Use uv pip compile to generate optimized requirements.txt with pinned versions
# Then install the dependencies and remove the lock file to keep the image clean
RUN uv pip compile requirements.txt -o requirements.lock && \
    uv pip sync --system requirements.lock && \
    rm requirements.lock

# Copy the test of application
COPY src/ ./src/


# Set environment variables
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1 \
    # add variables for optimization
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Clear unused packages and cache
RUN rm -rf /root/.cache && \
    find /usr/local -type d -name __pycache__ -exec rm -r {} + 

# Check the installation of langchain-core and execute the app
CMD ["sh", "-c", "python -c 'import langchain_core; print(\"Langchain-core is installed successfully.\")' && python src/main.py"]