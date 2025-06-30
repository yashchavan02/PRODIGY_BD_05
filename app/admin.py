from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Hotel, Room, Booking, Review

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at', 'last_login')




@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'rating', 'created_at')
    list_filter = ('city', 'state', 'country', 'rating')
    search_fields = ('name', 'city', 'description')
    readonly_fields = ('created_at', 'updated_at')




@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'price_per_night', 'max_occupancy', 'is_available')
    list_filter = ('room_type', 'is_available', 'hotel')
    search_fields = ('room_number', 'hotel__name', 'description')
    readonly_fields = ('created_at', 'updated_at')




@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('user__email', 'room__hotel__name', 'room__room_number')
    readonly_fields = ('created_at', 'updated_at', 'total_price')




@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'hotel__name', 'comment')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, UserAdmin)

