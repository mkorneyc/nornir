from nornir.core.task import Task, Result
from pysros.management import connect
import logging

logger = logging.getLogger("nornir")


def get_sros_config(task: Task) -> Result:
    node = {
        "host": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
    }

    try:
        device = connect(**node, hostkey_verify=False)
        config = device.running.get("/nokia-conf:configure")

        device.disconnect()

    except Exception as e:
        return Result(host=task.host, failed=True, result=f"Error: {e}")

    return Result(host=task.host, result=f"Config received")
