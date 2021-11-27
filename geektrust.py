import sys
from msl import scheduler

def main():
    input_file = sys.argv[1]
    config = {"valid interval": 15 ,
              "rooms" : {"C-Cave": 3,
                         "D-Tower": 7,
                         "G-Mansion":20},
              "buffer" : [["09:00","09:15"],
                          ["13:15","13:45"],
                          ["18:45","19:00"]],
              "meetings":[]
    }
    scheduler_app = scheduler.getInstanceFromJSON(json_config=config)
    with open(input_file) as f:
        for line in f:
            cmd = line.strip().split()
            try:
                if cmd[0].lower() == "book":
                    people = int(cmd.pop())
                    cmd.append(people)
                result = getattr(scheduler_app, cmd[0].lower())(*cmd[1:])
                print(result or "NO_VACANT_ROOM")
            except Exception as e:
                print("INCORRECT_INPUT")



if __name__ == '__main__':
    main()
