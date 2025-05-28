from collections import deque, defaultdict

# Class to represent the Job with its tasks and dependencies
class Job:
    def __init__(self, tasks, dependencies, completion_times, validate_dependencies=False, validate_completion_time=False): 
        self.tasks = tasks
        self.dependencies = dependencies
        self.completion_times = completion_times
        self.graph = defaultdict(list)  # adjacency list
        self.in_degree = defaultdict(int)  # to track number of prerequisites

        if (validate_dependencies):
            self._validate_task_dependencies()

        if (validate_completion_time):
            self._validate_task_completion_times()
        # Build the graph
        for task, deps in dependencies.items():
            for dep in deps:
                self.graph[dep].append(task)
                self.in_degree[task] += 1


    def _validate_task_dependencies(self):
        # Validate that all dependencies are in the tasks list.
        # Collect all tasks that are mentioned as dependencies
        all_dependencies = {dep for deps in self.dependencies.values() for dep in deps}
        # Include the tasks that are keys in the dependencies dictionary
        all_dependencies.update(self.dependencies.keys())
        # Check if any dependency is not in the tasks list
        invalid_deps = all_dependencies - set(self.tasks)
        if invalid_deps:
            raise ValueError(f"Invalid dependencies: {', '.join(invalid_deps)} are not in the tasks list.")

    def _validate_task_completion_times(self):
        # Validate that each task has a corresponding completion time.
        missing_completions = [task for task in self.tasks if task not in self.completion_times]
        
        if missing_completions:
            raise ValueError(f"Missing completion times for tasks: {', '.join(missing_completions)}")

    def get_minimum_completion_time(self):
        # Initialize the queue with tasks that have no dependencies (in-degree == 0)
        queue = deque([task for task in self.tasks if self.in_degree[task] == 0])
        completion_time = {task: 0 for task in self.tasks}  # Stores the earliest completion times for each task
        task_order = []  # This will store the order of tasks
        
        while queue:
            task = queue.popleft()
            task_order.append(task)
            # Update the completion time for dependent tasks
            for dependent in self.graph[task]:
                # Calculate the minimum time to complete the dependent task
                completion_time[dependent] = max(completion_time[dependent], completion_time[task] + self.completion_times[task])
                self.in_degree[dependent] -= 1
                if self.in_degree[dependent] == 0:
                    queue.append(dependent)

        # If not all tasks are processed, a cycle exists
        if len(task_order) != len(self.tasks):
            raise ValueError("Cycle detected in task dependencies. Cannot complete all tasks.")
        
        # The minimum time to complete the entire job is the maximum completion time across all tasks
        min_time = max(completion_time[task] + self.completion_times[task] for task in self.tasks)
        return min_time, task_order

# Define the task information
tasks = ['A', 'B', 'C', 'D', 'E', 'F']
dependencies = {
    'D': ['A'],      # D depends on A
    'E': ['B', 'C'], # E depends on B and C
    'F': ['D', 'E']  # F depends on D and E
}
completion_times = {
    'A': 3,
    'B': 2,
    'C': 4,
    'D': 5,
    'E': 2,
    'F': 3
}

# Create a Job instance
job = Job(tasks, dependencies, completion_times, validate_dependencies=True, validate_completion_time=True)

# Get the minimum completion time and the task order
min_time, task_order = job.get_minimum_completion_time()

# Print the results
print(f"Minimum completion time: {min_time} units")
print(f"Task order: {task_order}")
