import datetime
from fastzap.models import Chat, Message
from django.contrib.auth.models import User
from rest_framework import serializers, fields

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], first_name=validated_data['first_name'], password=validated_data['password'])
        return user


class MessageSerializer(serializers.ModelSerializer):
    timestamp = fields.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['sender'] = UserSerializer(instance=User.objects.get(pk=ret['sender'])).data
        return ret
    
    def create(self, validated_data):
        chat = Chat.objects.get(pk=self.context['view'].kwargs['parent_lookup_message_chat'])
        message = Message.objects.create(chat=chat, **validated_data)
        return message

    class Meta:
        model = Message
        fields = ['id','text_content', 'sender', 'timestamp']
        

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['participants'] = UserSerializer(instance.participants, many=True).data
        return ret
    
    def create(self, validated_data):
        
        validated_data['participants'].append(self.context['request'].user)
        return super().create(validated_data)
    class Meta:
        model = Chat
        fields = ['id', 'messages', 'participants']