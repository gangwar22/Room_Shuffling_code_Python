import os
import random
import json
from typing import Any, Dict, List


def load_data(path: str = "data.json") -> Any:
    """Try to load JSON from path. Return raw data or None if not found/invalid."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: failed to load {path}: {e}")
        return None


def ensure_list(value: Any, fallback: List[Any]) -> List[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [s.strip() for s in value.split(",") if s.strip()]
    try:
        return list(value)
    except Exception:
        return fallback


def main():
    data = load_data()
    # Try to load previous assignments from result.json to use as constraints
    previous_assignments = load_data("result.json") or {}

    # Provided hardcoded initial assignments (used only if result.json is missing)
    default_previous = {
        "1": ["Aashish markam", "Rahul", "Sagar Kumar", "Mohan", "Laxman", "Sagar bhaskar"],
        "2": ["sanath ram", "Lekesh", "Deepankar", "Narendra", "Deepak", "Geetesh", "Devashish"],
        "3": ["Vikky", "Balkrishna", "Sushil", "Yash", "Bheemsen"],
        "4": ["Ashok", "Himanshu", "Vivek", "Ramlal"],
        "5": ["Dilip", "RoopSingh", "Sukhlal", "Sudeshwar", "Kartik kaka"]
    }

    # Use result.json if it exists, otherwise use the default provided list
    constraints = previous_assignments if previous_assignments else default_previous

    # Flatten the list of students for shuffling
    students = []
    for room_students in constraints.values():
        students.extend(room_students)

    rooms = ["1", "2", "3", "4", "5"]

    # Shuffle until no student is in their original room
    max_attempts = 1000
    for attempt in range(max_attempts):
        random.shuffle(students)
        temp_assignments = {str(r): [] for r in rooms}
        
        # Calculate distribution
        total_students = len(students)
        total_rooms = len(rooms)
        base_count = total_students // total_rooms
        extra = total_students % total_rooms

        index = 0
        valid_shuffle = True
        for i, room in enumerate(rooms):
            count = base_count + (1 if i < extra else 0)
            assigned_to_room = students[index:index + count]
            
            # Constraint: No student should be in the same room as in 'constraints' (result.json)
            original_room_students = constraints.get(str(room), [])
            if any(s in original_room_students for s in assigned_to_room):
                valid_shuffle = False
                break
                
            temp_assignments[str(room)] = assigned_to_room
            index += count
        
        if valid_shuffle:
            room_assignments = temp_assignments
            print(f"✅ Successful shuffle found on attempt {attempt + 1}")
            break
    else:
        print("⚠️ Could not find a valid shuffle after 1000 attempts. Assigning randomly.")
        # Fallback to standard shuffle if constraint can't be met
        random.shuffle(students)
        room_assignments = {str(r): [] for r in rooms}
        index = 0
        for i, room in enumerate(rooms):
            count = base_count + (1 if i < extra else 0)
            room_assignments[str(room)] = students[index:index + count]
            index += count

    # Save to result.json
    try:
        with open("result.json", "w", encoding="utf-8") as outfile:
            json.dump(room_assignments, outfile, indent=4, ensure_ascii=False)
        print("✅ Random room assignments saved in result.json")
    except Exception as e:
        print(f"Error writing result.json: {e}")


if __name__ == "__main__":
    main()
