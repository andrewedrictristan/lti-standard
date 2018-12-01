import json
import os
from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify, Response
from pylti.flask import lti
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User
import threading

app = Flask(__name__)
engine = create_engine('sqlite:///LTI_provider.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
print(threading.get_ident())

@app.route('/lti/create', methods=['POST'])
def call_lti_content():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            lti_message_type = data['lti_message_type']
            lti_version = data['lti_version']
            resource_link_id=data['resource_link_id']
            print(lti_message_type)
            print(lti_version)
            print(resource_link_id)
            me = User(message_type=lti_message_type, lti_version=lti_version,resource_link_id=resource_link_id)
            db_session.add(me)
            db_session.commit()



            return jsonify({'Message': "CREATED......"}), 200

@app.route('/consumers')
def usersConsumer():
    db_session= DBSession()
    print(threading.get_ident())
    users = db_session.query(User).all()
    return render_template('index_consumer.html', users=users)

@app.route('/lti/delete', methods=['DELETE'])
def deleteConsumer():
    if request.method == 'DELETE':
        if request.is_json:
            data = request.get_json()
            lti_message_type = data['lti_message_type']
            lti_version = data['lti_version']
            resource_link_id = data['resource_link_id']
            print(lti_message_type)
            print(lti_version)
            print(resource_link_id)
            #me = User(message_type=lti_message_type, lti_version=lti_version,resource_link_id=resource_link_id)
            deletedUser = db_session.query(User).filter_by(resource_link_id=resource_link_id).one()
            db_session.delete(deletedUser)
            db_session.commit()

            return jsonify({'Message': "DELETED......"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_LTI_PORT", 5000))
    host = os.environ.get("FLASK_LTI_HOST", "localhost")
    app.run(debug=True, host=host, port=port)
