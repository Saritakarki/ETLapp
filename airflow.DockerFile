# Use the official Airflow image
FROM apache/airflow:2.2.0

# Install SQLite development libraries
USER root
RUN apt-get update && \
    apt-get install -y sudo sqlite3 libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy your DAG file and other required files into the container
COPY dags/etl_dag.py /opt/airflow/dags/etl_dag.py
COPY database.py /opt/airflow/dags/database.py
COPY api.py /opt/airflow/dags/api.py
COPY requirements.txt  /opt/airflow/

# Set the AIRFLOW_HOME environment variable
ENV AIRFLOW_HOME=/opt/airflow

# Upgrade pip to the latest version
RUN /usr/local/bin/python -m pip install --upgrade pip
# Install Requirements
RUN pip install --no-cache-dir -r requirements.txt

# Initialize the Airflow database (this will create the necessary tables)
RUN airflow db init

# Start the Airflow scheduler and webserver
CMD ["airflow", "webserver", "--port", "8080", "&", "airflow", "scheduler"]
