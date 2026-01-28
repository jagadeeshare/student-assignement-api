#post request test
from urllib import response
# -------------------- Student APIs --------------------
#1 post request
def test_post_student(client):
    response = client.post("/student", json={
        "name": "Jagadeesh",
        "age": 22
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "student created"

#2 get request test

def test_get_students(client):
    # Create one student
    client.post("/student", json={"name": "Ram", "age": 21})
    response = client.get("/student")
    assert response.status_code == 200
    students = response.get_json()
    assert len(students) == 1

#3 put request test

def test_put_students(client):
    client.post("/student",json={"name":"Ram","age":21})
    # getting the student_id
    students=client.get("/student").get_json()
    student_id = students[0]["id"]
    #updating the student using put
    response = client.put(f"/student/{student_id}", json={
        "name": "AJ",
        "age": 25
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "data is updated"
    #validating teh updated data
    updated=client.get("/student").get_json()[0]
    assert updated["name"]== "AJ"
    assert updated["age"]==25

#4delete request testing

def test_delete_student(client):
    client.post("/student",json={"name":"Aj","age":21})
    students=client.get("/student").get_json()
    student_id=students[0]["id"]
    client.delete(f"/student/{student_id}")
    response=client.get("/student").get_json()
    assert len(response)==0

#5delete request for not found one

def test_delete_not_student(client):
    client.post("/student",json={"name":"Jaggu","age":21})
    response=client.delete(f"/student/{21}")
    assert response.status_code==404
    assert response.get_json()["message"]=="student not found"

# -------------------- Assignemnet APIs --------------------

#6  post request testing for assignment
def test_post_assignment(client):
    client.post("/student",json={"name":"jaggu","age":21})
    students_id=client.get("/student").get_json()[0]["id"]
    response=client.post("/assignment",json={"topic":"sql_practice","status":"completed","student_id":students_id})
    assert response.status_code==201
    assert response.get_json()["message"]=="created"

#7 get request testing
def test_get_assignment(client):
    client.post("/student",json={"name":"jaggu","age":21})
    students_id=client.get("/student").get_json()[0]["id"]
    client.post("/assignment",json={"topic":"sql_practice","status":"completed","student_id":students_id})
    res=client.get("/assignment")
    assert res.status_code==200
    assert len(res.get_json())==1

#8  delete request testing
def test_delete_assignment(client):
    client.post("/student",json={"name":"jaggu","age":21})
    students_id=client.get("/student").get_json()[0]["id"]
    client.post("/assignment",json={"topic":"sql_practice","status":"completed","student_id":students_id})
    resu=client.get("/assignment")
    assign_id=resu.get_json()[0]["id"]
    res=client.delete(f"/assignment/{assign_id}")
    assert res.status_code==200
    assert res.get_json()["message"]=="Assignment deleted successfully"

#9 put request testing
def test_put_assignment(client):
    client.post("/student",json={"name":"jaggu","age":21})
    students_id=client.get("/student").get_json()[0]["id"]
    client.post("/assignment",json={"topic":"sql_practice","status":"completed","student_id":students_id})
    resu=client.get("/assignment")
    assign_id=resu.get_json()[0]["id"]
    response=client.put(f"/assignment/{assign_id}",json={"topic":"docker","status":"pending","student_id":students_id})
    assert response.status_code==200
    assert response.get_json()["message"]=="Assignment updated successfully"
    #validating the update
    result=client.get("/assignment").get_json()[0]
    assert result["topic"]=="docker"
    assert result["status"]=="pending"

    






