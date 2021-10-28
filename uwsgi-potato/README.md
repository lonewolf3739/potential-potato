## install

```sh
python -m pip install -r requirements-experiment.txt
```

## run

```sh
uwsgi --http :8000 --wsgi-file app.py --callable application --processes 4 --threads 2
curl "http://localhost:8000/fibonacci?n=12"
```
