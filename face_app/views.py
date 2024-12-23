import os
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Person
from django.conf import settings

# Ensure media directory exists
media_dir = os.path.join(settings.MEDIA_ROOT, 'images')
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Function to handle image upload and saving the data
def create_person(request):
    if request.method == "POST":
        # Ensure the media/images directory exists
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Get all image files in the media/images directory
        image_files = [f for f in os.listdir(media_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        # Convert image file names to relative paths for storage
        image_paths = [os.path.join('images', image) for image in image_files]

        # Extract name and roll number from POST request
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')

        if name and roll_number:
            try:
                # Check if the person already exists
                person = Person.objects.get(roll_number=roll_number)
                response_data = {"status": "error", "message": "Person already exists."}
                return JsonResponse(response_data, status=400)
            except ObjectDoesNotExist:
                # If the person doesn't exist, create a new entry
                person = Person(name=name, roll_number=roll_number, image_path=json.dumps(image_paths))
                person.save()

                # Process the images (for example, create face encodings or just store paths)
                for image_path in image_paths:
                    print(f"Processing image: {image_path}")
                    # Add your logic for processing images (e.g., face recognition model training)

                # Return a success response
                response_data = {"status": "success", "message": "Person created successfully."}
                return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"status": "error", "message": "Name and roll number are required."}, status=400)

    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

# Function to display all stored data
def display_data(request):
    people = Person.objects.all()
    for person in people:
        try:
            # Decode the JSON string stored in the database
            person.image_paths = json.loads(person.image_path) if person.image_path else []
        except json.JSONDecodeError:
            # Handle malformed JSON gracefully
            person.image_paths = []
    return render(request, 'display_data.html', {'people': people})
