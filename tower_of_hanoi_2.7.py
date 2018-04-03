import Queue

def init_state(n):
    tower0, tower1, tower2 = [], [], []
    for x in range(n - 1, -1, -1):
        tower0.append(x)
    return [tower0, tower1, tower2]

def end_state(n):
    tower0, tower1, tower2 = [], [], []
    for x in range(n - 1, -1, -1):
        tower2.append(x)
    return [tower0, tower1, tower2]

def movable(state, src, dst):
    if src != dst:
        if state[src]:
            if state[dst]:
                if state[dst][-1] > state[src][-1]:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    else:
        return False

def move(state, src, dst):
    next_state = state_copy(state)
    disk = next_state[src].pop()
    next_state[dst].append(disk)
    return next_state

def does_not_contain(list, filter):
    for x in list:
        if filter(x):
            return False
    return True

def print_solution(n, state_memory, move_count, search_name):
    print("Solved!")
    print("Solution is shown below:\n")

    solution_state = state_memory.pop()
    solution_states = []
    solution_move_count = 0

    while solution_state.previous_state != None:
        solution_states.append(solution_state.state)
        solution_state = solution_state.previous_state
        solution_move_count += 1
    solution_states.append(solution_state.state)
    while solution_states != []:
        print_state(n, solution_states.pop())

    print("Total moves for " + search_name + " solution: "),
    print(solution_move_count)
    print("Total states searched: "),
    print(move_count)
    print("")

def print_state(n, state):
    for x in range(n-1, -1, -1):
        try:
            print(state[0][x]),
        except:
            print("|"),
        print(" "),
        try:
            print(state[1][x]),
        except:
            print("|"),
        print(" "),
        try:
            print(state[2][x])
        except:
            print("|")
    print("")

def state_copy(state):
    if state != None:
        tower0_copy, tower1_copy, tower2_copy = [], [], []
        for x in state[0]:
          tower0_copy.append(x)
        for x in state[1]:
          tower1_copy.append(x)
        for x in state[2]:
          tower2_copy.append(x)
        return [tower0_copy, tower1_copy, tower2_copy]

def state_compare(n, state, end_state):
    score = 0
    for x in range (0, min(len(state[0]), len(end_state[0]))):
        if state[0][x] == end_state[0][x]:
            score += 1
    for x in range (0, min(len(state[1]), len(end_state[1]))):
        if state[1][x] == end_state[1][x]:
            score += 1
    for x in range (0, min(len(state[2]), len(end_state[2]))):
        if state[2][x] == end_state[2][x]:
            score += 1
    return (n - score)

class State:
    def __init__(self, state, previous_state):
        self.state = state
        self.previous_state = previous_state

solved = False

def DFS(n):
    global solved

    print("Starting depth-first search...\n")

    while solved == False:
        DFS_helper(n, State(init_state(n), None), end_state(n), [State(init_state(n), None)], 0)
    solved = False

def DFS_helper(n, current_state, end_state, state_memory, move_count):
    global solved

    print_state(n, current_state.state)
    move_count += 1

    if current_state.state == end_state:
        print_solution(n, state_memory, move_count, "DFS")
        solved = True
    else:
        for x in range(0, 3):
            for y in range(0, 3):
                if movable(current_state.state, x, y):
                    next_state = State(move(current_state.state, x, y), current_state)
                    if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                        state_memory.append(next_state)
                        DFS_helper(n, next_state, end_state, state_memory, move_count)
                        if solved == True:
                            return

        print("Backtracking 1 step...")
        print_state(n, current_state.previous_state.state)

def DFS_custom(init_state, end_state):
    n = len(init_state[0]) + len(init_state[1]) + len(init_state[2])
    m = len(end_state[0]) + len(end_state[1]) + len(end_state[2])
    if n != m:
        print("Those two states are incompatible.")
        return

    print("Starting depth-first search...\n")

    move_count = 0
    state_stack = [State(init_state, None)]
    state_memory = [State(init_state, None)]

    while state_stack:
        current_state = state_stack.pop()
        print_state(n, current_state.state)
        move_count += 1

        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "DFS")
            del state_stack[:]
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            state_memory.append(next_state)
                            state_stack.append(next_state)

def BFS(n):
    print("Starting breadth-first search...\n")

    state_queue = Queue.Queue()
    state_queue.put(State(init_state(n), None))

    BFS_helper(n, end_state(n), [State(init_state(n), None)], state_queue, 0)

def BFS_helper(n, end_state, state_memory, state_queue, move_count):
    while not state_queue.empty():
        current_state = state_queue.get()
        print_state(n, current_state.state)
        move_count += 1

        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "BFS")
            state_queue.queue.clear()
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            state_memory.append(next_state)
                            state_queue.put(next_state)

def BFS_custom(init_state, end_state):
    n = len(init_state[0]) + len(init_state[1]) + len(init_state[2])
    m = len(end_state[0]) + len(end_state[1]) + len(end_state[2])
    if n != m:
        print("Those two states are incompatible.")
        return

    print("Starting breadth-first search...\n")

    move_count = 0
    state_queue = Queue.Queue()
    state_queue.put(State(init_state, None))
    state_memory = [State(init_state, None)]

    while not state_queue.empty():
        current_state = state_queue.get()
        print_state(n, current_state.state)
        move_count += 1

        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "BFS")
            state_queue.queue.clear()
            print('hiya')
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            state_memory.append(next_state)
                            state_queue.put(next_state)

def BestFS(init_state, end_state):
    n = len(init_state[0]) + len(init_state[1]) + len(init_state[2])
    m = len(end_state[0]) + len(end_state[1]) + len(end_state[2])
    if n != m:
        print("Those two states are incompatible.")
        return

    print("Starting best-first search...\n")

    move_count, queue_count = 0, 0
    state_queue = Queue.PriorityQueue()
    state_queue.put((state_compare(n, init_state, end_state), queue_count, State(init_state, None)))
    state_memory = [State(init_state, None)]

    while not state_queue.empty():
        current_state = state_queue.get()[2]
        print_state(n, current_state.state)
        move_count += 1

        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "BestFS")
            del state_queue.queue[:]
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            queue_count += 1
                            state_memory.append(next_state)
                            state_queue.put((state_compare(n, next_state.state, end_state), queue_count, next_state))
