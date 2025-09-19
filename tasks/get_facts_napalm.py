from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Task, Result


def get_facts_napalm(task: Task) -> Result:
    """
    Получить базовую информацию об устройстве через napalm_sros
    """
    try:
        result = task.run(task=napalm_get, getters=["facts", "interfaces"])

    except Exception as e:
        return Result(host=task.host, failed=True, exception=e)

    return Result(host=task.host, result=result.result)  # прокидываем данные дальше
