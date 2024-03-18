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

