from django.urls import path
from .views import (
    list_services, list_categories, contact_submit, service_detail,
    service_create, service_update, service_delete,
    about_us, why_choose, how_it_works, final_cta, stats,
)


urlpatterns = [
    path("services/", list_services, name="services-list"),
    path("services/<int:id>", service_detail, name="service-detail"),
    path("services/create", service_create, name="service-create"),
    path("services/<int:id>/update", service_update, name="service-update"),
    path("services/<int:id>/delete", service_delete, name="service-delete"),
    path("categories", list_categories, name="categories-list"),
    path("contact/submit", contact_submit, name="contact-submit"),
    path("aboutus", about_us, name="about-us"),
    path("why-choose", why_choose, name="why-choose"),
    path("how-it-works", how_it_works, name="how-it-works"),
    path("final-cta", final_cta, name="final-cta"),
    path("stats", stats, name="stats"),
]


