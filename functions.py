FILEPATH = "task.txt"

def get_task(filepath=FILEPATH):
    """ read text file and return the list of task items"""

    with open(filepath, "r") as file_local:
        tasks_local = file_local.readlines()
    return tasks_local


def write_tasks(tasks_args, filepath=FILEPATH):
    """write task list to text file"""

    with open(filepath, "w") as file:
        file.writelines(tasks_args)