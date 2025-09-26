"""Helper function for all metrics to be captured"""

import socket
import time

import psutil

from logs import get_logger

# Initialise logger
logger = get_logger(__name__)


class MetricsCollector:
    """Helper class to collect various system metrics"""

    def __init__(self):
        self._previous_net_counters = {}

    def cpu_metrics(self):
        """Gather base set of CPU specific metrics from psutils"""
        try:
            return {
                "timestamp": time.time(),
                "host": socket.gethostname(),
                "cpu_count": psutil.cpu_count(),
                "physical_cpu_count": psutil.cpu_count(logical=False),
                "cpu_frequency": psutil.cpu_freq(percpu=True),
                "cpu_overall_percentage": psutil.cpu_percent(),
                "cpu_percentage": psutil.cpu_percent(percpu=True),
                "cpu_stats": psutil.cpu_stats(),
                "cpu_times": psutil.cpu_times(),
                "cpu_times_percentage": psutil.cpu_times_percent(),
                "cpu_load_average": psutil.getloadavg(),
            }
        except psutil.AccessDenied:
            logger.error("Permission denied while collecting CPU metrics.")
            return None
        except psutil.Error as e:
            logger.error("Unexpected psutil error while collecting CPU metrics: %s", e)
            return None

    def memory_metrics(self):
        """Gather base set of memory specific metrics from psutils"""
        try:
            return {
                "timestamp": time.time(),
                "memory_usage": dict(
                    zip(
                        [
                            "total",
                            "available",
                            "percent_used",
                            "used",
                            "free",
                            "active",
                            "inactive",
                            "buffers",
                            "cached",
                            "wired",
                            "shared",
                        ],
                        psutil.virtual_memory(),
                    )
                ),
                "memory_swap": dict(
                    zip(
                        [
                            "total",
                            "used",
                            "free",
                            "percent_used",
                            "swap_in",
                            "swap_out",
                        ],
                        psutil.swap_memory(),
                    )
                ),
            }
        except psutil.AccessDenied:
            logger.error("Permission denied while collecting Memory metrics.")
            return None
        except psutil.Error as e:
            logger.error(
                "Unexpected psutil error while collecting Memory metrics: %s", e
            )
            return None

    def disk_metrics(self):
        """Gather base set of disk/mount specific metrics from psutils"""
        try:
            return {
                "timestamp": time.time(),
                "disks": [
                    dict(zip(["device", "mountpoint", "fstype", "opts"], disk))
                    for disk in psutil.disk_partitions(all=False)
                ],
                "disk_usage": dict(
                    zip(
                        ["total", "used", "free", "percentage_used"],
                        psutil.disk_usage("/"),
                    )
                ),
                "disk_io": [
                    {"disk": part, **disk._asdict()}
                    for part, disk in psutil.disk_io_counters(perdisk=True).items()
                ],
            }
        except psutil.AccessDenied:
            logger.error("Permission denied while collecting Disk metrics.")
            return None
        except psutil.Error as e:
            logger.error("Unexpected psutil error while collecting Disk metrics: %s", e)
            return None

    def network_metrics(self, interval: int = 1):
        """Gather base set of netwrok specific metrics from psutils
        and calculate uload and downlad rates
        """

        try:
            # Current snapshot of network counters
            current_net_counters = psutil.net_io_counters(pernic=True)

            upload_download_stats = {}

            # Calculate upload/download if we have a previous snapshot
            if self._previous_net_counters:
                for nic, current_stats in current_net_counters.items():

                    prev_stats = self._previous_net_counters.get(nic)
                    if prev_stats:
                        # Bytes sent and received in the interval
                        uploaded = current_stats.bytes_sent - prev_stats.bytes_sent
                        downloaded = current_stats.bytes_recv - prev_stats.bytes_recv

                        upload_download_stats[nic] = {
                            "uploaded": uploaded,
                            "upload_speed": round((uploaded / interval), 2),
                            "downloaded": downloaded,
                            "download_speed": round((downloaded / interval), 2),
                        }

            # Update previous counters for next call
            self._previous_net_counters = current_net_counters

            return {
                "timestamp": time.time(),
                "network stats": {
                    nic: {**nicstats._asdict()}
                    for nic, nicstats in psutil.net_if_stats().items()
                },
                "network_io": {
                    nic: {**netio._asdict()}
                    for nic, netio in psutil.net_io_counters(pernic=True).items()
                },
                "upload_download": upload_download_stats,
            }

        except psutil.AccessDenied:
            logger.error("Permission denied while collecting Network metrics.")
            return None

        except psutil.Error as e:
            logger.error(
                "Unexpected psutil error while collecting Network metrics: %s", e
            )
            return None
