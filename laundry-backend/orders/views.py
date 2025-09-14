from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# Simple in-memory cart per user for demo. Replace with DB later.
_carts = {}


def _get_cart(user_id):
    return _carts.setdefault(user_id, {"items": [], "totalQty": 0, "total": 0})


@api_view(["GET", "DELETE"])
@permission_classes([AllowAny])
def cart_root(request):
    user_id = request.user.id if request.user and request.user.is_authenticated else 0
    if request.method == "GET":
        return Response(_get_cart(user_id))
    # DELETE clears the cart for demo
    _carts[user_id] = {"items": [], "totalQty": 0, "total": 0}
    return Response(_carts[user_id])


@api_view(["POST"])
@permission_classes([AllowAny])
def cart_add(request):
    user_id = request.user.id if request.user and request.user.is_authenticated else 0
    cart = _get_cart(user_id)
    item_id = request.data.get("id")
    qty = int(request.data.get("qty", 1))
    price = float(request.data.get("price", 0))
    
    if item_id is None:
        return Response({"message": "id required"}, status=400)
    if price <= 0:
        return Response({"message": "valid price required"}, status=400)
        
    existing = next((i for i in cart["items"] if i["id"] == item_id), None)
    if existing:
        existing["qty"] += qty
    else:
        cart["items"].append({
            "id": item_id, 
            "qty": qty, 
            "price": price,
            "name": request.data.get("name", f"Item {item_id}"),
            "emoji": request.data.get("emoji", "📦")
        })
    cart["totalQty"] = sum(i["qty"] for i in cart["items"])
    cart["total"] = sum(i["qty"] * float(i["price"]) for i in cart["items"])
    return Response(cart)


@api_view(["POST"])
@permission_classes([AllowAny])
def cart_decrease(request):
    user_id = request.user.id if request.user and request.user.is_authenticated else 0
    cart = _get_cart(user_id)
    item_id = request.data.get("id")
    existing = next((i for i in cart["items"] if i["id"] == item_id), None)
    if existing:
        existing["qty"] -= 1
        if existing["qty"] <= 0:
            cart["items"] = [i for i in cart["items"] if i["id"] != item_id]
    cart["totalQty"] = sum(i["qty"] for i in cart["items"])
    cart["total"] = sum(i["qty"] * float(i["price"]) for i in cart["items"])
    return Response(cart)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def cart_remove(request, id):
    user_id = request.user.id if request.user and request.user.is_authenticated else 0
    cart = _get_cart(user_id)
    cart["items"] = [i for i in cart["items"] if str(i["id"]) != str(id)]
    cart["totalQty"] = sum(i["qty"] for i in cart["items"])
    cart["total"] = sum(i["qty"] * float(i["price"]) for i in cart["items"])
    return Response(cart)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def cart_clear_all(_request):
    _carts.clear()
    return Response({"items": [], "totalQty": 0, "total": 0})


@api_view(["GET"])
@permission_classes([AllowAny])
def my_orders(_request):
    # Demo data shaped for MyOrders.jsx
    sample = [
        {
            "_id": "demo-1",
            "serviceName": "Laundry Service",
            "status": "Pending",
            "createdAt": "2025-01-01T00:00:00Z",
            "total": 299,
        }
    ]
    return Response(sample)


