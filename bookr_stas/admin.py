from django.contrib import admin


class BookrAdminSite(admin.AdminSite):
    site_title = 'Bookr Admin'
    site_header = 'Bookr Administration'
    index_title = 'Bookr site admin'
