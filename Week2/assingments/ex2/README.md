# PokeAPI - Public REST API

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Common Headers](#common-headers)
- [Endpoints](#endpoints)
  - [Pokemon List](#1-pokemon-list)
  - [Pokemon Detail](#2-pokemon-detail)
  - [Ability Detail](#3-ability-detail)
  - [Type Detail](#4-type-detail)
  - [Generation Detail](#5-generation-detail)
---

## Overview

[PokeAPI](https://pokeapi.co/) là public API cung cấp dữ liệu về Pokemon, abilities, types, generations và nhiều tài nguyên khác.

---

## Base URL

```
https://pokeapi.co/api/v2
```

---

## Common Headers

### Request Headers

```http
Accept: application/json
```

### Response Headers

```http
Content-Type: application/json
```
---

## Endpoints

### 1. Pokemon List

```
GET /pokemon?limit=20&offset=0
```

| Thuộc tính | Giá trị |
|:-----------|:--------|
| Method     | `GET`   |
| Status     | `200 OK` |
| Error      | `400 Bad Request` nếu query không hợp lệ |

Trả về danh sách Pokemon. `limit` giới hạn số lượng kết quả, `offset` xác định vị trí bắt đầu.

<details>
<summary>Ví dụ sử dụng cURL</summary>

```bash
curl -H "Accept: application/json" \
  "https://pokeapi.co/api/v2/pokemon?limit=20&offset=0"
```

</details>

---

### 2. Pokemon Detail

```
GET /pokemon/{name_or_id}
```

| Thuộc tính | Giá trị |
|:-----------|:--------|
| Method     | `GET`   |
| Status     | `200 OK` |
| Error      | `404 Not Found` nếu Pokemon không tồn tại |

Trả về thông tin chi tiết của Pokemon, bao gồm ID, types, abilities, stats và sprites.

<details>
<summary>Ví dụ: Pikachu</summary>

```bash
curl -H "Accept: application/json" \
  "https://pokeapi.co/api/v2/pokemon/pikachu"
```

</details>

---

### 3. Ability Detail

```
GET /ability/{id}
```

| Thuộc tính | Giá trị |
|:-----------|:--------|
| Method     | `GET`   |
| Status     | `200 OK` |
| Error      | `404 Not Found` nếu Ability không tồn tại |

Trả về thông tin Ability và danh sách Pokemon có Ability đó.

<details>
<summary>Ví dụ: Ability ID 65</summary>

```bash
curl -H "Accept: application/json" \
  "https://pokeapi.co/api/v2/ability/65"
```

</details>

---

### 4. Type Detail

```
GET /type/{id}
```

| Thuộc tính | Giá trị |
|:-----------|:--------|
| Method     | `GET`   |
| Status     | `200 OK` |
| Error      | `404 Not Found` nếu Type không tồn tại |

Trả về thông tin Type, các điểm mạnh/yếu và Pokemon thuộc Type đó.

<details>
<summary>Ví dụ: Type ID 3 (Fighting)</summary>

```bash
curl -H "Accept: application/json" \
  "https://pokeapi.co/api/v2/type/3"
```

</details>

---

### 5. Generation Detail

```
GET /generation/{id}
```

| Thuộc tính | Giá trị |
|:-----------|:--------|
| Method     | `GET`   |
| Status     | `200 OK` |
| Error      | `404 Not Found` nếu Generation không tồn tại |

Trả về thông tin Generation, bao gồm vùng, Pokemon, moves và types liên quan.

<details>
<summary>Ví dụ: Generation I</summary>

```bash
curl -H "Accept: application/json" \
  "https://pokeapi.co/api/v2/generation/1"
```

</details>

---
