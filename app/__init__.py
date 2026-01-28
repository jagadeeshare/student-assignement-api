from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
"cockroachdb://durgajagadeesh:sk7neRNanjv4aNeofdc3ZQ@palm-bugbear-11720.jxf.gcp-asia-southeast1.cockroachlabs.cloud:26257/aj?sslmode=verify-full&sslrootcert=ca.crt"
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# -------------------- Models --------------------
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)  # CockroachDB supports INT
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )

# -------------------- Create Tables --------------------
with app.app_context():
    db.create_all()
# -------------------- Routes --------------------
@app.route("/")
def home():
    return "Server is running"
# -------------------- Student APIs --------------------

@app.route("/student", methods=["POST"])
def create_student():
    data = request.get_json()
    student = Student(name=data["name"], age=data["age"])
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "student created"}), 201

@app.route("/student", methods=["GET"])
def read_all():
    students = Student.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "age": s.age}
        for s in students
    ])

@app.route("/student/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "id is not present"}), 404
    student.name = data["name"]
    student.age = data["age"]
    db.session.commit()
    return jsonify({"message": "data is updated"}), 200

@app.route("/student/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "data is deleted successsfully"}), 200

# -------------------- Assignment APIs --------------------

@app.route("/assignment", methods=["POST"])
def adding_data():
    data = request.get_json()
    student = Student.query.get(data["student_id"])
    if not student:
        return jsonify({"message": "record not exixt"}), 404
    assignment = Assignment(
        topic=data["topic"],
        status=data["status"],
        student_id=data["student_id"]
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({"message": "created"}), 201

@app.route("/assignment/<int:id>", methods=["PUT"])
def update_assignment(id):
    data = request.get_json()
    assignment = Assignment.query.get(id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404
    assignment.topic = data["topic"]
    assignment.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Assignment updated successfully"}), 200

@app.route("/assignment", methods=["GET"])
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([
        {
            "id": a.id,
            "topic": a.topic,
            "status": a.status,
            "student_id": a.student_id
        }
        for a in assignments
    ])

@app.route("/assignment/<int:id>", methods=["DELETE"])
def delete_assignment(id):
    assignment = Assignment.query.get(id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": "Assignment deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

