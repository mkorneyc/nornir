from nornir_napalm.plugins.tasks import napalm_configure
from nornir.core.task import Task, Result


def set_hostname_napalm(task: Task, hostname: str) -> Result:
    """
    Задача: установить hostname на устройстве SROS
    """
    config = f"""
    /configure system name {hostname}
    """

    result = task.run(
        task=napalm_configure,
        configuration=config,
        replace=False,  # False = добавить к текущей конфигурации
        commit_message=f"Set hostname to {hostname}",
    )

    return Result(host=task.host, result=f"Hostname set to {hostname}")
