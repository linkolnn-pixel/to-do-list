import logging
from time import perf_counter
from fastapi import Request, Response


request_counter = 0

logger = logging.getLogger(__name__)


async def log_request(request: Request, call_next) -> Response:
    global request_counter
    request_counter += 1
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2f ms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_counter,
    )

    response.headers["X-Request-Number"] = str(request_counter)

    return response

