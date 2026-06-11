

def test_create_category(client, auth_headers):
    response = client.post(
        "/categories",
        json={"name": "Food"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Food"

def test_get_categories(client, auth_headers):
    client.post(
        "/categories",
        json={"name": "Food"},
        headers=auth_headers
    )
    
    response=client.get(
        "/categories",headers=auth_headers
    )
    assert response.status_code==200
    assert isinstance(response.json(),list)
    assert len(response.json())>0
    assert response.json()[0]["name"]=="Food"