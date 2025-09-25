from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from nornir.core.task import Task, Result


def show_sros_scrapli(task: Task) -> Result:
    """
    Таска Nornir для выполнения 'show version' на Nokia SR OS
    с обработкой ошибок.
    """
    device = {
        "host": task.host.hostname,
        "auth_username": task.host.username,
        "auth_password": task.host.password,
        "auth_strict_key": False,
        "platform": "nokia_sros",
        "port": task.host.get("port", 22),
    }

    try:
        with Scrapli(**device) as conn:
            reply = conn.send_command("show version")
            task.host["show_version"] = reply.result
            print(f"\n=== {task.host} ===\n{reply.result}")

    except ScrapliException as e:
        task.host["show_version_error"] = str(e)
        print(f"\n=== {task.host} === ERROR: {e}")
