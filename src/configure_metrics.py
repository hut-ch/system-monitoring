"""Helper function for all metrics to be captured"""

import socket
import time

import psutil

from logs import get_logger

# Initialise logger
logger = get_logger(__name__)


def cpu_metrics():
    """Gather base set of CPU specific metrics from psutils"""
    try:
        return {
            "timestamp": time.time(),
            "host": socket.gethostname(),
            "cpu_count": psutil.cpu_count(),
            "physical_cpu_count": psutil.cpu_count(logical=False),
            "cpu_frequency": psutil.cpu_freq(percpu=True),
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


def memory_metrics():
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
                    ["total", "used", "free", "percent_used", "swap_in", "swap_out"],
                    psutil.swap_memory(),
                )
            ),
        }
    except psutil.AccessDenied:
        logger.error("Permission denied while collecting CPU metrics.")
        return None
    except psutil.Error as e:
        logger.error("Unexpected psutil error while collecting CPU metrics: %s", e)
        return None


def disk_metrics():
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
                    ["total", "used", "free", "percentage_used"], psutil.disk_usage("/")
                )
            ),
            "disk_io": [
                {"disk": part, **disk._asdict()}
                for part, disk in psutil.disk_io_counters(perdisk=True).items()
            ],
        }
    except psutil.AccessDenied:
        logger.error("Permission denied while collecting CPU metrics.")
        return None
    except psutil.Error as e:
        logger.error("Unexpected psutil error while collecting CPU metrics: %s", e)
        return None


def network_metrics():
    """Gather base set of disk/mount specific metrics from psutils"""
    try:
        return {
            "timestamp": time.time(),
            "network stats": psutil.net_if_stats(),
            "netwrok_io": psutil.net_io_counters(pernic=True),
        }
    except psutil.AccessDenied:
        logger.error("Permission denied while collecting CPU metrics.")
        return None
    except psutil.Error as e:
        logger.error("Unexpected psutil error while collecting CPU metrics: %s", e)
        return None
