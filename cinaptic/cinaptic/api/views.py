
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from library.semantic.ContextManager import ContextManager

class ContextViewSet(APIView):

    def post(self, request, format=None):

        analizador = ContextManager()
        data = request.data
        print(request.data)
        res = analizador.analyse_context(data)
        response = Response({"status": "ok", "nodes": res})
        response["Access-Control-Allow-Origin"] = "*"

        return response

    def get(self, request, format=None):

        print(request.data)
        return Response({"hola":"mundo"})