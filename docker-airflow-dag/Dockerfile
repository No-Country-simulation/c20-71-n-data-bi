
FROM apache/airflow:2.9.2

# Set the working directory
WORKDIR /usr/local/airflow

# Set environment variables for Apache Airflow
ENV AIRFLOW_HOME=/usr/local/airflow

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt $AIRFLOW_HOME/requirements.txt
RUN pip install --no-cache-dir -r $AIRFLOW_HOME/requirements.txt

# Copy DAGs and modules
COPY dags / $AIRFLOW_HOME/dags/

# Copy the .env file
COPY .env /opt/airflow/.env

# Initialize the Airflow database
RUN airflow db init

# Default command to run Airflow scheduler and webserver
CMD ["sh", "-c", "airflow scheduler & airflow webserver"]