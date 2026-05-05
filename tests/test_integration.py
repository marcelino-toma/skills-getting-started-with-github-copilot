def test_signup_then_unregister_sequence(client):
    email = "sequence@mergington.edu"

    signup_response = client.post(f"/activities/Gym%20Class/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()["Gym Class"]["participants"]

    unregister_response = client.delete(f"/activities/Gym%20Class/signup?email={email}")
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()["Gym Class"]["participants"]


def test_data_isolation_between_tests(client):
    email = "isolated@mergington.edu"
    activities = client.get("/activities").json()
    assert email not in activities["Drama Club"]["participants"]
