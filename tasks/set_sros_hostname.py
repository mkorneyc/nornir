from nornir.core.task import Task, Result
from pysros.management import connect

path = '/nokia-conf:configure/system'

def set_sros_hostname(task: Task) -> Result:
    node = {
        "host": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password
    }


    try:
        device = connect(**node, hostkey_verify=False)
        current_hostname = str(device.running.get("/nokia-conf:configure/system").get('name'))
        desired_hostname = task.host.data.get('hostname')

        changed = False
        if current_hostname != desired_hostname:
            device.candidate.set(path, {'name': desired_hostname}, commit=True)
            changed = True

        device.disconnect() 
        
        return Result(
            host=task.host,
            result={"old": current_hostname, "new": desired_hostname},
            changed=changed
        )

    except Exception as e:
        return Result(host=task.host, failed=True, result=f"Error: {e}")