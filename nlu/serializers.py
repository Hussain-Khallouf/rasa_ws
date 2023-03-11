from rest_framework import serializers

from nlu.models import Intent, IntentExample
from nlu.tasks import add_intent_to_bot


class IntentExampleListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [IntentExample(**item) for item in validated_data]
        return IntentExample.objects.bulk_create(books)


class IntentExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentExample
        fields = "text",
        list_serializer_class = IntentExampleListSerializer


class IntentSerializer(serializers.ModelSerializer):
    examples = IntentExampleSerializer(many=True)

    def create(self, validated_data):
        examples = validated_data.get("examples", [])
        examples_serializer = IntentExampleSerializer(data=examples, many=True)
        examples_serializer.is_valid()
        examples = examples_serializer.save()
        validated_data.pop("examples")
        intent = Intent.objects.create(**validated_data)
        intent.examples.set(examples)
        intent.save()
        add_intent_to_bot(intent.name, list(intent.examples.values_list("text", flat=True)))
        return intent

    def update(self, instance, validated_data):
        instance.examples.remove()
        examples_serializer = IntentExampleSerializer(data=validated_data.get("examples"), many=True)
        examples_serializer.is_valid()
        examples = examples_serializer.save()
        instance.examples.set(examples)
        instance.save()
        return instance

    class Meta:
        model = Intent
        fields = (
            "id",
            "name",
            "examples"
        )
