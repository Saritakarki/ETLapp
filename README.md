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
