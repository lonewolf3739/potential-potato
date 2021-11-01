import os
import time

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import get_tracer, get_tracer_provider, set_tracer_provider

set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "app"})))
exporter = InMemorySpanExporter()
get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter, schedule_delay_millis=50))

tracer = get_tracer(__name__, "0.1")


def func():
    print("pid: ", os.getpid())
    exporter.clear()

    with tracer.start_as_current_span("proc"):
        with tracer.start_as_current_span("inner_span"):
            pass
    time.sleep(0.5)
    spans = exporter.get_finished_spans()
    assert len(spans) == 2
    for span in spans:
        assert span.name in ["proc", "inner_span"]

if __name__ == "__main__":
    print("pid: ", os.getpid())
    pid = os.fork()
    if not pid:
        func()
    time.sleep(5)
