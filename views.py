from flask import abort
from flask import request, jsonify, Response
from flask.views import MethodView

from app import app, db
from models import User, Announcement


class UserView(MethodView):

    def get_user(self, id_needed):
        result = []
        if id_needed is None:
            instance = db.session.query(User).all()
        else:
            instance = [db.session.query(User).get(id_needed)]

        if instance is []:
            return jsonify({'result': None})

        for elem in instance:
            result.append({
                'id': elem.id,
                'username': elem.username,
                'email': elem.email,
                'password': elem.password,
            })
        return jsonify(result)

    def post_user(self):
        new_user = User(**request.json)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'password': new_user.password,
        })


class AnnouncementView(MethodView):

    def get_announce(self, id_announce):
        result = []
        if id_announce is None:
            instance = db.session.query(Announcement).all()
        else:
            instance = [db.session.query(Announcement).get(id_announce)]

        if instance is []:
            return jsonify({'result': None})

        for elem in instance:
            result.append({
                'id': elem.id,
                'title': elem.title,
                'text': elem.text,
                'created': elem.created,
                'owner': elem.owner
            })
        return jsonify(result)

    def post_announce(self):
        announce = Announcement(**request.json)
        db.session.add(announce)
        db.session.commit()
        return jsonify({
            'id': announce.id,
            'title': announce.title,
            'text': announce.text,
            'created': announce.created,
            'owner': announce.owner
        })

    def delete_announce(self, id_announce):
        instance = db.session.query(Announcement).get(id_announce)
        if instance is None:
            return abort(Response('There is no such announcement', 404))
        db.session.query(Announcement).filter_by(id=id_announce).delete()
        db.session.commit()
        if db.session.query(Announcement).get(id_announce) is None:
            return jsonify({
                'status': 'deleted'
            })
        return jsonify({
            'status': 'Not deleted'
        })


app.add_url_rule(
    '/user/', defaults={'id_user': None}, view_func=UserView.as_view('users_get'), methods=['GET']
)
app.add_url_rule(
    '/users/', view_func=UserView.as_view('users_create'), methods=['POST']
)
app.add_url_rule(
    '/announce/', view_func=AnnouncementView.as_view('announce_create'), methods=['POST']
)
app.add_url_rule(
    '/announce/<int:id_announce>', view_func=AnnouncementView.as_view('announce_get'), methods=['GET']
)
app.add_url_rule(
    '/announce/<int:id_announce>', view_func=AnnouncementView.as_view('announce_delete'), methods=['DELETE']
)
