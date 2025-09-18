from nornir.core.task import Task, Result
import paramiko
from scp import SCPClient
import os


def fetch_config(
    task: Task, remote_file="cf3:/config.cfg", local_dir="backups"
) -> Result:
    os.makedirs(local_dir, exist_ok=True)
    local_file = os.path.join(local_dir, f"{task.host.name}_config.cfg")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            task.host.hostname, username=task.host.username, password=task.host.password
        )

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(remote_file, local_file)

        ssh.close()
        return Result(host=task.host, result=f"Config saved to {local_file}")

    except Exception as e:
        return Result(host=task.host, failed=True, result=str(e))
