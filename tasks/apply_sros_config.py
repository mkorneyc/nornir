from nornir.core.task import Task, Result
from pysros.management import connect
import json
import logging

logger = logging.getLogger("nornir")


def apply_sros_config(task: Task) -> Result:
    logger.debug(f"Начало задачи {task.name} на хосте {task.host.name}")
    node = {
        "host": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
    }

    try:
        config_file = task.host.data.get("config_file")
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        changed = False

        device = connect(**node, hostkey_verify=False)
        path = "/nokia-conf:configure/system/management-interface"
        #        current_config = device.running.get(path)

        device.candidate.set(path, config, commit=False)
        #        candidate_config = device.candidate.get(path)

        diff = device.candidate.compare(output_format="md-cli")

        if diff:
            changed = True
            result = "changed"
            device.candidate.commit()
        else:
            result = "unchanged"
            device.candidate.discard()

        device.disconnect()

    except Exception as e:
        logger.error(f"Ошибка на {task.host.name}: {e}")
        return Result(host=task.host, failed=True, result=f"Error: {e}")

    return Result(host=task.host, result=result, diff=diff, changed=changed)
