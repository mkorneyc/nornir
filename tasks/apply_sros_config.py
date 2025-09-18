from nornir.core.task import Task, Result
from pysros.management import connect
import os
from pysros.wrappers import Leaf, Container
import json

def apply_sros_config(task: Task) -> Result:
    node = {
        "host": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password
    }


    try:

        config_file = task.host.data.get("config_file")
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        changed = False




        device = connect(**node, hostkey_verify=False)
        path = '/nokia-conf:configure/system/management-interface'
        current_config = device.running.get(path)


        device.candidate.set(path, config, commit=False)
        candidate_config = (device.candidate.get(path))


        diff=device.candidate.compare(output_format='md-cli')

        if diff:
            changed = True
            device.candidate.commit()

        device.disconnect() 

        return Result(
            host=task.host,
            diff=diff,
            changed=changed
        )


    except Exception as e:
        return Result(host=task.host, failed=True, result=f"Error: {e}")