from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class StartState(State):
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)


class TerminationState(State):
    def __init__(self) -> None:
        self.next_states = []
        super().__init__()

    def check_self(self, char: str) -> bool:
        return False



class DotState(State):
    """
    state for . character (any character accepted)
    """

    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char: str):
        return True


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

    next_states: list[State] = []
    curr_sym = ""

    def __init__(self, symbol: str) -> None:
        self.next_states = []
        self.curr_sym = symbol
        super().__init__()

    def check_self(self, curr_char: str) -> State | Exception:
        return curr_char == self.curr_sym


class StarState(State):

    next_states: list[State] = []

    def __init__(self, checking_state: State):
        self.next_states = [checking_state]

    def check_self(self, char):
        for state in self.next_states:
            if state.check_self(char):
                return True

        return False


class PlusState(State):
    next_states: list[State] = []

    def __init__(self, checking_state: State):
        self.next_states = [checking_state]

    def check_self(self, char):
        for state in self.next_states:
            if state.check_self(char):
                return True
        return False


class RegexFSM:
    curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:

        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        for char in regex_expr:
            tmp_next_state = self.__init_next_state(char, prev_state, tmp_next_state)
            prev_state.next_states.append(tmp_next_state)

    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()
            case next_token if next_token == "*":
                if prev_state.next_states:
                    prev_state.next_states.pop()
                new_state = StarState(tmp_next_state)

            case next_token if next_token == "+":
                if prev_state.next_states:
                    prev_state.next_states.pop()
                new_state = PlusState(tmp_next_state)

            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)

            case _:
                raise AttributeError("Character is not supported")

        return new_state

    def check_string(self, string: str):
        states = self.curr_state.next_states

        def dfs(state_idx: int, str_idx: int):
            if state_idx == len(states):
                return str_idx == len(string)
            state = states[state_idx]
            if isinstance(state, StarState):
                if dfs(state_idx + 1, str_idx):
                    return True
                curr_str_idx = str_idx
                while curr_str_idx < len(string) and state.check_self(string[curr_str_idx]):
                    curr_str_idx += 1
                    if dfs(state_idx + 1, curr_str_idx):
                        return True
                return False

            elif isinstance(state, PlusState):
                curr_str_idx = str_idx
                while curr_str_idx < len(string) and state.check_self(string[curr_str_idx]):
                    curr_str_idx += 1
                    if dfs(state_idx + 1, curr_str_idx):
                        return True
                return False
            else:
                if str_idx < len(string) and state.check_self(string[str_idx]):
                    return dfs(state_idx + 1, str_idx + 1)
                return False
        return dfs(0, 0)


if __name__ == "__main__":
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False
