
import json
import logging
from aidetect.logging_setup import JsonFormatter

def test_json_formatter_outputs_json():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="aidetect.api",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request",
        args=(),
        exc_info=None,
    )
    record.request_id = "rid"
    record.method = "GET"
    record.path = "/health"
    record.status_code = 200
    record.elapsed_ms = 5

    s = formatter.format(record)
    data = json.loads(s)

    assert data["event"] == "request"
    assert data["request_id"] == "rid"
    assert data["path"] == "/health"
    assert "ts" in data
