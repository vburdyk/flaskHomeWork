from flask import Flask, abort
from datetime import datetime
import pytz

app = Flask(__name__)


@app.route('/datetime')
def documentation():
    return """
    <h1>Now you are on documentation route</h1>
    <p>Here you can check time in different timezones.</p> 
    <p>Example of commands:</p> 
    <ul>
    <li>'/datetime/'- it will show you current date and time in your time zone</li>
    <li>'/datetime/+2' - it will show you current date and time in GMT+2 timezone</li>
    <li>'/datetime' - shows you little documentation</li>
    </ul>
    """


@app.route('/datetime/')
def current_time():
    now = datetime.now()
    return "Current date and time: {}".format(now.strftime("%d-%m-%Y %H:%M:%S %Z%z"))


@app.route('/datetime/<int:tz>')
@app.route('/datetime/+<int:tz>')
def get_datetime(tz=0):
    try:
        timezone = pytz.timezone('Etc/GMT' + str(tz) if tz < 0 else 'Etc/GMT+' + str(tz))
    except pytz.exceptions.UnknownTimeZoneError:
        return abort(406, 'Timezone not found')

    dt = datetime.now(timezone)
    if tz == 0:
        return "Current date and time: {}".format(dt.strftime("%d-%m-%Y %H:%M:%S, now you are in Greenwich "))
    else:
        return "Current date and time: {}".format(dt.strftime("%d-%m-%Y %H:%M:%S, now you are in GMT+%Z "))


if __name__ == "__main__":
    import logging
    app.logger.setLevel(logging.DEBUG)
    app.run(host="127.0.0.1", port=5000, debug=True)