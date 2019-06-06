#!/usr/bin/env python3
from cinaptic.cinaptic.api.library.semantic.GraphBuilder import GraphBuilder 
from cinaptic.cinaptic.api.library.semantic.Config import Config

class App:
    def run(self):
        config = Config().getParameters()
        builder = GraphBuilder()
        builder.build(config)

app = App()
app.run()