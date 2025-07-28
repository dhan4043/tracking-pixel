from flask import Flask, send_file, request, render_template_string
import datetime
import urllib.request

app = Flask(__name__)

@app.route('/image')
def tracking_pixel():
    # File path and name for 1 x 1 pixel. Must be an absolute path to pixel
    filename = './static/img/pixel.png'
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')
    get_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Lookup Geolocation of IP Address
    with urllib.request.urlopen('http://ip-api.com/json/'+ get_ip) as url:
        data = url.read().decode()

    # Add User-Agent, Timestamp, and IP Address + Geolocation information to dictionary
    log_entry = f'Website Opened:\nTimestamp: {timestamp}\nUser Agent: {user_agent}\nIP Address Data: {data}\n'

    # Write log to hardcoded path. Must be an absolute path to the log file
    with open('./logs.txt', 'w') as file:
        file.write(log_entry)
    print(log_entry)

    # Serve a transparent pixel image when navigating to .../image URL. "image/png" displays the image in PNG format
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run()
