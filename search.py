#!/usr/bin/python
# -*- coding: utf-8 -*-
print("module [app] loaded")
import os

from backend_search import app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6050))
    #app.run("0.0.0.0", debug=False, port=port, threaded=False)
    app.run("0.0.0.0", debug=False, port=port, threaded=True)