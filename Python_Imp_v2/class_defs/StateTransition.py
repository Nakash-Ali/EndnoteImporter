# This class is used to represent the state transitions from one class to another
# Objects of this class are owned by the source state and destination state is part of the object
# A transition only takes place if the input matches the transition string


class StateTransition:
    def __init__(self, str, dest_state):
        self.transition_string = str
        self.dest_state = dest_state
