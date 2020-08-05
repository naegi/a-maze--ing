import collections

from logs import logs


logger = logs.get_logger(__name__)

class EventDispatcher:
    def __init__(self):
        self.fifo = collections.deque()
        self.registrations = collections.defaultdict(set)

    def register(self, event_type, f):
        logger.debug("Registering callback {} for event \"{}\"".format(str(f), event_type))
        self.registrations[event_type].add(f)

    def unregister(self):
        raise NotImplementedError

    def add_event(self, event_type, *args, **kwargs):
        self.fifo.append((event_type, args, kwargs))

    def dispatch(self):
        fifo = self.fifo
        self.fifo = collections.deque()
        try:
            while event := fifo.popleft():
                for callback in self.registrations[event[0]]:
                    callback(*event[1], **event[2])
        except IndexError:
            pass



