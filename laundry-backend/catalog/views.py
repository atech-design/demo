from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail

from .models import Service, ContactMessage
from .serializers import ServiceSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def list_services(_request):
    services = Service.objects.filter(is_active=True).order_by("id")
    serializer = ServiceSerializer(services, many=True)
    enriched = []
    default_icons = ["🧺", "🧼", "👟", "🧥", "👗", "👕"]
    for idx, item in enumerate(serializer.data):
        enriched.append({
            **item,
            "icon": default_icons[idx % len(default_icons)],
            "nameKey": item.get("name"),
            "descKey": item.get("description"),
        })
    return Response({"success": True, "data": enriched, "pagination": None})


@api_view(["GET"])
@permission_classes([AllowAny])
def list_categories(_request):
    categories = list(
        Service.objects.filter(is_active=True)
        .order_by()
        .values_list("category", flat=True)
        .distinct()
    )
    if not categories:
        categories = ["All", "Laundry", "Home Care", "Accessories"]
    return Response(categories)


@api_view(["POST"])
@permission_classes([AllowAny])
def contact_submit(request):
    data = request.data
    required = ["name", "email", "message"]
    if not all(data.get(k) for k in required):
        return Response({"message": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
    msg = ContactMessage.objects.create(
        name=data.get("name", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
        subject=data.get("subject", ""),
        message=data.get("message", ""),
    )
    # Send email notification to admin
    try:
        subject = f"New Contact: {msg.subject or 'No subject'}"
        body = (
            f"Name: {msg.name}\n"
            f"Email: {msg.email}\n"
            f"Phone: {msg.phone}\n\n"
            f"Message:\n{msg.message}\n"
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass
    return Response({"success": True})


@api_view(["GET"])
@permission_classes([AllowAny])
def service_detail(_request, id: int):
    try:
        service = Service.objects.get(pk=id, is_active=True)
    except Service.DoesNotExist:
        return Response({"error": True}, status=404)
    data = ServiceSerializer(service).data
    # Mock extra fields expected by ServiceDetail page
    mock = {
        "emoji": "🧺",
        "nameKey": data.get("name"),
        "taglineKey": "Professional care for your clothes",
        "before": "Wrinkled",
        "after": "Crisp & Fresh",
        "steps": [{"key": "Pickup"}, {"key": "Sort & Treat"}, {"key": "Wash & Dry"}, {"key": "Iron & Deliver"}],
        "options": [
            {"id": int(f"{data['id']}01"), "label": "Shirt", "labelKey": "Shirt", "price": float(data["price"]) + 10, "emoji": "👕"},
            {"id": int(f"{data['id']}02"), "label": "Trousers", "labelKey": "Trousers", "price": float(data["price"]) + 15, "emoji": "👖"},
            {"id": int(f"{data['id']}03"), "label": "Kurta", "labelKey": "Kurta", "price": float(data["price"]) + 20, "emoji": "👘"},
            {"id": int(f"{data['id']}04"), "label": "Saree", "labelKey": "Saree", "price": float(data["price"]) + 40, "emoji": "🧣"},
            {"id": int(f"{data['id']}05"), "label": "Jacket", "labelKey": "Jacket", "price": float(data["price"]) + 40, "emoji": "🧥"},
        ],
        "perks": [
            {"key": "Stain Pre-treatment"},
            {"key": "Fabric-safe Detergents"},
            {"key": "Contactless Delivery"}
        ],
    }
    return Response({**data, **mock})


@api_view(["POST"])
@permission_classes([IsAdminUser])
def service_create(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["PATCH", "PUT"])
@permission_classes([IsAdminUser])
def service_update(request, id: int):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response({"message": "Not found"}, status=404)
    partial = request.method == "PATCH"
    serializer = ServiceSerializer(service, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def service_delete(_request, id: int):
    try:
        Service.objects.filter(pk=id).delete()
        return Response(status=204)
    except Exception:
        return Response({"message": "Failed"}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def about_us(_request):
    return Response({
        "stats": [
            {"icon": "Users", "value": 1200, "suffix": "+", "label": "Happy Customers"},
            {"icon": "Shirt", "value": 25, "suffix": "k", "label": "Garments Cleaned"},
            {"icon": "Clock", "value": 5, "suffix": "+", "label": "Years of Service"},
        ],
        "values": [
            {"icon": "ShieldCheck", "title": "Quality First", "desc": "Top detergents and hygiene protocols."},
            {"icon": "Truck", "title": "On-time Delivery", "desc": "Reliable pickups and doorstep delivery."},
            {"icon": "Recycle", "title": "Eco-Friendly", "desc": "We use water- and energy-saving methods."},
            {"icon": "HeartHandshake", "title": "Care & Trust", "desc": "Handled like our own clothes."},
        ],
        "timeline": [
            {"year": "2020", "title": "Started", "text": "Began with neighborhood pickups."},
            {"year": "2022", "title": "Scaled", "text": "Expanded to city-wide operations."},
            {"year": "2024", "title": "Smart Laundry", "text": "Launched app-powered experience."},
        ],
        "team": [
            {"emoji": "👨‍💼", "name": "Amit", "role": "Operations"},
            {"emoji": "👩‍💻", "name": "Riya", "role": "Tech"},
            {"emoji": "🧼", "name": "Kiran", "role": "Quality"},
            {"emoji": "🚚", "name": "Vikas", "role": "Logistics"},
        ],
        "testimonials": [
            {"name": "Neha", "text": "Super quick and reliable!", "rating": 5},
            {"name": "Rohit", "text": "Clothes smell great every time.", "rating": 4},
            {"name": "Sara", "text": "Affordable and on time.", "rating": 5},
        ],
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def why_choose(_request):
    return Response([
        {"title": "Fast Pickup", "desc": "Request pickup in seconds.", "border": "border-blue-400"},
        {"title": "Premium Wash", "desc": "Fabric-friendly cleaning.", "border": "border-purple-400"},
        {"title": "On-time Delivery", "desc": "We value your time.", "border": "border-green-400"},
    ])


@api_view(["GET"])
@permission_classes([AllowAny])
def how_it_works(_request):
    return Response([
        {"animKey": "booking", "step": "Book", "desc": "Schedule a pickup in the app."},
        {"animKey": "pickup", "step": "Pickup", "desc": "Executive collects your laundry."},
        {"animKey": "washing", "step": "Wash", "desc": "Premium wash and care."},
        {"animKey": "delivery", "step": "Deliver", "desc": "Back at your doorstep."},
    ])


@api_view(["GET"])
@permission_classes([AllowAny])
def final_cta(_request):
    return Response({
        "title": "Experience Premium Laundry Today",
        "desc": "Book now and get doorstep pickup within 30 minutes.",
        "ctaText": "Book Now"
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def stats(_request):
    return Response({
        "customers": 1200,
        "clothes": 25000,
        "years": 5,
    })

