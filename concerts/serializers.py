from rest_framework import serializers
from .models import Venue, Concert, Composition

# Simple serializer for venues (used in dropdowns or detail views)
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'city', 'address', 'map_link']


# Serializer for compositions (inside each concert program)
class CompositionSerializer(serializers.ModelSerializer):
    concert = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Composition
        fields = ['id', 'composer', 'title', 'order', 'concert']  # concert = the FK id

# Main serializer for concerts (includes nested program and nested venue)
#one Concert ➜ many Compositions ---> program = CompositionSerializer(many=True)
#Many Concert ➜ one Venue ----> venue = PrimaryKeyRelatedField(...) , A concert happens at one venue, selected by ID
class ConcertSerializer(serializers.ModelSerializer):
    program = CompositionSerializer(many=True, required= False)
    venue = serializers.PrimaryKeyRelatedField(queryset=Venue.objects.all())

    class Meta:
        model = Concert
        fields = [
            'id', 'title', 'date', 'venue', 'description',
            'ticket_link', 'event_link', 'is_public', 'created_at', 'program'
        ]
        read_only_fields = ('id', 'created_at')  # good practice

    def create(self, validated_data):
        program_data = validated_data.pop('program',[])
        concert = Concert.objects.create(**validated_data)

        for item in program_data:
            Composition.objects.create(concert=concert, **item)

        return concert

    def update(self, instance, validated_data):
        program_data = validated_data.pop('program', None)

        # Update concert fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if program_data is not None:
            # Clear and recreate program list (simpler than complex updates)
            instance.program.all().delete()
            for item in program_data:
                Composition.objects.create(concert=instance, **item)

        return instance

