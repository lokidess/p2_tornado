from tornado import web, ioloop

from app import Index, Delete, TodoUpdate


def make_app():
    return web.Application([
        (r'/', Index),
        (r'/delete-todo/', Delete),
        (r'/todo-update/', TodoUpdate)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
