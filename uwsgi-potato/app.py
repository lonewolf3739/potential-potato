#
# i. uwsgi --http :8000 --wsgi-file app.py --callable application --master --enable-threads
# ii. uwsgi --http :8000 --wsgi-file app.py --callable application --processes 4 --threads 2
# iii. more?
#

import flask
from flask import request

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

application = flask.Flask(__name__)

FlaskInstrumentor().instrument_app(application)

resource = Resource.create(attributes={"service.name": "api-service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)


def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_fast(n - 2)


def fib_fast(n):
    nth_fib = [0] * (n + 2)
    nth_fib[1] = 1
    for i in range(2, n + 1):
        nth_fib[i] = nth_fib[i - 1] + nth_fib[i - 2]
    return nth_fib[n]


@application.route("/fibonacci")
def fibonacci():
    n = int(request.args.get("n", 1))
    with tracer.start_as_current_span("root"):
        with tracer.start_as_current_span("fib_slow") as slow_span:
            ans = fib_slow(n)
            slow_span.set_attribute("n", n)
            slow_span.set_attribute("nth_fibonacci", ans)
        with tracer.start_as_current_span("fib_fast") as fast_span:
            ans = fib_fast(n)
            fast_span.set_attribute("n", n)
            fast_span.set_attribute("nth_fibonacci", ans)

    return "F({}) is: ({})".format(n, ans)


if __name__ == "__main__":
    application.run()
