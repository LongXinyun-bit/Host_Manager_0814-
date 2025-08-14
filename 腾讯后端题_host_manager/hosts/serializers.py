from rest_framework import serializers
from .models import City, IDC, Host, HostStats


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class IDCSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = IDC
        fields = ['id', 'name', 'city']


class HostSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    idc = serializers.PrimaryKeyRelatedField(queryset=IDC.objects.all())
    root_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Host
        fields = [
            'id', 'hostname', 'ip', 'city', 'idc',
            'root_password', 'ping_last_ok', 'ping_last_rtt_ms',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['ping_last_ok', 'ping_last_rtt_ms', 'created_at', 'updated_at']

    def create(self, validated_data):
        from .utils import encrypt_text
        password = validated_data.pop('root_password')
        encrypted = encrypt_text(password)
        host = Host.objects.create(root_password_encrypted=encrypted, **validated_data)
        return host

    def update(self, instance, validated_data):
        from .utils import encrypt_text
        password = validated_data.pop('root_password', None)
        if password is not None:
            instance.root_password_encrypted = encrypt_text(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class HostStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostStats
        fields = ['id', 'stat_date', 'city', 'idc', 'host_count'] 