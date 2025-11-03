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

    default_rooms = ["1", "2", "3", "4", "5"]
    default_students = [
        "Aashish markam", "Deepankar", "Neeraj", "Lekesh", "Vivek", "Dilip sori",
        "Sudeshswor", "Goverdhan", "Balkrishna", "Bhagat", "Imran", "Mohan",
        "Rahul", "Sagar bhaskar", "Harshit", "Vinod", "Sabindar", "Dev Aashish",
        "Laxman", "Mahadev", "Sagar Kumar", "Umesh", "Manoj mandavi", "Gango",
        "Sushil", "Ashok", "Badal", "Aashish Kashyap", "Karthik kaka", "Deepak Thakur",
        "Narendra", "Geetesh", "Parveen", "Harsh borla", "Bheemsen", "Dhurwa",
        "Himanshu", "Ramlal", "Sukhlal", "Vikash", "Vikky", "Yash"
    ]

    # Handle flexible data.json structure
    if isinstance(data, dict):
        rooms = ensure_list(data.get("rooms") or data.get("room") or data.get("Rooms"), default_rooms)
        students = ensure_list(
            data.get("students") or data.get("Students") or data.get("students_list"),
            default_students,
        )
    elif isinstance(data, list):
        rooms = default_rooms
        students = data
    else:
        rooms = default_rooms
        students = default_students

    if not rooms:
        rooms = default_rooms
    if not students:
        students = default_students

    # Shuffle both rooms and students
    random.shuffle(rooms)
    random.shuffle(students)

    # Initialize room assignments
    room_assignments: Dict[str, List[str]] = {str(r): [] for r in rooms}

    # Calculate base distribution
    total_students = len(students)
    total_rooms = len(rooms)
    base_count = total_students // total_rooms
    extra = total_students % total_rooms

    # Assign students evenly, ensuring no room has > 10 students
    index = 0
    for i, room in enumerate(rooms):
        count = base_count + (1 if i < extra else 0)
        count = min(count, 10)
        room_assignments[str(room)] = students[index:index + count]
        index += count

    # If some students remain unassigned due to 10-student limit, assign randomly within limit
    remaining = students[index:]
    for student in remaining:
        available_rooms = [r for r, s in room_assignments.items() if len(s) < 10]
        if not available_rooms:
            print("⚠️ All rooms full (10 max). Some students unassigned.")
            break
        random_room = random.choice(available_rooms)
        room_assignments[random_room].append(student)

    # Save to result.json
    try:
        with open("result.json", "w", encoding="utf-8") as outfile:
            json.dump(room_assignments, outfile, indent=4, ensure_ascii=False)
        print("✅ Random room assignments saved in result.json")
    except Exception as e:
        print(f"Error writing result.json: {e}")


if __name__ == "__main__":
    main()
