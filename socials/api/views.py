from rest_framework.decorators import api_view
from rest_framework.response import Response
from socials.models import Room
from socials.api.serializers import RoomSerializer
@api_view(['GET'])
def getRoute(request):
    routes =[
        'GET /api' 
        'GET /api/rooms',
        'GET /api/rooms/id'
        ]
    return Response(routes,)
@api_view(['GET'])
def getRoom(request):
    room =Room.objects.all()
    serializer = RoomSerializer(room, many =True)

    return Response(serializer.data)