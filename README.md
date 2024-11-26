# Project Hub Backend

A backend API in Django to manage Project and Tasks with role based access

## Steps to Run the Server

1. Clone the github repo
2. Create a virtual environment inside the folder with Python venv

```bash
python3 -m venv venv
```

3. Activate the virtual environment (Linux/macOs)

```bash
source venv/bin/activate
```
4.  Activate the virtual environment (Windows)
```powershell
venv\bin\Activate.ps1
```

5. Install the required libraries from requirements.txt

```console
pip3 install -r requirements.txt
```
6. Run the following command to set up the default SQLite database:

```console
python3 projecthub/manage.py migrate
```
7. Run the server
```console
python3 projecthub/manage.py runserver
```


## CORS

To add any list of domains for CORS got to projecthub -> projecthub -> settings.py and append the domain in the CORS_ALLOWED_ORIGINS

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",  # Vite React default
]
```

