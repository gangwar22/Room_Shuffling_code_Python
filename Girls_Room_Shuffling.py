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

    default_rooms = [
        "1","3","5","6","7","8","9","10","11","12","13","14","31","32","33","34",
        "37","38","39","40","41","42","43","44","45","46","48","55","56","57","58",
        "59","60","61","62","63","64","65","66","67","68","69","70","71","72","73",
        "74","75","76","77","78","79","80","81"
    ]

    default_students = [
        "Aanchal sahu","Akanksha Dewangan","Anjali Morla","Indu nayak","Anju sori","Ankita nag",
        "Asha jagat","Asmati Markam","Avantika Lambadi","Damini Kunjam","Deepa Sodi","Divya nag",
        "Divya sunarkar","Gungun Goswami","Prerna Atami","Jyoti Karmkar",
        "Kamini Sethiya","Kasak raut","Roochi Patel","Komal baghel",
        "Lachhan Rana","Bharti vishwakarama","Neetu kuldeep","Neetu Mandavi","Deepika Bhanjdev","Priyanka baghel","Nirmla Thakur",
        "Shivani Yadav","Pratibha Mark dayalu","Kunti Pandey","Shushmita Totapalli","Sanjna Neelam","Shivani Kashyap",
        "Sumita Yadav","Shraddha sahu","Sanjana Kawasi","Savesh Pradhan","Vaishali Acharya",
        "Roshni Netam","Nikita Telam","Rita Mudami","Salita Lekami","Sakshi Nagesh",
       "Subati Mandavi","Bindiya Korram","Kumli Kashyap","Jyoti Bhvani","Aarti Chand"
    ]

    # Load custom data if exists
    if isinstance(data, dict):
        rooms = ensure_list(data.get("rooms") or data.get("room") or data.get("Rooms"), default_rooms)
        students = ensure_list(data.get("students") or data.get("Students") or data.get("students_list"), default_students)
    else:
        rooms = default_rooms
        students = default_students

    # Fixed room assignments
    fixed_assignments = {
        "11": ["Rudra"],
        "10": ["Gungun Goswami"],
        "38": ["Kamini Sethiya"],
        "72":["Subati Mandavi" ],
        "40":["Joti Bhvani"],
        "75":["Aanchal sahu", "Prathibha Mark dayalu"],
        "46" : ["sushmita Totapalli", "anju sori"],
        "8": ["Divya sunarkar"],
        "9":["indu nayak"],
        "75": ["Sanjna Neelam", "Shivani Yadav"],
        "76":["Avantika Lambadi"],
        "69":["Asmati Markam", "sumita Yadav"],
        "32":["artichand", "ankita nag"],
        "31":["Anjali Morla"],
        "77":["Sakshi Nagesh"],
        "6":["sanjana Neelam"],
        "42":["Bindya Korram", "savesh Pradhan"],
         
    }

    # Remove fixed students from random pool
    fixed_students = {s for sl in fixed_assignments.values() for s in sl}
    remaining_students = [s for s in students if s not in fixed_students]

    # Remove fixed rooms from random pool
    remaining_rooms = [r for r in rooms if r not in fixed_assignments.keys()]

    # Shuffle remaining rooms and students
    random.shuffle(remaining_rooms)
    random.shuffle(remaining_students)

    # Initialize result
    room_assignments: Dict[str, List[str]] = dict(fixed_assignments)

    # Fill fixed rooms (1-person ones) to 2-person max
    for room, assigned in list(room_assignments.items()):
        if len(assigned) < 2 and remaining_students:
            room_assignments[room].append(remaining_students.pop(0))

    # Assign remaining rooms with 2 students each
    index = 0
    for room in remaining_rooms:
        if index + 2 <= len(remaining_students):
            room_assignments[room] = [remaining_students[index], remaining_students[index + 1]]
            index += 2
        else:
            break

    # Save to JSON
    with open("result.json", "w", encoding="utf-8") as outfile:
        json.dump(room_assignments, outfile, indent=4, ensure_ascii=False)

    print("✅ Room assignments (2 per room, fixed rooms filled automatically) saved in result.json")


if __name__ == "__main__":
    main()
