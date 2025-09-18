from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks import *


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


def full_workflow(task: Task) -> Result:
    task.run(task=apply_sros_config)
    task.run(task=get_sros_config)
    task.run(task=run_sros_ping)
    task.run(task=set_sros_hostname)
    return Result(host=task.host)


# result = nr.run(task=full_workflow)
result = nr.run(task=apply_sros_config)
print_result(result)
