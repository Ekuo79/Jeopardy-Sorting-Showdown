from website import create_app
import csv
from flask import session

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


