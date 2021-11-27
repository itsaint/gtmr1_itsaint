'''
scheduler module is the System
To query vacant meeting rooms and book rooms to schedule meetings
It loads the system details from config.json
Usage:
as cli:
python -m msl.scheduler path-to-config.json
'''
import sys
import json
from os import path
from typing import NamedTuple, List, Iterable, Tuple, Type, TypeVar
from dataclasses import dataclass, field, InitVar


class SlotNotFreeException(Exception):
    pass


@dataclass(order=True, frozen=True)
class Time():
    time_str: str = field(compare=True)
    # valid_interval_mins: InitVar[int] = field(default=1)

    def __post_init__(self):
        try:
            h, m = map(int, self.time_str.split(":"))
        except Exception:
            raise ValueError(f"Time {self.time_str} must be a valid Time string within 00:00 to 23:59")
        if not (0 <= h < 24) or not (0 <= m < 60):
            raise ValueError(f"Time {self.time_str} must be a valid Time string within 00:00 to 23:59")
        if (m % Scheduler.VALID_INTERVAL):
            raise ValueError(f'{self.time_str} Invalid. Time should be a \
        multiple of {Scheduler.VALID_INTERVAL} minutes')
        object.__setattr__(self, "time_str", f"{h:02d}:{m:02d}")

    def __str__(self):
        return self.time_str


@dataclass(order=True)
class TimePeriod:
    start: Time = field(compare=True)
    end: Time = field(compare=True)

    def __post_init__(self):
        if not (isinstance(self.start,Time) and isinstance(self.start,Time)):
            raise TypeError(f"Parameters must be of type scheduler.Time")
        if self.start >= self.end:
            raise ValueError(f"{self.start!s} must be before {self.end!s}")

    def overlaps(self, other) -> bool:
        if not (isinstance(other, TimePeriod)):
            raise TypeError(f"{other} must be of type TimePeriod")
        return not (self.end <= other.start or self.start >= other.end)

    def __str__(self):
        return f'{self.start!s}-{self.end!s}'


@dataclass(order=True)
class Room:
    name: str = field(compare=False)
    capacity: int = field(compare=True)

    def __str__(self):
        return f"{self.name}: {self.capacity}"

@dataclass()
class Meeting:
    room: Room
    slot: TimePeriod


class Scheduler:
    VALID_INTERVAL = 1
    def __init__(self, rooms:List[Room],
                 already_booked_meetings: List[Meeting] = [],
                 buffer:List[TimePeriod] = [],
                 valid_interval=1):
        self.rooms = sorted(rooms)
        self.meetings = already_booked_meetings
        self.buffer = sorted(buffer)
        Scheduler.VALID_INTERVAL = valid_interval
        # global VALID_INTERVAL

    def _vacancy(self, period: TimePeriod, people: int=1) -> List[Room] :
        available_rooms = []
        if any(period.overlaps(buffer_break) for buffer_break in self.buffer):
            # raise SlotNotFreeException(f'{period!s} clashes with cleaning hours{", ".join(map(str,self.buffer))}')
            return []
        for room in self.rooms:
            # ignore this room if it's capacity is not enough for these many people
            if room.capacity < people:
                continue

            if not any((period.overlaps(meet.slot)
                       and (room == meet.room))
                       for meet in self.meetings):
                available_rooms.append(room)

        return available_rooms

    def vacancy(self,start: str, end: str,) -> str:
        period = TimePeriod(Time(start), Time(end))
        vacant_rooms = self._vacancy(period)
        return " ".join([r.name for r in vacant_rooms])

    def book(self, start: str, end: str, people: int) -> str:
        period = TimePeriod(Time(start), Time(end))
        vacant_rooms = self._vacancy(period,people)
        if(len(vacant_rooms) > 0):
            meeting = Meeting(room=vacant_rooms[0], slot=period)
            self.meetings.append(meeting)
            return vacant_rooms[0].name

        return ""


def getInstanceFromJSON(json_config) -> Scheduler:
    rooms= [Room(k,v) for (k,v) in json_config.get("rooms",{}).items() ]
    buffers = [TimePeriod(Time(s), Time(e))
               for (s, e) in json_config.get("buffer",[])]
    valid_interval = int(json_config.get("valid interval",1))
    return Scheduler(rooms,buffer=buffers,valid_interval=valid_interval)


def main(config_file_path):
    if not(path.exists(config_file_path)):
        print(f"File not found {config_file_path}")
        print("Usage: python -m msl.scheduler path-to-config.json")
        print("Example config file structure:")
        json_config_str = '''
        {   "valid interval": 15,
        
            "rooms" : {"C-Cave": 3,
                     "D-Tower": 7,
                     "G-Mansion":20},
            "buffer" : [["09:00","09:15"],
                      ["13:15","13:45"],
                      ["18:45","19:00"]],
            "meetings":[]
        }
        '''
        print(json_config_str)
        exit()

    schduler_app = None
    with open(config_file_path) as f:
        scheduler_app  = getInstanceFromJSON(json.load(f))

    print("Welcome to MSL ")
    print("Meeting Rooms and capacity: "+(", ".join(map(str,scheduler_app.rooms))))
    print("Maintenance hours: "+(", ".join(map(str,scheduler_app.buffer))))
    print(f"VALID INTERVAL : {scheduler_app.VALID_INTERVAL}")
    counter = 0
    while True:
        inp = input("[v]acancy, [b]ook, [e]xit: ")
        if(inp == "v"):
            s = input("start time : ")
            e = input("end time : ")
            print(scheduler_app.vacant(TimePeriod(Time(s),Time(e))))

        elif(inp == "b"):
            s = input("start time : ")
            e = input("end time : ")
            no_people = int(input("number of people : "))
            room = scheduler_app.book(TimePeriod(Time(s),Time(e)), no_people)
            if(room):
                print(f"successfully booked room for {no_people} people in {room}")
            else:
                print("no vacant room")
        elif(inp == "e"):
            print("bye")
            break
        else:
            continue



    # schduler_app


if __name__ == "__main__":
    main(sys.argv[1])