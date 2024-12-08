from dotenv import dotenv_values, set_key
import requests

env_config = dotenv_values('.env')

class BackupService:
    BASE_URL = 'https://api.snapshooter.com/v1'
    BASE_DESTINATION_PATH = '/home/fernando/snapshooter/backups'

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
                server_name = job['compute']['name']
                job_ids.append({
                    'id': job['id'],
                    'name': job['name'],
                    'server_name': server_name,
                })

            return job_ids
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def backup_ids(self):
        job_ids = self.job_ids()
        backup_ids = []
        for job in job_ids:
            job_id = job['id']
            job_name = job['name']
            job_server_name = job['server_name']

            response = requests.get(f'{self.BASE_URL}/jobs/{job_id}/backups', headers=self._headers())
            backup_data = response.json()['data']
            lastest_backup_data = backup_data[0]
            backup_id = lastest_backup_data['id']
            backup_files = lastest_backup_data['files']
            backup_ids.append({
                'id': backup_id,
                'name': job_name,
                'server_name': job_server_name,
                'files': backup_files
            })

        return backup_ids

    def run_backups(self):
        job_ids = self.job_ids()

        for job in job_ids:
            job_id = job['id']
            job_name = job['name']
            job_url = f'{self.BASE_URL}/jobs/{job_id}/backups/start'

            response = requests.post(job_url, headers=self._headers(), data=self._data_binary())
            backup_data = response.json()
            backup_id = backup_data['backup_id']
            print(f'Running backup for {job_name} with id: {job_id}: backup id: {backup_id}')

    def download_backups(self):
        backup_ids = self.backup_ids()

        for backup in backup_ids:
            if isinstance(backup, list) or isinstance(backup, dict):
                server_name = backup['server_name']
                print(f'Backup for: {server_name}')

                for file in backup['files']:
                    file_name = file['name']
                    file_name = file_name.split('/')[-1]
                    if "storage" in file_name:
                        file_name = f'{server_name}_storage'

                    file_url = file['url']
                    self._download_file(f'{self.BASE_DESTINATION_PATH}/{file_name}', file_url)

    def call(self):
        self.download_backups()
        # self.job_ids()

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