
from flask import Flask, request, jsonify
from app.database import db
from app.models import Student
import os
def create_app():
    app = Flask(__name__)
    # CockroachDB connection URI
    app.config["SQLALCHEMY_DATABASE_URI"] = (
"cockroachdb://durgajagadeesh:sk7neRNanjv4aNeofdc3ZQ@palm-bugbear-11720.jxf.gcp-asia-southeast1.cockroachlabs.cloud:26257/aj?sslmode=verify-full&sslrootcert=ca.crt"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    @app.route("/")
    def home():
        return {"message": "Connected to CockroachDB"}
#get method
    @app.route("/students", methods=["GET"])
    def get_students():
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])
#post method
    @app.route("/students", methods=["POST"])
    def add_student():
        data = request.json
        student = Student(name=data["name"])
        db.session.add(student)
        db.session.commit()
        return student.to_dict(), 201
#put method
    @app.route("/students/<int:id>", methods=["PUT"])
    def update_student(id):
        data = request.json
        student = Student.query.get(id)
        student.name = data["name"]
        db.session.commit()
        return student.to_dict(), 201
#delete method
    @app.route("/students/<int:id>", methods=["DELETE"])
    def delete_student(id):
        student = Student.query.get(id)
        if student is None:
            return {"error": "Student not found"}, 404
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted successfully"}
    return app
