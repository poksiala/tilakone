from typing import Dict, Generic, TypedDict, TypeVar, NotRequired

E = TypeVar('E')
T = TypeVar('T')


class StateDict(TypedDict, Generic[T, E]):
    on: NotRequired[Dict[E, T]]
    initial: NotRequired[bool]


class StateChart(Dict[T, StateDict[T, E]], Generic[T, E]):
    pass


class StateMachine(Generic[T, E]):
    def __init__(self, states: StateChart[T, E], initial_state: T | None = None):
        self.states = states
        initial = initial_state
        if initial is not None:
            if not self._is_valid_state(initial):
                raise ValueError(f"Given initial state `{initial_state}` is not a valid state")
        else:
            for name, state in self.states.items():
                if state.get("initial"):
                    if initial is not None:
                        raise ValueError("More than one initial state defined")
                    initial = name
        if initial is None:
            raise ValueError("No initial state defined")
        self.current_state = initial
        

    def _is_valid_state(self, name: T) -> bool:
        return name in list(self.states.keys())


    def send(self, event: E) -> bool:
        # Send event to a state machine and perform transition.
        # Returns boolean that tells if transition happened or not.
        state_data = self.states[self.current_state]
        transitions = state_data.get("on")
        if transitions is None:
            return False
        next_state = transitions.get(event)
        if next_state is None:
            return False
        if not self._is_valid_state(next_state):
            raise ValueError(f"State machine tried to transition to invalid state `{next_state}` not present in state chart")
        self.current_state = next_state
        return True