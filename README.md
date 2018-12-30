# Visualization-for-classroom-status

* [项目需求规格说明书](./项目需求规格说明书.md)  
* [项目总体设计报告](./项目总体设计报告.md)  

安装说明：
1. 安装 [nginx](http://nginx.org/)
2. 将 nginx 的根目录指向 html
2. 向 nginx 的配置文件中加入如下代码：
    ```
    location = /Office/LoginController/initGeetest.do {
        proxy_pass  http://127.0.0.1:5000/Office/LoginController/initGeetest.do;
    }
    location = /Office/LoginController/login.do {
        proxy_pass  http://127.0.0.1:5000/Office/LoginController/login.do;
    }
    location = /Office/LoginController/queryCanUseClassroom.do {
        proxy_pass  http://127.0.0.1:5000/Office/LoginController/queryCanUseClassroom.do;
    }
    location = /Office/LoginController/lightPosition.do {
        proxy_pass  http://127.0.0.1:5000/Office/LoginController/lightPosition.do;
    }  
    ```
1. 启动 nginx
3. 启动 .\app\nginx\python\web.py
4. 打开 [登录页面](http://127.0.0.1/Office/LoginController/newLogin.htm)