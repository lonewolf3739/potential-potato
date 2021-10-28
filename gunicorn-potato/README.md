## install

```sh
python -m pip install -r requirements-experiment.txt
```

## run

```sh
gunicorn app -c gunicorn.config.py
curl "http://localhost:8000/fibonacci?n=12"
```
