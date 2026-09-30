# Thiết kế Resource cho Blog API

## 1. Xác định Resources

Trong Blog API, các resources chính:

- `posts`: Bài viết
- `comments`: Bình luận
- `tags`: Thẻ
- `followers`: Người theo dõi

Quan hệ giữa các resources:

```text
Post
├── Comments
├── Tags
└── Followers
```

## 2. Phân loại Collection / Item / Sub-resource

### Collection

Collection đại diện cho tập hợp các resource:

```text
GET /api/v1/posts
```

Lấy danh sách tất cả bài viết.

### Item

Item đại diện cho một resource cụ thể:

```text
GET /api/v1/posts/{post_id}
```

Ví dụ:

```text
GET /api/v1/posts/1
```

Lấy bài viết có `id = 1`.

### Sub-resource

Sub-resource là resource thuộc về một resource khác:

```text
GET /api/v1/posts/{post_id}/comments
GET /api/v1/posts/{post_id}/tags
GET /api/v1/posts/{post_id}/followers
```

Ví dụ:

```text
GET /api/v1/posts/1/comments
```

Lấy tất cả comment của bài viết có `id = 1`.

## 3. Version API bằng URL Path Segment

API sử dụng version `v1` trong URL:

```text
/api/v1/posts
/api/v1/posts/1
/api/v1/posts/1/comments
/api/v1/posts/1/tags
/api/v1/posts/1/followers
```

Cấu trúc:

```text
/api
└── v1
    └── posts
        └── {post_id}
            ├── comments
            ├── tags
            └── followers
```