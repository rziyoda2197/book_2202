class Task:
    def __init__(self, title, done=False):
        self.title = title
        self.done = done

    def __repr__(self):
        return f"Task(title={self.title}, done={self.done})"


t = Task("OOP o'rganish")
print(t)

