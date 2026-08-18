# Architecture

VectorStream uses an append-only event store plus an aggregation engine. Ingestion performs idempotency by event ID, validates timestamps, and stores normalized events. Queries compute tumbling windows over event time. The interfaces intentionally allow replacement with Kafka/Redpanda, ClickHouse and object storage.
