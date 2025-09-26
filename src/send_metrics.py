"""Main script to send system metrics to Kafka"""

import json
import sys
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError, NoBrokersAvailable

from configure_metrics import MetricsCollector
from logs import get_logger

# Initialise logger
logger = get_logger(__name__)


def serialiser(message):
    """Serialise data ahead of senfgin to Kafka"""
    return json.dumps(message).encode("utf-8")


def init_producer(bootstrap_servers="kafka:9092"):
    """Initialise Kafka Producer or exit ion failure"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers, value_serializer=serialiser
        )
        logger.info("Kafka producer initialized successfully.")
        return producer
    except NoBrokersAvailable as e:
        logger.error("Kafka broker not available: %s", {e})
        sys.exit(1)
    except KafkaError as e:
        logger.error("Kafka error during producer setup: %s", {e})
        sys.exit(1)


def producer_send(producer: KafkaProducer, topic: str, message, retries=3, delay=1):
    """Send metrics to Kafka topic if send timesout retry given number of times"""

    send_attempt = 0
    while send_attempt <= retries:
        try:
            producer.send(topic, message)
            producer.flush()
            # logger.info("Successfully sent to topic %s", topic)
            return True
        except KafkaTimeoutError as e:
            send_attempt += 1
            delay_period = delay * (2 ** (send_attempt - 1))
            logger.warning(
                "Timeout sending to %s (attempt %s/%s): %s",
                topic,
                send_attempt,
                retries,
                e,
            )
            if send_attempt > retries:
                logger.error(
                    "Maximum number of attempts met message: %s not sent to %s",
                    message,
                    topic,
                )
                return False
            time.sleep(delay_period)

        except KafkaError as e:
            logger.error("Failed to send to topic %s: %s", topic, e)
            return False
    return False


def main(interval=5):
    """Gathers and sends metrics at set intervals"""

    producer = init_producer()
    metric_collector = MetricsCollector()

    try:
        while True:
            # Gather Metrics mapping Kafka topics to the
            # corresponding get_metric function
            metric_collectors = {
                "cpu_stats": metric_collector.cpu_metrics,
                "memory_stats": metric_collector.memory_metrics,
                "disk_stats": metric_collector.disk_metrics,
                "network_stats": lambda: metric_collector.network_metrics(interval),
                # Future metrics can be added here
            }

            # Iterate over metrics ands send to Kafka
            for topic, collector in metric_collectors.items():
                try:
                    message = collector()
                    producer_send(producer, topic, message)
                except KafkaError as e:
                    logger.error("Failed to collect or send %s: %s", topic, e)

            # Wait for next interval
            if time.strftime("%S") == "00":
                logger.info("Metrics still sending to Kafka")

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Script interrupted by user. Exiting gracefully.")
        sys.exit(0)


if __name__ == "__main__":
    main(interval=2)
