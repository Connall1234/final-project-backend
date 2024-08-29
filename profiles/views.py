from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk is not None:
            # Detailed view of a specific profile
            profile = self.get_object(pk)

            if request.user.is_superuser or profile.owner == request.user:
                self.check_object_permissions(self.request, profile)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Not authorized to view this profile.'}, status=status.HTTP_403_FORBIDDEN)

        # Listing view of profiles
        if request.user.is_superuser:
            # Superuser: Return all profiles
            profiles = Profile.objects.all()
        else:
            # Regular user: Return only their own profile
            profiles = Profile.objects.filter(owner=request.user)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)

        if request.user.is_superuser or profile.owner == request.user:
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Not authorized to update this profile.'}, status=status.HTTP_403_FORBIDDEN)
