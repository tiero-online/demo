from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    Сериализер, который принимает дополнительный аргумент `fields`,
    который контролирует, какие поля должны отображаться.

    Пример:

    profile = UserProfile.objects.get(user=request.user)
    serializer = DynamicProfileSerializer(profile, fields=('id', 'username', 'email'))

    Без указания 'fields' будут выбраны все поля.

    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        assert not (fields and exclude), (
            "Нельзя указывать одновременно 'fields' и 'exclude'"
        )
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            # Удаляет поля, которые НЕ находятся в 'fields'
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            # Удаляет поля, которые находятся в 'exclude'
            excluded = set(exclude)
            for field_name in excluded:
                self.fields.pop(field_name)
