import json
import math
import requests
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from requests.cookies import RequestsCookieJar

from freeclassroom import FreeClassroom
from sunpos import sun_position

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route("/Office/LoginController/initGeetest.do", methods=['GET'])
def initGeetest():
    url = 'http://dean.tuoqie.com/Office/LoginController/initGeetest.do'
    remoteResponse = requests.get(url)
    cookie = remoteResponse.cookies.get('JSESSIONID')
    localResponse = make_response(remoteResponse.text)
    localResponse.set_cookie('JSESSIONID', cookie)
    print('cookie: {0}, response: {1}'.format(cookie, remoteResponse.text))
    return localResponse


@app.route("/Office/LoginController/login.do", methods=['POST'])
def login():
    cookie = request.cookies.get('JSESSIONID')
    cookie_jar = RequestsCookieJar()
    cookie_jar.set('JSESSIONID', cookie)
    url = 'http://dean.tuoqie.com/Office/LoginController/login.do'
    postData = {
        'username': request.form['username'],
        'password': request.form['password'],
        'geetest_challenge': request.form['geetest_challenge'],
        'geetest_validate': request.form['geetest_validate'],
        'geetest_seccode': request.form['geetest_seccode']
    }
    remoteResponse = requests.post(url, data=postData, cookies=cookie_jar)
    print('cookie: {0}, username: {1}, response: {2}'.format(
        cookie, request.form['username'], remoteResponse.text))
    return remoteResponse.text


def time2Lesson(hour, minute):
    time = hour * 60 + minute
    if time < 8 * 60 + 45:
        lesson = 1
    elif time < 9 * 60 + 35:
        lesson = 2
    elif time < 10 * 60 + 35:
        lesson = 3
    elif time < 11 * 60 + 25:
        lesson = 4
    elif time < 12 * 60 + 15:
        lesson = 5
    elif time < 14 * 60 + 45:
        lesson = 6
    elif time < 15 * 60 + 35:
        lesson = 7
    elif time < 16 * 60 + 35:
        lesson = 8
    elif time < 17 * 60 + 25:
        lesson = 9
    elif time < 18 * 60 + 15:
        lesson = 10
    elif time < 20 * 60 + 15:
        lesson = 11
    elif time < 21 * 60 + 5:
        lesson = 12
    elif time < 21 * 60 + 55:
        lesson = 13
    else:
        lesson = 1
    return lesson


@app.route("/Office/LoginController/queryCanUseClassroom.do", methods=['POST'])
def queryCanUseClassroom():
    cookie = request.cookies.get('JSESSIONID')
    # if not (cookie):
    #    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    hour = int(request.form['hour'])
    minute = int(request.form['minute'])
    date = str(year) + '-' + str(month) + '-' + str(day)
    lesson = time2Lesson(hour, minute)
    rooms = freeclassroom.getFreeClassroom(date, lesson)
    freeRooms = []
    for room in rooms:
        freeRooms.append(room['room_name'])
    return jsonify(freeRooms)


@app.route("/Office/LoginController/lightPosition.do", methods=['POST'])
def lightPosition():
    cookie = request.cookies.get('JSESSIONID')
    # if not (cookie):
    #    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    hour = int(request.form['hour'])
    minute = int(request.form['minute'])
    azimuth, elevation = sun_position(year, month, day, hour, minute)
    d = 2000
    z = d * math.sin(math.radians(elevation))
    xy = d * math.cos(math.radians(elevation))
    theta = azimuth - 90 - 44.085
    x = xy * math.cos(math.radians(theta))
    y = xy * math.sin(math.radians(theta))
    return jsonify({'x': x, 'y': y, 'z': z})


if __name__ == '__main__':
    freeclassroom = FreeClassroom()
    app.run()
