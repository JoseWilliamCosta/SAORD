from rest_framework import serializers
from core.models import Session, Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'description',
            'file',
            'created_at'
        ]


class SessionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = [
            'id',
            'title',
            'created_at',
            'documents'
        ]