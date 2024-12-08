from dotenv import dotenv_values, set_key
import requests

env_config = dotenv_values('.env')

print(env_config.get('SNAPSHOOTER_TOKEN'))

class BackupService:
    BASE_URL = 'https://api.snapshooter.com/v1'

    def __init__(self):
        self.token = env_config.get('SNAPSHOOTER_TOKEN')

        if not self.token:
            raise Exception("Key not found")

    def jobs(self):
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
        job_ids = self.jobs()


        for job in job_ids:
            job_id = job['id']
            print(f'{self.BASE_URL}/jobs/{job_id}/backups/start')

    def test_backup(self):
        job_id = "f11dbfc0-21e2-48ea-9987-d5192daede3d"
        url = f'{self.BASE_URL}/jobs/{job_id}/backups/start'

        data_binary = """
        {
        "is_manual": true,
        "is_hourly": false,
        "is_daily": false,
        "is_weekly": false,
        "is_monthly": false
        }
        """
        response = requests.post(url, headers=self._headers(), data=data_binary)

    def download_backups(self):
        pass

    def call(self):
        self.test_backup()

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f'Bearer {self.token}'
        }

    @classmethod
    def run(cls):
        (BackupService()).call()

backup_service = BackupService()

backup_service.run()