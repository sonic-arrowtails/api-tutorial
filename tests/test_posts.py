import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    # posts = res.json()

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_list = list(map(validate,res.json()))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

    assert posts_list[-1].Post.id == test_posts[0].id

def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/696969696969")
    assert res.status_code == 404

def test_get_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    assert res.json()["Post"]["title"] == "First Victim"  # before validation, shouldnt rly be here lmao
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id

@pytest.mark.parametrize("title, content, published",[("Test post title","Quality content", True),
                                                      ("titel two","content two", False)])
def test_create_posts(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title":title,"content":content,"published":published})
    assert res.status_code == 201
    post = schemas.Post(**res.json())
    assert post.title == title
    assert post.content == content

def test_create_posts_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={"title":"title","content":"content"})
    assert res.status_code == 201
    post = schemas.Post(**res.json())
    assert post.title == "title"
    assert post.content == "content"

def test_unauthorized_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title":"title","content":"content"})
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/789678976796")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res = authorized_client.put("/posts/6969696969", json=data)
    assert res.status_code == 404
