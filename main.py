from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from dotenv import load_dotenv
import os

# from tasks import *
from tasks import (
    apply_sros_config,
    get_sros_config,
    run_sros_ping,
    set_sros_hostname,
    fetch_config,
    get_facts_napalm,
    set_hostname_napalm,
    show_sros_scrapli,
)

load_dotenv()


def full_workflow(task: Task) -> Result:
    task.run(task=apply_sros_config)
    task.run(task=get_sros_config)
    task.run(task=run_sros_ping)
    task.run(task=set_sros_hostname)
    task.run(task=fetch_config)
    return Result(host=task.host)


def main():

    nr = InitNornir(
        config_file="config.yaml",
        logging={
            "enabled": True,  # Включить логирование
            "level": "DEBUG",  # Уровень логирования: DEBUG, INFO, WARNING, ERROR
            "log_file": "nornir.log",  # Файл для записи логов
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат логов
            "to_console": False,  # Выводить ли логи в консоль
        },
    )

    for host in nr.inventory.hosts.values():
        if not getattr(host, "username", None):
            host.username = os.getenv("NORNIR_USERNAME")
        if not getattr(host, "password", None):
            host.password = os.getenv("NORNIR_PASSWORD")

    # result = nr.run(task=full_workflow)
    result = nr.run(task=show_sros_scrapli)

    #    new_hostnames = {host: f"{host}-lab" for host in nr.inventory.hosts}
    #
    #    result = nr.run(
    #        task=set_hostname_napalm, hostname=lambda task: new_hostnames[task.host.name]
    #    )

    print_result(result)


if __name__ == "__main__":
    main()
