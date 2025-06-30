from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app.models import User, Hotel, Room, Booking, Review

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password does not match')
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2', None)
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'total_price']

    def validate(self, data):
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError("Check-out date must be after check-in date")

            room = data.get('room')
            if room:
                overlapping_bookings = Booking.objects.filter(
                    room=room,
                    status__in=['pending', 'confirmed'],
                    check_in_date__lt=check_out,
                    check_out_date__gt=check_in
                )
                
                if self.instance:
                    overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)
                
                if overlapping_bookings.exists():
                    raise serializers.ValidationError("Room is not available for the selected dates")
        
        return data


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']

