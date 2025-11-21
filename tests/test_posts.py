from app import schemas

import pytest

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
    

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/9999")
    assert res.status_code == 404
    

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())    
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_posts[0].owner_id
    
    
@pytest.mark.parametrize("title, content, published", [
    ("New Post 1", "Content for new post 1", True),
    ("New Post 2", "Content for new post 2", False),
    ("New Post 3", "Content for new post 3", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    
    
def test_unauthorized_user_create_post(client, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "Unauthorized Post", "content": "Should not be created"}
    )
    assert res.status_code == 401
    
    
def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    

def test_delete_post_success(authorized_client, test_user, test_posts):
    post_to_delete = test_posts[0]
    res = authorized_client.delete(f"/posts/{post_to_delete.id}")
    assert res.status_code == 204


def test_delete_post_non_existent(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/9999")
    assert res.status_code == 404
    
    
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
