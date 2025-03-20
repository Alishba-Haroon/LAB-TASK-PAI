from collections import deque
def water_jug(jug1, jug2, goal):
    queue = deque([(0, 0, [])])
    visited = set((0, 0))
    while queue:
        x, y, path = queue.popleft()
        if x == goal or y == goal:
            print("Solution found:")
            for i, (rule, (x, y)) in enumerate(path):
                print(f"Step {i+1}: Apply rule {rule}")
                print(f"({x}, {y})")
            return
        rules = [
            ("1: Fill jug1", (jug1, y)),
            ("2: Fill jug2", (x, jug2)),
            ("3: Empty jug1", (0, y)),
            ("4: Empty jug2 gallon ", (x, 0)),
            ("Pour jug1 into jug2", (max(0, x - (jug2 - y)), min(jug2, y + x))),
            ("Pour jug2 into jug1", (min(jug1, x + y), max(0, y - (jug1 - x)))),
            ("Pour jug1 into jug2 until jug1 is empty", (0, y + x)),
            ("Pour jug2 into jug1 until jug2 is empty", (x + y, 0))]
        for rule, next_state in rules:
            if next_state not in visited:
                queue.append((next_state[0], next_state[1], path + [(rule, next_state)]))
                visited.add(next_state)
    print("No solution found.")
def main():
    jug1 = int(input("Enter the capacity of jug1: ")) # 4 liters
    jug2 = int(input("Enter the capacity of jug2: ")) # 5 liters
    goal = int(input("Enter the target amount: "))    # 2 liters
    water_jug(jug1, jug2, goal)
if __name__ == "__main__":
    main()