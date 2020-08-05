import time

from logs import logs

logger = logs.get_logger(__name__)


def repeat(event_dispatcher, name, delta, f, *args, **kwargs):
    name_repeat = name + "_repeat"

    def fct():
        t = time.time()
        if t - fct.last_time > delta:
            fct.last_time = t
            event_dispatcher.add_event(name, *args, **kwargs)
        event_dispatcher.add_event(name_repeat)

    fct.last_time = time.time()


    event_dispatcher.register(name, f)
    event_dispatcher.register(name_repeat, fct)
    event_dispatcher.add_event(name_repeat)
