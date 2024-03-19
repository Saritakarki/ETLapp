### ETL APP ###

In order to run the app in local follow the following steps:
1. Open the project in your IDE
2. Create a venv
3. `pip install -r requirements.txt`
4. Open terminal and go to root directory.
5. Run `python3 main.py`
 Then you can see the logging for data being extracted and saved to SQLite.

#### Check Data in SQLite ###
1. Install `sqlite3` in your device: `sudo apt install sqlite3`
2. Get inside SQLite interface: `sqlite3 app/news_data.sqlite`
3. `select * from news_data;`

### Using DockerFile ###
1. Build Docker File: `docker build -t testetl -f Dockerfile . --no-cache`
2. Run Docker File: `docker run testetl`


### Scheduling Job using Airflow DAG ###
There's a DAG file inside DAG folder.
1. `pip install apache-airflow`
2. Set `AIRFLOW_PATH = 'your_path'`
3. `airflow db init`
4. `cd ~your_airflow_path`
5. Check for `airflow.cfg` file and adjust the `dags_folder` path as the folder path for dags in the project
6. You are set to schedule the job: </br>
   a. `airflow scheduler` </br>
   b. `airflow webserver -p 8080` </br>
7. Now you can see your DAG listed in `http://0.0.0.0:8080/home`. Either trigger it manually or it will be auto triggered once a day as per the schedule.
   

### Running Tests ###
Make sure `pytest` is installed. Should be installed from `requirements.txt`.</br>
Go to Terminal and run `pytest`
- To test a single file run `pytest path/to/test.py::function_name`



#### Application Architecture: ####
The application follows a modular architecture, consisting of separate components for interacting with the API, managing the database, and running the main application logic.
It leverages Python as the primary programming language for its simplicity, versatility, and rich ecosystem of libraries for web scraping, API interaction, database management, and more.

#### API Interaction (api.py): ####
The api.py module is responsible for interacting with the external API (e.g., Spaceflight News API) to fetch data based on specific search terms.
It utilizes the requests library to send HTTP requests to the API endpoints, handles authentication if required, and processes the API responses.

#### Database Management (database.py): ####
The database.py module handles database interactions using SQLAlchemy ORM, providing an abstraction layer for managing database connections, executing queries, and handling transactions.
It defines database models using SQLAlchemy's declarative syntax, facilitating object-relational mapping between Python objects and database tables.

#### Main Application Logic (main.py): ####
The main.py module serves as the entry point for the application, orchestrating the data collection process by interacting with the API and database.
It utilizes the functionalities provided by api.py and database.py to fetch data from the API, process it, and store it in the database.

#### Containerization (Docker): ####
The application is containerized using Docker to ensure consistency and portability across different environments.
The Dockerfile defines the application's environment, dependencies, and runtime configuration, allowing the application to be packaged and run as a containerized service.

#### Database Storage (SQLite): ####
Since it's a test project, the application stores retrieved data in an SQLite database, chosen for its simplicity, lightweight footprint, and ease of use.
SQLite provides a self-contained, serverless database engine, making it suitable for small to medium-scale applications and prototyping.

#### Dynamic Search Terms: ####
The application supports dynamic search terms by storing search terms in a separate database table (SearchTerm) and iterating over these terms dynamically to collect data from the API.

#### Apache Airflow(etl_dag.py): ####
The application uses apache airflow to schedule the job daily. The DAG file defined does the process as explained above in this README. However,
docker file for this is not complete and fully tested due to time constraint. 

Overall, the application architecture emphasizes modularity, simplicity, and flexibility, leveraging Python, Docker, SQLAlchemy ORM, SQLite to facilitate efficient data retrieval, storage, and management and Apache airflow to schedule the job. It is designed to be scalable and extensible, allowing for future enhancements and integration with additional APIs or data sources as needed.