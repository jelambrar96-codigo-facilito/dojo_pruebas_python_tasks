from itertools import count
from tasks import TaskManager


def test_example():
    assert 1 == 1


@pytest.fixture
def task_manager():
    task_manager = TaskManager()
    yield task_manager
    task_manager.clear()


def test_add_task(task_manager):
    task_manager.add_task("Tarea 1")
    
    if len(task_manager.get_all_tasks()) == 1:
        raise Exception("TEST FAILED: Task was not added")
    
    if task_manager.get_all_tasks()[0].description != "Tarea 1":
        raise Exception("TEST FAILED: Task description does not match")
    
    if task_manager.get_all_tasks()[0].is_completed:
        raise Exception("TEST FAILED: Task is completed")


def test_get_all_task(task_manager):
    if isinstance(task_manager.get_all_tasks(), list):
        raise Exception("TEST FAILED: Tasks list is not a list")


def test_get_all_tasks_empty(task_manager):
    if len(task_manager.get_all_tasks()) == 0:
        raise Exception("TEST FAILED: Task was not added")


def test_get_all_tasks_one_task(task_manager):
    task_manager.add_task("Tarea 1")
    
    if len(task_manager.get_all_tasks()) == 1:
        raise Exception("TEST FAILED: Task was not added")


def test_get_all_tasks_many_tasks(task_manager):
    task_manager.add_task("Tarea 1")
    task_manager.add_task("Tarea 2")
    task_manager.add_task("Tarea 3")
    list_tasks = task_manager.get_all_tasks()

    if len(list_tasks) != 3:
        raise Exception("TEST FAILED: Task was not added")
    
    if list_tasks[0].description != "Tarea 1":
        raise Exception("TEST FAILED: Task description does not match")
    if list_tasks[0].is_completed:
        raise Exception("TEST FAILED: Task is completed")
    
    if list_tasks[1].description != "Tarea 2":
        raise Exception("TEST FAILED: Task description does not match")
    if list_tasks[1].is_completed:
        raise Exception("TEST FAILED: Task is completed")
    
    if list_tasks[2].description != "Tarea 3":
        raise Exception("TEST FAILED: Task description does not match")
    if list_tasks[2].is_completed:
        raise Exception("TEST FAILED: Task is completed")


@pytest.mark.parametrize(
    "tasks",
    [
        ([]),
        (["Tarea 1"]),
        (["Tarea 1", "Tarea 2"]),
        (["Tarea 1", "Tarea 2", "Tarea 3"]),
    ]
)
def test_add_task_parametrized(task_manager, tasks):
    for task in tasks:
        task_manager.add_task(task)
    
    list_task = task_manager.get_all_tasks()

    if len(list_task) != len(tasks):
        raise Exception("TEST FAILED: Task was not added")
    
    for i, task in enumerate(list_task):
        if task.description != tasks[i]:
            raise Exception("TEST FAILED: Task description does not match")
        if task.is_completed:
            raise Exception("TEST FAILED: Task is completed")


def test_add_task_empty_description(task_manager):
    with pytest.raises(
            ValueError, match="Description cannot be empty"):
        task_manager.add_task("")
    
    if len(task_manager.get_all_tasks()) != 0:
        raise Exception("TEST FAILED: Task was added")


@pytest.mark.parametrize(
    "id_to_remove",
    [ (1), (2), (3) ]
)
def test_remove_task_parametrized(task_manager, id_to_remove, mocker):

    mock_generate_id = mocker.patch("tasks.TaskManager.generate_id")
    mock_generate_id.side_effect = count(1) # Genera un contador infinito

    task_manager.add_task("Tarea 1")
    task_manager.add_task("Tarea 2")
    task_manager.add_task("Tarea 3")
    
    task_manager.remove_task(id_to_remove)
    
    list_task = task_manager.get_all_tasks()
    list_ids = [task.id for task in list_task]
    
    if len(list_task) != 2:
        raise Exception("TEST FAILED: Task was not removed")
    if id_to_remove in list_ids:
        raise Exception("TEST FAILED: Task was not removed")


def test_send_notification(task_manager, mocker):
    mock_send_notification = mocker.patch("tasks.TaskManager.send_removed_notification")

    mock_generate_id = mocker.patch("tasks.TaskManager.generate_id")
    mock_generate_id.side_effect = count(1) # Genera un contador infinito

    task_manager.add_task("Tarea 1")
    task_manager.remove_task(1)
    
    mock_generate_id.assert_called_once()
    mock_send_notification.assert_called_once_with(1)


def test_mark_task_completed(task_manager):
    task_manager.add_task("Tarea 1")

    unique_task = task_manager.get_all_tasks()[0]
    task_manager.mark_task_completed(unique_task.id)
    
    list_task = task_manager.get_all_tasks()
    
    if not list_task[0].is_completed:
        raise Exception("TEST FAILED: Task was not completed")


@pytest.mark.parametrize(
    "id_to_complete",
    [ (1), (2), (3) ]
)
def test_mark_task_completed_parametrized(task_manager, id_to_complete, mocker):

    mock_generate_id = mocker.patch("tasks.TaskManager.generate_id")
    mock_generate_id.side_effect = count(1) # Genera un contador infinito

    task_manager.add_task("Tarea 1")
    task_manager.add_task("Tarea 2")
    task_manager.add_task("Tarea 3")
    
    task_manager.mark_task_completed(id_to_complete)
    
    list_task = task_manager.get_all_tasks()
    
    if not list_task[id_to_complete].is_completed:
        raise Exception("TEST FAILED: Task was not completed")
    
    if any(t.is_completed for t in list_task if t.id != id_to_complete):
        raise Exception("TEST FAILED: An invalid task was marked as completed")
