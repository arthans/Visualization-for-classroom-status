import datetime
import json
import pickle
import threading

import requests
from requests.cookies import RequestsCookieJar

isOnline = True


class FreeClassroom():
    def __init__(self):
        self.__cookie = RequestsCookieJar()
        self.__lock = threading.RLock()
        self.__date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.classData = [[0 for i in range(13)] for i in range(4)]
        self.refresh()

    def __remoteFreeClassroom(self, startDate, lesson):
        url = 'http://dean.tuoqie.com/Office/classroom/queryCanUseClassroom.do'
        postData = {
            'school_area_code': '3EE3490E29BCC4AA',  # 犀浦校区
            'set_term_id': '1CFDF221C84E52F5',
            'class_begin': '2018-09-03 00:00:00.0',
            'SetWeek': 'Date',
            'StartDate': startDate,  # 日期
            'Lesson': str(lesson) + '-' + str(lesson),  # 时间
            'building': '1号楼',
            'floor': '--忽略--',
            'room_type': '多媒体',  # 普通
            'room_name': '--忽略--',
            'use_type': '3'
        }
        remoteResponse = requests.post(
            url, data=postData, cookies=self.__cookie)
        try:
            freeClassroomInfo = json.loads(remoteResponse.text)
        except:
            print("加载教务数据失败！")
            return {}
        return freeClassroomInfo

    def __loadRemoteFreeClassroom(self, day, lesson):
        startDate = (datetime.datetime.now() +
                     datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        freeClassroomInfo = self.__remoteFreeClassroom(startDate, lesson)
        self.__lock.acquire()
        self.classData[day][lesson - 1] = freeClassroomInfo
        self.__lock.release()
        print("{0} 第{1}讲课".format(startDate, lesson))

    def __refreshCookie(self):
        url = 'http://dean.tuoqie.com/Office/LoginController/initGeetest.do'
        remoteResponse = requests.get(url)
        cookie = remoteResponse.cookies.get('JSESSIONID')
        self.__cookie.set('JSESSIONID', cookie)

    def refresh(self):
        if isOnline:
            self.__refreshCookie()
            for day in range(4):
                thread_list = []
                for lesson in range(1, 14):
                    t = threading.Thread(
                        target=self.__loadRemoteFreeClassroom, args=(day, lesson,))
                    thread_list.append(t)
                for t in thread_list:
                    t.start()
                for t in thread_list:
                    t.join()
            timer = threading.Timer(30 * 60, self.refresh)
            timer.start()
            with open('G:\\Visualization-for-classroom-status\\app\\nginx\\html\\classData.pk', 'wb') as f:
                pickle.dump(self.classData, f)
        else:
            with open('G:\\Visualization-for-classroom-status\\app\\nginx\\html\\classData.pk', 'rb') as f:
                self.classData = pickle.load(f)

    def getFreeClassroom(self, date, lesson):
        day = (datetime.datetime.strptime(date, '%Y-%m-%d') -
               datetime.datetime.strptime(self.__date, '%Y-%m-%d')).days
        return self.classData[day][lesson - 1]
