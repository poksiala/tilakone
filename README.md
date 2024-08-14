# Tilakone

Super simple state machine

```PYTHON
from tilakone import StateChart, StateMachine
from typing import Literal

States = Literal["ON", "OFF"]
Events = Literal["toggle", "turn_off"]

state_chart = StateChart[States, Events]({
    "OFF": {
        "initial": True,
        "on": {
            "toggle": "ON"
        }
    },
    "ON": {
        "initial": False,
        "on": {
            "toggle": "OFF",
            "turn_off": "OFF"
        }
    }
})

machine = StateMachine(state_chart)
assert machine.current_state == "OFF"

transitioned = machine.send("toggle")
assert transitioned == True
assert machine.current_state == "ON"

transitioned = machine.send("turn_off")
assert transitioned == True
assert machine.current_state == "OFF"

# Irrelevant events are ignored
transitioned = machine.send("turn_off")
assert transitioned == False
assert machine.current_state == "OFF"

```