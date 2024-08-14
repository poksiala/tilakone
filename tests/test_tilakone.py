from tilakone import StateChart, StateDict, StateMachine
from typing import Literal
import pytest


States = Literal["green", "red", "yellow"]
Events = Literal["toggle", "go_red", "go_yellow"]

def get_state_chart():
    return StateChart[States, Events]({
        "green": {
            "initial": True,
            "on": {
                "toggle": "red",
                "go_red": "red",
                "go_yellow": "yellow"
            }
        },
        "red": {
            "initial": False,
            "on": {
                "toggle": "green"
            }
        }
    })

def test_simple_valid_state_machine():
    machine = StateMachine(get_state_chart())
    assert machine.current_state == "green"
    res = machine.send("toggle")
    assert res == True
    assert machine.current_state == "red"
    res = machine.send("toggle")
    assert res == True
    assert machine.current_state == "green"
    

def test_giving_initial_state():
    machine = StateMachine(get_state_chart(), "red")
    assert machine.current_state == "red"

def test_unsuitable_events_are_ignored():
    machine = StateMachine(get_state_chart(), "red")
    res = machine.send("go_yellow")
    assert res == False
    assert machine.current_state == "red"

def test_raises_on_multiple_initial_states():
    chart = get_state_chart()
    chart["red"]["initial"] = True
    with pytest.raises(ValueError):
        machine = StateMachine(chart)

def test_raises_when_no_initial_state():
    chart = get_state_chart()
    chart["green"]["initial"] = False
    with pytest.raises(ValueError):
        machine = StateMachine(chart)

def test_raises_if_tries_to_move_to_non_existen_state():
    machine = StateMachine(get_state_chart())
    with pytest.raises(ValueError):
        machine.send("go_yellow")