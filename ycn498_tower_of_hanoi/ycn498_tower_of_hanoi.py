import Queue

# Given n, returns a list representing a state with n disks on the leftmost tower
# Used to pass state arguments to search functions
def init_state(n):
    tower0, tower1, tower2 = [], [], []
    for x in range(n - 1, -1, -1):
        tower0.append(x)
    return [tower0, tower1, tower2]

# Given n, returns a list representing a state with n disks on the rightmost tower
# Used to pass state arguments to search functions
def end_state(n):
    tower0, tower1, tower2 = [], [], []
    for x in range(n - 1, -1, -1):
        tower2.append(x)
    return [tower0, tower1, tower2]

# Given a state, if a disk can be moved from the source tower to the destination tower, returns True
# Otherwise, returns False
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

# Given a state, returns a list representing the state with a disk moved from the source tower to the destination tower
def move(state, src, dst):
    next_state = state_copy(state)
    disk = next_state[src].pop()
    next_state[dst].append(disk)
    return next_state

# Given a filter, if any entry in the list passes the filter, returns False
# Otherwise, returns True
# Used to find if a state has already been searched
def does_not_contain(list, filter):
    for x in list:
        if filter(x):
            return False
    return True

# Prints the solution obtained by a completed search,
# along with the number of moves in the solution and the total number of searches it took to find
def print_solution(n, state_memory, move_count, search_name):
    print("Solved!")
    print("Solution is shown below:\n")

    solution_state = state_memory.pop()
    solution_states = []
    solution_move_count = 0

    # Uses references to trace the solution back to the initial state, adding each state to a list
    # Then uses the list to output the solution
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

# Prints a visual representation of a state
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

# Given a state, returns a copy of the same state
# Used in move() function to bypass Python's default pass-by-reference behaviour
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

# Given two states, returns a score rating their similarity, based on the number of disks in the same position
# Heuristic used to order the priority queue in the best-first search function, so the highest score is 0
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

# State class designed to hold state information and a reference to the previous State in the search
class State:
    def __init__(self, state, previous_state):
        self.state = state
        self.previous_state = previous_state

# Depth-first search function wrapper
# Given n, runs the search function with the initial state having n disks on the leftmost tower
# and the end state having n disks on the rightmost tower
def DFS_wrapper(n):
    DFS(init_state(n), end_state(n))

# Depth-first search, takes an initial state and an end state as parameters
def DFS(init_state, end_state):
    # Checks that the two states have the same number of disks
    n = len(init_state[0]) + len(init_state[1]) + len(init_state[2])
    m = len(end_state[0]) + len(end_state[1]) + len(end_state[2])
    if n != m:
        print("Those two states are incompatible.")
        return

    print("Starting depth-first search...\n")

    # Initializing variables
    move_count = 0
    state_stack = [State(init_state, None)]
    state_memory = [State(init_state, None)]

    # Continues to run as long as there are states to check in the stack
    while state_stack:
        current_state = state_stack.pop()
        print_state(n, current_state.state)
        move_count += 1

        # End state check, if so, prints the solution and clears the stack
        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "DFS")
            del state_stack[:]
        else:
            # Iterates through all the possible disk movements from the current state,
            # and adds any resulting unsearched state to the state memory variable before pushing it onto the stack
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            state_memory.append(next_state)
                            state_stack.append(next_state)

# Breadth-first search function wrapper
# Given n, runs the search function with the initial state having n disks on the leftmost tower
# and the end state having n disks on the rightmost tower
def BFS_wrapper(n):
    BFS(init_state(n), end_state(n))

# Breadth-first search, takes an initial state and an end state as parameters
def BFS(init_state, end_state):
    # Checks that the two states have the same number of disks
    n = len(init_state[0]) + len(init_state[1]) + len(init_state[2])
    m = len(end_state[0]) + len(end_state[1]) + len(end_state[2])
    if n != m:
        print("Those two states are incompatible.")
        return

    print("Starting breadth-first search...\n")

    # Initializing variables
    move_count = 0
    state_queue = Queue.Queue()
    state_queue.put(State(init_state, None))
    state_memory = [State(init_state, None)]

    # Continues to run as long as there are states to check in the queue
    while not state_queue.empty():
        current_state = state_queue.get()
        print_state(n, current_state.state)
        move_count += 1

        # End state check, if so, prints the solution and clears the queue
        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "BFS")
            state_queue.queue.clear()
        else:
            # Iterates through all the possible disk movements from the current state,
            # and adds any resulting unsearched state to the state memory variable before enqueuing it
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            state_memory.append(next_state)
                            state_queue.put(next_state)

# Best-first search function wrapper
# Given n, runs the search function with the initial state having n disks on the leftmost tower
# and the end state having n disks on the rightmost tower
def BestFS_wrapper(n):
    BestFS(init_state(n), end_state(n))

# Best-first search, takes an initial state and an end state as parameters
def BestFS(init_state, end_state):
    # Checks that the two states have the same number of disks
    n = len(init_state[0]) + len(init_state[1]) + len(init_state[2])
    m = len(end_state[0]) + len(end_state[1]) + len(end_state[2])
    if n != m:
        print("Those two states are incompatible.")
        return

    print("Starting best-first search...\n")

    # Initializing variables
    move_count, queue_count = 0, 0
    state_queue = Queue.PriorityQueue()
    state_queue.put((state_compare(n, init_state, end_state), queue_count, State(init_state, None)))
    state_memory = [State(init_state, None)]

    # Continues to run as long as there are states to check in the queue
    while not state_queue.empty():
        current_state = state_queue.get()[2]
        print_state(n, current_state.state)
        move_count += 1

        # End state check, if so, prints the solution and clears the queue
        if current_state.state == end_state:
            print_solution(n, [current_state], move_count, "BestFS")
            del state_queue.queue[:]
        else:
            # Iterates through all the possible disk movements from the current state,
            # and adds any resulting unsearched state to the state memory variable before enqueuing it
            for x in range(0, 3):
                for y in range(0, 3):
                    if movable(current_state.state, x, y):
                        next_state = State(move(current_state.state, x, y), current_state)
                        if does_not_contain(state_memory, lambda x: x.state == next_state.state):
                            queue_count += 1
                            state_memory.append(next_state)
                            state_queue.put((state_compare(n, next_state.state, end_state), queue_count, next_state))

DFS_wrapper(4)
BFS_wrapper(4)
BestFS_wrapper(4)
