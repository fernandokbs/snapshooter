from dotenv import dotenv_values, set_key
import requests

env_config = dotenv_values('.env')

class BackupService:
    BASE_URL = 'https://api.snapshooter.com/v1'
    BASE_DESTINATION_PATH = '/home/fernando/snapshooter'

    def __init__(self):
        self.token = env_config.get('SNAPSHOOTER_TOKEN')
        self.backup_id = "4a3ec18c-337a-4762-893e-47189598dbd1"
        self.job_id = "f11dbfc0-21e2-48ea-9987-d5192daede3d"

        if not self.token:
            raise Exception("Key not found")

    def job_ids(self):
        response = requests.get(f'{self.BASE_URL}/jobs', headers=self._headers())
        jobs_data = response.json()
        job_ids = []

        if response.status_code == 200:
            for job in jobs_data['data']:
                job_ids.append({
                    'id': job['id'],
                    'name': job['name']
                })
            return job_ids
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def run_backups(self):
        job_ids = self.job_ids()

        for job in job_ids:
            job_id = job['id']
            job_name = job['name']
            job_url = f'{self.BASE_URL}/jobs/{job_id}/backups/start'
            print(f'Running backup for {job_name} with id: {job_id}')

            response = requests.post(job_url, headers=self._headers(), data=self._data_binary())

    def test_backup(self):
        url = f'{self.BASE_URL}/jobs/{self.job_id}/backups/start'

        response = requests.post(url, headers=self._headers(), data=self._data_binary())
        backup_data = response.json()

        print(backup_data)

    def backup_status(self):
        response = requests.get(f'{self.BASE_URL}/backups/{self.backup_id}', headers=self._headers())
        json_data = response.json()
        print(json_data)

    def download_backup(self):
        response = requests.post(f'{self.BASE_URL}/backups/{self.backup_id}/download', headers=self._headers())
        json_data = response.json()

        for key, value in json_data['data'].items():
            file_name = key.split('/')[-1]
            print(f"Key: {file_name}, Value: {value}")
            self._download_file(f'{self.BASE_DESTINATION_PATH}r/{file_name}', value)

    def call(self):
        self.run_backups()

    def _download_file(self, file_destination_path, url_file):
        with requests.get(url_file, stream=True)  as response:
            response.raise_for_status()

            with open(file_destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

        return url_file

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f'Bearer {self.token}'
        }

    def _data_binary(self):
        return """
        {
        "is_manual": true,
        "is_hourly": false,
        "is_daily": false,
        "is_weekly": false,
        "is_monthly": false
        }
        """

    @classmethod
    def run(cls):
        (BackupService()).call()


if __name__ == '__main__':
    BackupService.run()