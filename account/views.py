from django.shortcuts import render
from .models import Account
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .permission import IsOwnerUserOrReadOnly
from .serializer import RegisterSerializer, LoginSerializer, MyAccountSerializer,MyAccountUpdateSerializer


class AccountRegister(generics.GenericAPIView):
    # http://127.0.0.1:8000/api/account/register
    serializer_class = RegisterSerializer

    def post(self, *args, **kwargs):
        user = self.request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'muvaffaqiyat': True, 'xabar': 'Hisob Muvaffaqiyatli yaratildi'})


class AccountLogin(generics.GenericAPIView):
    # http://127.0.0.1:8000/api/account/login
    serializer_class = LoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'muvaffaqiyat': True, "ma'lumotlar": serializer.data['tokens']}, status=status.HTTP_200_OK)


class MyAccount(generics.GenericAPIView):
    serializer_class = MyAccountSerializer

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response({'muvaffaqiyat': True, "ma'lumotlar": serializer.data}, status=status.HTTP_200_OK)


class MyAccountRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerUserOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = super().get_object()
        if query:
            serializer = self.serializer_class(query)
            return Response({'muvaffaqiyat': True, "ma'lumotlar": serializer.data}, status=status.HTTP_200_OK)
        return Response({'muvaffaqiyat': False, "ma'lumotlar": "so'rov mavjud emas"})

    def put(self, request, *args, **kwargs):
        obj = super().get_object()
        serializer = self.serializer_class(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'muvaffaqiyat': True, "ma'lumotlar": serializer.data}, status=status.HTTP_200_OK)
        return Response({'muvaffaqiyat': False, "ma'lumotlar": "hisob malumotlari yaroqsiz"})

    def delete(self, request, *args, **kwargs):
        obj = super().get_object()
        obj.delete()
        return Response({'muvaffaqiyat': True})







