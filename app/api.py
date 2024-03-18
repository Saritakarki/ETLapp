import requests
import logging
import time

logger = logging.getLogger('ETL Logger')


class APIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = 'https://api.spaceflightnewsapi.net/v4'

    def fetch_api_data(self, search_term: dict = None):
        url = f'{self.base_url}/articles'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                                 " like Gecko) Chrome/91.0.4472.77 Safari/537.36"
                   }

        logger.info('Fetching First Set of Data...')
        response = requests.get(url, headers=headers, params=search_term)
        results = {}
        if response.status_code == 200:
            response_json = response.json()
            next_url = response_json['next']
            results['results'] = response_json['results']

            # This count is set for this test app only so that we don't waste time pulling all the data
            count = 0
            while next_url and count < 10:
                time.sleep(2)  # waiting for 2 sec before making another call, not to overload API with requests
                logger.info('Fetching next page data..')
                # Requesting next data
                next_results = requests.get(next_url).json()

                # Adding to the original results dictionary
                results['results'] += next_results['results']

                # Updating the next URL
                next_url = next_results['next']
                count += 1
            logger.info('Completed Fetching Data!!')
            return results
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

