from app import schemas
import pytest

def test_get_all_posts(authorized_client, dummy_posts):
    res = authorized_client.get("/posts/")
    
    post_list = list(map(lambda post: schemas.PostOut(**post), res.json()))
    assert len(dummy_posts) == len(post_list)
    assert res.status_code == 200

def test_get_one_post(authorized_client, dummy_posts):
    res = authorized_client.get(f"/posts/{dummy_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == dummy_posts[0].id
    assert post.Post.title == dummy_posts[0].title
    assert post.Post.content == dummy_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published, status_code", [
    ("Post 1", "Content 1", True, 201),
    ("Post 2", "Content 2", False, 201),
    ("Post 3", "Content 3", True, 201),
    ("Post 1", "Content 1", True, 201),
    ("Post 4", "Content 4", None, 201),
])
def test_create_post(authorized_client, dummy_users, dummy_posts, title, content, published, status_code):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    created_post = schemas.PostResponse(**res.json())
    assert created_post.published == published if published != None else True
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == dummy_users[0]["id"]
    assert res.status_code == status_code

@pytest.mark.parametrize("post_id, title, content, published, status_code", [
    (1, "Updated Title", "Updated Content", False, 200),
    (2, "Updated Title", "Updated Content", True, 200),
    (3, "Updated Title", "Updated Content", True, 403),
    (80000, "Updated Title", "Updated Content", True, 404)
])
def test_update_post(authorized_client, dummy_users, dummy_posts, post_id, title, content, published, status_code):
    data = {
        "title": title,
        "content": content,
        "published": published
    }
    res = authorized_client.put(f"/posts/{post_id}", json=data)
    if status_code == 200:
        updated_post = schemas.PostResponse(**res.json())
        assert updated_post.title == data["title"]
        assert updated_post.content == data["content"]
    assert res.status_code == status_code

def test_delete_post(authorized_client, dummy_posts):
    res = authorized_client.delete(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == 204

def test_get_one_post_nonexistent(authorized_client, dummy_posts):
    res = authorized_client.get("/posts/888")
    assert res.status_code == 404

def test_delete_post_nonexistent(authorized_client, dummy_posts):
    res = authorized_client.delete("/posts/888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, dummy_posts):
    res = authorized_client.delete(f"/posts/{dummy_posts[2].id}")
    assert res.status_code == 403

def test_unauthorized_user_get_all_post(client):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, dummy_posts):
    res = client.get(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={
        "title": "Example",
        "content": "Example"
    })
    assert res.status_code == 401

def test_unauthorized_user_update_post(client, dummy_posts):
    res = client.put(f"/posts/{dummy_posts[0].id}", json={
        "title": "Updated Title",
        "content": "Updated Content",
        "published": True
    })
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, dummy_posts):
    res = client.delete(f"/posts/{dummy_posts[0].id}")
    assert res.status_code == 401




