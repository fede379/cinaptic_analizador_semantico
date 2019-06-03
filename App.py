from daemonize import Daemonize
from cinaptic.cinaptic.api.library.semantic.GraphBuilder import GraphBuilder 
from cinaptic.cinaptic.api.library.semantic.Config import Config
pid = "/tmp/test.pid"

class App:
    def run(self):
        config = Config().getParameters()
        builder = GraphBuilder()
        builder.build(config)
        # print(config)

def main():
    app = App()
    app.run()

daemon = Daemonize(app="cinaptic", pid=pid, action=main)
daemon.start()


# app = App()
# app.run()

