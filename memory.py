class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.variables = {}

    def has_key(self, name):  # variable name
        return self.variables.get(name, None)

    def get(self, name):  # gets from memory current value of variable <name>
        return self.variables.get(name, None)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value

    def __contains__(self, item):
        return self.variables.__contains__(item)


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memory = memory
        self.content = []
        self.elements = 0
        if memory is not None:
            self.content = [self.memory]
            self.elements = 1

    def get(self, name, index=0):  # gets from memory stack current value of variable <name>
        for i in range(self.elements-1, -1, -1):
            if self.content[i].__contains__(name):
                if isinstance(self.content[i].get(name), list):
                    return self.content[i].get(name)[index]
                return self.content[i].get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        top = self.pop()
        top.put(name, value)
        self.push(top)

    def set(self, name, value, index=0):  # sets variable <name> to value <value>
        for i in range(self.elements):
            if self.content[i].__contains__(name):
                if isinstance(self.content[i].variables[name], list):
                    self.content[i].variables[name][index] = value
                else:
                    self.content[i].variables[name] = value

    def push(self, memory):  # pushes memory <memory> onto the stack
        if len(self.content) <= self.elements:
            self.content.append(memory)
        else:
            self.content[self.elements] = memory
        self.elements += 1

    def pop(self):  # pops the top memory from the stack
        self.elements -= 1
        return self.content[self.elements]
