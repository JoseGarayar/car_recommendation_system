# App
import sys
from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # If there are command-line arguments, run the custom commands
        from flask.cli import main
        main()
    else:
        # If no command-line arguments, run the app
        app.run(port = 5000, host='0.0.0.0')