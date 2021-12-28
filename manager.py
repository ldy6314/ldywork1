from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import create_app


def main():
    http_sever = HTTPServer(WSGIContainer(create_app('production')))
    http_sever.listen(5050)
    print("start serving")
    IOLoop.current().start()


if __name__ == '__main__':
    main()