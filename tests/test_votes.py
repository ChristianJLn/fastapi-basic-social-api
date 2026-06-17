import pytest

def test_vote_on_unvoted_post(authorized_client, dummy_posts):
    res = authorized_client.post("/vote/", json={
        "id_post": dummy_posts[0].id,
        "dir": True
    })
    assert res.status_code == 201

def test_vote_on_voted_post(authorized_client, dummy_vote):
    res = authorized_client.post("/vote/", json={
        "id_post": dummy_vote["id_post"],
        "dir": True
    })
    assert res.status_code == 409

def test_unvote_on_voted_post(authorized_client, dummy_vote):
    res = authorized_client.post("/vote/", json={
        "id_post": dummy_vote["id_post"],
        "dir": False
    })
    assert res.status_code == 201

def test_unvote_on_unvoted_post(authorized_client, dummy_posts):
    res = authorized_client.post("/vote/", json={
        "id_post": dummy_posts[0].id,
        "dir": False
    })
    assert res.status_code == 404

def test_vote_on_post_nonexistent(authorized_client):
    res = authorized_client.post("/vote/", json={
        "id_post": 8000,
        "dir": True
    })
    assert res.status_code == 404

@pytest.mark.parametrize("dir", [
    (True,),
    (False,)
])
def test_unauthorized_user_vote_or_unvote_on_post(client, dummy_posts, dir):
    res = client.post("/vote/", json={
        "id_post": dummy_posts[0].id,
        "dir": dir
    })
    assert res.status_code == 401

