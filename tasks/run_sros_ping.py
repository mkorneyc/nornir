from nornir.core.task import Task, Result
from pysros.management import connect
from pysros.pprint import printTree


def run_sros_ping(task: Task) -> Result:
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

        if (
            str(
                result.get("results")
                .get("summary")
                .get("statistics")
                .get("packets")
                .get("loss")
            )
            == "0.0"
        ):
            failed = False

        device.disconnect()

        return Result(host=task.host, failed=failed)

    except Exception as e:
        return Result(host=task.host, failed=True, result=f"Error: {e}")
