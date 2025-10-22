# Technical Specification (Template)
- Source: mqtt|http_poll|websocket|filewatch
- Parse: schema-validated mapping (Pydantic/Zod)
- Sink: http_push|mqtt_pub|s3_blob
- Observability: /healthz, /metrics
- Rollback: revert commit or disable flag
