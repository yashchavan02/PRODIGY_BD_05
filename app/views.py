from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from app.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({'msg' : "user registration succesful", 'refresh': str(token), 'access': str(token.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
       serializer = UserLoginSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           email = serializer.data.get('email')
           password = serializer.data.get('password')
           user = authenticate(email = email, password = password)
           if user is not None :
               token = RefreshToken.for_user(user)
               return Response({'msg' : "user login succesful", 'refresh': str(token), 'access': str(token.access_token) }, status=status.HTTP_200_OK) 
           return Response({'non_field_errors' : ["Your credentials are not match"]}, status=status.HTTP_404_NOT_FOUND) 
       return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)




from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from app.serializers import HotelSerializer, RoomSerializer, BookingSerializer, ReviewSerializer
from app.models import Hotel, Room, Booking, Review

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filterset_fields = ['city', 'state', 'country']
    search_fields = ['name', 'description', 'city', 'amenities']
    ordering_fields = ['name', 'rating', 'created_at']
    ordering = ['name']

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ['hotel', 'room_type', 'is_available']
    search_fields = ['room_number', 'description', 'amenities']
    ordering_fields = ['price_per_night', 'max_occupancy', 'created_at']
    ordering = ['hotel', 'room_number']

    @action(detail=False, methods=['get'])
    def search_available(self, request):
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        guests = request.query_params.get('guests')
        city = request.query_params.get('city')
        room_type = request.query_params.get('room_type')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        queryset = self.get_queryset().filter(is_available=True)

        if city:
            queryset = queryset.filter(hotel__city__icontains=city)

        if room_type:
            queryset = queryset.filter(room_type=room_type)

        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        if guests:
            queryset = queryset.filter(max_occupancy__gte=guests)

        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                overlapping_bookings = Booking.objects.filter(
                    status__in=['pending', 'confirmed'],
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date
                ).values_list('room_id', flat=True)
                
                queryset = queryset.exclude(id__in=overlapping_bookings)
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                              status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'room__hotel']
    ordering_fields = ['created_at', 'check_in_date', 'check_out_date']
    ordering = ['-created_at']

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Booking cancelled successfully'})
        return Response({'error': 'Cannot cancel this booking'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['hotel', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        if self.action == 'list':
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

