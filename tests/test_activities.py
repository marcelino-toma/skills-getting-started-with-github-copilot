from src import app as app_module


def test_get_activities_returns_all(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_structure(client):
    response = client.get("/activities")
    assert response.status_code == 200

    activity = response.json()["Chess Club"]
    assert activity["description"] == "Learn strategies and compete in chess tournaments"
    assert activity["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert activity["max_participants"] == 12
    assert isinstance(activity["participants"], list)


def test_signup_successful(client):
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_duplicate_email_returns_400(client):
    email = "duplicate@mergington.edu"
    first_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"
    assert app_module.activities["Chess Club"]["participants"].count(email) == 1


def test_signup_nonexistent_activity_returns_404(client):
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_successful(client):
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    response = client.delete("/activities/Chess%20Club/signup?email=missing@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_nonexistent_activity_returns_404(client):
    response = client.delete("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
