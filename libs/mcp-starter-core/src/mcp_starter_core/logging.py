"""Structured process logging configured for MCP stdio and HTTP deployments."""

import logging
import sys

import structlog
from structlog.types import Processor


def configure_logging(level: str = "INFO", output: str = "console") -> None:
    """Configure structured logs on stderr so stdio protocol output stays clean."""
    logging.basicConfig(level=level, format="%(message)s", stream=sys.stderr, force=True)
    renderer: Processor
    if output == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level)),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
