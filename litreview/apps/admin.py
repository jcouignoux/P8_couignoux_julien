from django.contrib import admin

from apps.models import Ticket, Review
# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description',
                     'user', 'image', 'time_created']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['ticket', 'rating',
                     'headline', 'body', 'user', 'time_created']
