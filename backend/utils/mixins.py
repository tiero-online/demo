from backend.utils.serializers import DynamicFieldsModelSerializer


class DynamicModelSerializersMixin:
    """
    Миксин для использовния динамических сериализеров
    в rest_framework.generics

    ВНИМАНИЕ: При использовании необходимо указывать
    первым(!) наследуемым классом данный миксин.

    Пример неработающего кода:

    class MyListAPIView(generics.ListAPIView, DynamicModelSerializersMixin):
        pass  # Этот код нерабочий!

    Пример работающего кода:

    class MyListAPIView(DynamicModelSerializersMixin, generics.ListAPIView):
        pass  # Этот код сработает.

    P.S. Почему так - я пока не разобрался.
    """
    serializer_fields = None
    serializer_exclude = None

    def __init__(self, *args, **kwargs):
        assert not (self.serializer_fields and self.serializer_exclude), (
            'Нельзя указывать одновременно "serializer_fields" и "serializer_exclude"'
        )
        assert issubclass(self.serializer_class, DynamicFieldsModelSerializer), (
            'Для использования данного миксина необходимо '
            'использовать сериализер, наследующийся от '
            'DynamicFieldsModelSerializer'
        )
        super().__init__(*args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        if self.serializer_fields is not None:
            fields = set(self.serializer_fields)
            kwargs['fields'] = fields
        if self.serializer_exclude is not None:
            exclude = set(self.serializer_exclude)
            kwargs['exclude'] = exclude
        return super().get_serializer(*args, **kwargs)
