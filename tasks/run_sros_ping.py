from nornir.core.task import Task, Result
from pysros.management import connect
import logging

logger = logging.getLogger("nornir")

# from pysros.pprint import printTree


def run_sros_ping(task: Task) -> Result:
    logger.debug(f"Начало задачи {task.name} на хосте {task.host.name}")
    node = {
        "host": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
    }
    failed = True

    try:
        device = connect(**node, hostkey_verify=False)
        path = "/nokia-oper-global:global-operations/ping"
        input_data = {"destination": "192.168.25.200", "router-instance": "management"}
        result = device.action(path, input_data)
        #        print(node.get('host'))
        #        printTree(result)
        #        print(dict(result))

        loss = str(
            result.get("results")
            .get("summary")
            .get("statistics")
            .get("packets")
            .get("loss")
        )

        if loss == "0.0":
            failed = False
        else:
            pass
        device.disconnect()

        logger.info(f"Потеря пакетов на хосте {task.host.name}: {loss}%")

    except Exception as e:
        return Result(host=task.host, failed=True, result=f"Error: {e}")

    return Result(host=task.host, failed=failed)
