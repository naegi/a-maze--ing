import sys
import logging
import yaml


class Logs():
    """
    A class that helps to manage logging more easily
    It will read logs.yaml and will create a logger according to this
    look in logs.yaml for an exemple.

    Only the get_logger should be used.
    """
    default_format = '%(levelname)s - %(name)s - %(message)s'
    default_level = "DEBUG"
    default_params = {
        "name": "",
        "level": default_level,
        "format": default_format,
        "handlers": {
            "main_stdout": {
                "type": "stream",
                "format": default_format,
                "output": "stdout",
                "level": default_level
            }
        },
        "childs": {}
    }

    def __init__(self, param_filename='logs.yaml'):
        self._param_filename = param_filename
        self._params_data = None
        self._logger = None
        self._root_logger_ = None

    @property
    def _params(self):
        if self._params_data is None:
            self._params_data = self.default_params.copy()

            with open(self._param_filename) as f:
                self._params_data.update(yaml.safe_load(f))

        return self._params_data

    @property
    def _root_logger(self):
        if self._root_logger_ is None:
            self._root_logger_ = self._make_logger()
        return self._root_logger_

    def _make_logger(self):
        """
        Create the base logger, according to the params.
        Here, we deal with:
            - The name of the root logger (name of project...)
              (Cf. name in YAML)
            - The level of verbosity of the root
              (will affect every child) (level in Y.)
            - The differents handlers (handlers in Y.)
              handlers is a dict, keys are not used

              values in common for each handler:
                  - activate (If False, disable the handler)
                  - format (Cf python logging's doc about Formatter)
                  - level (level of verbosity)
                  - output
                  - type (cf after)
              Type can be:
                  - file (a... file)
                  - stream (a stream)
              File:
                  logs will be written to output
              Stream:
                  Should be stdout/stderr
        """
        params = self._params

        logger = logging.getLogger(params["name"])
        logger.setLevel(params["level"].upper())

        for handler in params["handlers"].values():
            if not handler.get("activate", True):
                continue

            format = handler.get("format", self._params_data["format"])
            output = handler.get("output")
            level = handler.get("level", self._params_data["level"]).upper()

            formatter = logging.Formatter(format)

            if handler.get("type", "") == "file":
                h = logging.FileHandler(output)

            if handler.get("type", "") == "stream":
                if output == "stdout":
                    output = sys.stdout
                elif output == "stderr":
                    output = sys.stderr
                else:
                    output = None

                h = logging.StreamHandler(output)

            h.setLevel(level)
            h.setFormatter(formatter)
            logger.addHandler(h)

        return logger

    def get_logger(self, name):
        """
        Get a subloggger
        This should be the sole called function of this module

        If name is specified in childs section of the YAML, it will apply
          verbosity level as specified
        """
        logger = self._root_logger.getChild(name)

        child_param = self._params["childs"].get(name, {})
        level = child_param.get("level", self._params_data["level"]).upper()
        logger.setLevel(level)
        return logger


logs = Logs()
