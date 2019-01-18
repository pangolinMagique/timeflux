"""timeflux.core.manager: manage workers"""

import logging
import json
import yaml
from timeflux.core.worker import Worker

class Manager:

    """Load configuration and spawn workers."""

    def __init__(self, config):
        """
        Load configuration

        Parameters
        ----------
        config : str|dict
            The configuration can either be a path to a YAML or JSON file, a JSON string or a dict.

        """

        # Load config
        if isinstance(config, dict):
            self.config = config
        elif isinstance(config, str):
            extension = config.split('.')[-1]
            if extension in ('yml', 'yaml'):
                self.config = self._load_yaml(config)
            elif extension == 'json':
                self.config = self._load_json(config)
            else:
                self.config = json.loads(config)
        else:
            raise ValueError('Could not load config.')
        if not self._validate():
            raise ValueError('Invalid config.')

    def run(self):
        """Span as many workers as there are graphs."""
        for graph in self.config['graphs']:
            worker = Worker(graph)
            pid = worker.run()
            logging.debug("Worker spawned with PID %d", pid)

    def _load_yaml(self, filename):
        with open(filename) as stream:
            return yaml.load(stream)

    def _load_json(self, filename):
        with open(filename) as stream:
            return json.load(stream)

    def _validate(self):
        # TODO
        return True