from daemonize import Daemonize
from cinaptic.cinaptic.api.library.semantic.GraphBuilder import GraphBuilder
from cinaptic.cinaptic.api.library.semantic.Config import Config
import logging

pid = "/tmp/cinapticApp.pid"

# logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler("app.log", "w")
fh.setLevel(logging.INFO)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


class App2:
    def run(self):
        config = Config().getParameters()
        builder = GraphBuilder()
        builder.build(config)
        # print(config)


def main():
    app = App2()
    app.run()

daemon = Daemonize(app="cinaptic", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()


# app = App2()
# app.run()
