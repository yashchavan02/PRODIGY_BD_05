import os
import sys
import django
from datetime import date, timedelta

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestAPI.settings')
# django.setup()

from app.models import User, Hotel, Room, Booking, Review

def create_sample_data():
    print("Creating sample data...")
    
    # Create sample hotels
    hotel1 = Hotel.objects.create(
        name="Grand Plaza Hotel",
        description="Luxury hotel in the heart of the city with world-class amenities",
        address="Nagala park",
        city="Kolhapur",
        state="Maharashra",
        country="India",
        postal_code="416237",
        phone="+911234567890",
        email="info@grandplaza.com",
        rating=4.5,
        amenities="WiFi, Pool, Gym, Spa, Restaurant, Bar, Parking"
    )
    
    hotel2 = Hotel.objects.create(
        name="Seaside Resort",
        description="Beautiful beachfront resort with stunning ocean views",
        address="456 Ocean Drive",
        city="Mumbai",
        state="Maharashra",
        country="India",
        postal_code="416377",
        phone="+911234567890",
        email="info@seasideresort.com",
        rating=4.8,
        amenities="WiFi, Beach Access, Pool, Spa, Restaurant, Water Sports"
    )
    
    hotel3 = Hotel.objects.create(
        name="Mountain View Lodge",
        description="Cozy mountain lodge perfect for nature lovers",
        address="Durga Tekdi",
        city="Pune",
        state="Maharashra",
        country="India",
        postal_code="416871",
        phone="+911234567890",
        email="info@mountainview.com",
        rating=4.2,
        amenities="WiFi, Fireplace, Hiking Trails, Restaurant, Parking"
    )
    

    # Create sample rooms
    rooms_data = [
        # Grand Plaza Hotel rooms
        {"hotel": hotel1, "room_number": "101", "room_type": "single", "price": 150.00, "occupancy": 1},
        {"hotel": hotel1, "room_number": "102", "room_type": "double", "price": 200.00, "occupancy": 2},
        {"hotel": hotel1, "room_number": "201", "room_type": "suite", "price": 350.00, "occupancy": 4},
        {"hotel": hotel1, "room_number": "301", "room_type": "deluxe", "price": 280.00, "occupancy": 2},
        
        # Seaside Resort rooms
        {"hotel": hotel2, "room_number": "A1", "room_type": "double", "price": 250.00, "occupancy": 2},
        {"hotel": hotel2, "room_number": "A2", "room_type": "suite", "price": 450.00, "occupancy": 4},
        {"hotel": hotel2, "room_number": "B1", "room_type": "family", "price": 380.00, "occupancy": 6},
        {"hotel": hotel2, "room_number": "B2", "room_type": "deluxe", "price": 320.00, "occupancy": 3},
        
        # Mountain View Lodge rooms
        {"hotel": hotel3, "room_number": "C1", "room_type": "single", "price": 120.00, "occupancy": 1},
        {"hotel": hotel3, "room_number": "C2", "room_type": "double", "price": 180.00, "occupancy": 2},
        {"hotel": hotel3, "room_number": "C3", "room_type": "family", "price": 300.00, "occupancy": 5},
        {"hotel": hotel3, "room_number": "C4", "room_type": "suite", "price": 280.00, "occupancy": 3},
    ]
    
    for room_data in rooms_data:
        Room.objects.create(
            hotel=room_data["hotel"],
            room_number=room_data["room_number"],
            room_type=room_data["room_type"],
            description=f"Comfortable {room_data['room_type']} room with modern amenities",
            price_per_night=room_data["price"],
            max_occupancy=room_data["occupancy"],
            amenities="WiFi, TV, Air Conditioning, Mini Bar, Room Service",
            is_available=True
        )
    
    # Create sample users
    user1 = User.objects.create_user(
        email="satejpatil@example.com",
        name="satej Patil",
        password="password123"
    )
    
    user2 = User.objects.create_user(
        email="krishmahadik@example.com",
        name="Krish Mahadik",
        password="password123"
    )
    
    # Create sample bookings
    room1 = Room.objects.get(hotel=hotel1, room_number="102")
    room2 = Room.objects.get(hotel=hotel2, room_number="A1")
    
    booking1 = Booking.objects.create(
        user=user1,
        room=room1,
        check_in_date=date.today() + timedelta(days=7),
        check_out_date=date.today() + timedelta(days=10),
        guests=2,
        status='confirmed',
        special_requests="Late check-in requested"
    )
    
    booking2 = Booking.objects.create(
        user=user2,
        room=room2,
        check_in_date=date.today() + timedelta(days=14),
        check_out_date=date.today() + timedelta(days=17),
        guests=2,
        status='pending'
    )
    
    # Create sample reviews
    Review.objects.create(
        user=user1,
        hotel=hotel1,
        booking=booking1,
        rating=5,
        comment="Excellent service and beautiful rooms. Highly recommended!"
    )
    
    print("Sample data created successfully!")
    print(f"Created {Hotel.objects.count()} hotels")
    print(f"Created {Room.objects.count()} rooms")
    print(f"Created {User.objects.filter(is_superuser=False).count()} regular users")
    print(f"Created {Booking.objects.count()} bookings")
    print(f"Created {Review.objects.count()} reviews")

if __name__ == "__main__":
    create_sample_data()

