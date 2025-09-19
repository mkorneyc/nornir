from nornir.core.task import Task, Result
from pysros.management import connect
import logging

logger = logging.getLogger("nornir")

path = "/nokia-conf:configure/system"


def set_sros_hostname(task: Task) -> Result:
    node = {
        "host": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
    }

    try:
        device = connect(**node, hostkey_verify=False)
        current_hostname = str(
            device.running.get("/nokia-conf:configure/system").get("name")
        )
        desired_hostname = task.host.data.get("hostname")

        changed = False
        if current_hostname != desired_hostname:
            device.candidate.set(path, {"name": desired_hostname}, commit=True)
            changed = True
            logger.debug(
                f"Имя хоста изменено с {current_hostname} на {desired_hostname} на хосте {task.host.name}"
            )

        device.disconnect()

    except Exception as e:
        return Result(host=task.host, failed=True, result=f"Error: {e}")

    return Result(
        host=task.host,
        result={"old_hostname": current_hostname, "new_hostname": desired_hostname},
        changed=changed,
    )
