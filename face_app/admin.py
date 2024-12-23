# import json  # Add this line to import json module
# from django.contrib import admin
# from .models import Person

# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('name', 'roll_number', 'image_count', 'image_preview')
#     search_fields = ('name', 'roll_number')
#     list_filter = ('name',)

#     def image_count(self, obj):
#         """Count the number of images stored for a person."""
#         if obj.image_path:
#             return len(json.loads(obj.image_path))
#         return 0
#     image_count.short_description = 'Number of Images'

#     def image_preview(self, obj):
#         """Display the first image as a preview (if available)."""
#         if obj.image_path:
#             image_paths = json.loads(obj.image_path)
#             if image_paths:
#                 return f"<img src='/{image_paths[0]}' width='50' height='50' />"
#         return "No Image"
#     image_preview.allow_tags = True
#     image_preview.short_description = 'Preview'

# # Register the model with admin
# admin.site.register(Person, PersonAdmin)



import json
from django.contrib import admin
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'image_count', 'image_preview')

    def image_count(self, obj):
        try:
            if obj.image_path:
                return len(json.loads(obj.image_path))
        except json.JSONDecodeError:
            return "Invalid JSON"
        return 0

    def image_preview(self, obj):
        try:
            if obj.image_path:
                image_paths = json.loads(obj.image_path)
                if image_paths:
                    return f"<img src='/{image_paths[0]}' width='50' height='50' />"
        except json.JSONDecodeError:
            return "Invalid JSON"
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

admin.site.register(Person, PersonAdmin)
