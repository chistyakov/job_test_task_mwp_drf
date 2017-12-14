from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Author, Profile, Book, Card


# TODO: fix the bug with error on adding user + profile
#       via admin without dropping the 'post_save' signals
#       (http://disq.us/p/1eo2g0s)
class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Card)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
