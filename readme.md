### Script to trigger and download backups from https://snapshooter.com/

## How to use

#### Copy .env
```bash
cp .env.example .env
```

### Conver token to base64
```bash
echo "token" | base64
```

#### Create virtual env

```
python3 -m venv env
source env/bin/activate
```

#### Install dependencies
```bash
pip3 install -r requirements.txt
```

#### Run script to trigger backups
```bash
python3 script.py backup
```

#### Run script to download backups
```bash
python3 script.py download
```