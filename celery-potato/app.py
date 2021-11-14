#
# celery -A app worker --loglevel=INFO --concurrency=10
#


from opentelemetry import trace
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from celery import Celery

resource = Resource.create(attributes={"service.name": "name"})

trace.set_tracer_provider(TracerProvider(resource=resource))
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)

CeleryInstrumentor().instrument()

app = Celery("tasks", broker="amqp://localhost")


@app.task
def really_add(x, y):
    print(x + y)
    return x + y


@app.task
def add(x, y):
    print("nah!")
    really_add.delay(x, y)


add.delay(1, 2)
