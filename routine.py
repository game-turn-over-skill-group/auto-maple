"""A collection of classes used in the 'machine code' generated by Auto Maple's compiler for each routine."""

import config
import utils


def _update(func):
    """Decorator function that updates CONFIG.ROUTINE_VAR for all mutative Routine operations."""

    def f(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        display = []
        for e in self.sequence:
            if isinstance(e, str):
                display.append(e + ':')
            elif isinstance(e, Point):
                display.append(str(e))
        config.routine_var.set(display)
        return result
    return f


class Routine:
    """Describes a routine file in Auto Maple's custom 'machine code'."""

    def __init__(self):
        self.path = ''
        self.sequence = []

    @_update
    def set(self, arr):
        self.sequence = arr

    @_update
    def append(self, p):
        self.sequence.append(p)

    def index(self, item):
        return self.sequence.index(item)

    def __getitem__(self, i):
        if i < 0 or i >= len(self):
            raise IndexError
        return self.sequence[i]

    def __len__(self):
        return len(self.sequence)


class Point:
    """Represents a location in a user-defined routine."""

    def __init__(self, x, y, frequency=1, counter=0, adjust='False'):
        self.location = (float(x), float(y))
        self.frequency = utils.validate_nonzero_int(frequency)
        self.counter = int(counter)
        self.adjust = utils.validate_boolean(adjust)
        self.commands = []

    @utils.run_if_enabled
    def execute(self):
        """
        Executes the set of actions associated with this Point.
        :return:    None
        """

        if self.counter == 0:
            move = config.command_book.get('move')
            move(*self.location).execute()
            if self.adjust:
                adjust = config.command_book.get('adjust')
                adjust(*self.location).execute()
            for command in self.commands:
                command.execute()
        self._increment_counter()

    @utils.run_if_enabled
    def _increment_counter(self):
        """
        Increments this Point's counter, wrapping back to 0 at the upper bound.
        :return:    None
        """

        self.counter = (self.counter + 1) % self.frequency

    def __str__(self):
        """
        Returns a string representation of this Point object.
        :return:    This Point's string representation.
        """

        return f'  * {self.location}'
