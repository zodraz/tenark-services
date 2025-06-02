FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y curl gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*
COPY recommendation-service.py .
COPY requirements.txt .
RUN apt-get update && apt-get install -y unixodbc-dev && pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "recommendation-service.py"]