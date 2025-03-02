import numpy as np

class MetaLearningAlgorithm:
    def __init__(self):
        self.learning_rate = 0.01
        self.past_performance = []

    def learn_to_learn(self, tasks):
        meta_knowledge = self._aggregate_meta_knowledge(tasks)
        self._optimize_learning_rate(meta_knowledge)

    def _aggregate_meta_knowledge(self, tasks):
        valid_tasks = [task for task in tasks if hasattr(task, 'performance') and isinstance(task.performance, (int, float))]
        if not valid_tasks:
            raise ValueError("No valid tasks with performance data found.")
        return np.mean([task.performance for task in valid_tasks])

    def _optimize_learning_rate(self, meta_knowledge):
        self.past_performance.append(meta_knowledge)
        if len(self.past_performance) > 1:
            performance_trend = np.diff(self.past_performance)
            if performance_trend[-1] > 0:
                self.learning_rate *= 1.05  # Increase learning rate if performance is improving
            else:
                self.learning_rate *= 0.95  # Decrease learning rate if performance is declining
        self.learning_rate = max(min(self.learning_rate, 1.0), 0.0001)  # Clamp the learning rate between 0.0001 and 1.0