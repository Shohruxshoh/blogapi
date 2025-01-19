from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Har bir sahifadagi yozuvlar soni
    page_size_query_param = 'page_size'  # Foydalanuvchi so'rov orqali o'zgartirishi mumkin
    max_page_size = 50  # Maksimal ruxsat etilgan sahifa hajmi
