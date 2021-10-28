## install

```sh
python -m pip install -r requirements-experiment.txt
```

## run

* start broker

```sh
docker run -p 5672:5672 rabbitmq
```

* run

```sh
celery -A app worker --loglevel=INFO --concurrency=10
```

* send task

```python
>>> from app import add
>>> add.delay(1, 2)
```
