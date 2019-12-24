import urllib
from tornado import web, websocket, ioloop
from sqlalchemy.orm import sessionmaker
from tornado.websocket import WebSocketClosedError

from db import engine
from models import Todo


class Index(web.RequestHandler):

    def get(self):
        session = sessionmaker(bind=engine)()
        context = {
            'todos': session.query(Todo).all(),
            'error': None,
            'priority_choices': range(1, 6)
        }
        self.render('templates/index.html', **context)

    def post(self):
        session = sessionmaker(bind=engine)()
        session.add(Todo(
            name=self.get_body_argument('todo-text'),
            priority=int(self.get_body_argument('priority')),
        ))
        session.commit()
        todos = session.query(Todo).all()
        # тут собственно и происходит отправка по сокету
        # в качестве сообщения я отправляю срендеренный
        # файлик в виде строки, в файлике просто html для списка todo
        TodoUpdate.send_message(
            self.render_string('templates/todo_list.html', **{'todos': todos})
        )
        context = {
            'todos': todos,
            'error': None,
            'priority_choices': range(1, 6)
        }
        self.render('templates/index.html', **context)


class Delete(web.RequestHandler):

    def post(self):
        session = sessionmaker(bind=engine)()
        todo = session.query(Todo).filter_by(
            id=int(self.get_body_argument('id'))
        ).first()
        session.delete(todo)
        session.commit()
        todos = session.query(Todo).all()
        # тут собственно и происходит отправка по сокету
        # в качестве сообщения я отправляю срендеренный
        # файлик в виде строки, в файлике просто html для списка todo
        TodoUpdate.send_message(
            self.render_string('templates/todo_list.html', **{'todos': todos})
        )
        self.redirect('/')


class TodoUpdate(websocket.WebSocketHandler):
    clients = []

    def open(self, *args: str, **kwargs: str):
        TodoUpdate.clients.append(self)
        super(TodoUpdate, self).open(*args, **kwargs)

    def close(self, code=None, reason=None):
        TodoUpdate.clients.remove(self)

    @classmethod
    def send_message(cls, message):
        for client in cls.clients:
            # тупо try не хватало :(
            try:
                client.write_message(message)
            except WebSocketClosedError:
                pass
