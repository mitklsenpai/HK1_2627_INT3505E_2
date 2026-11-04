products = []

def get_products():
    return {"products": products}, 200

def add_product(body):
    products.append(body)
    return body, 201