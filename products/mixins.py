class ChoiceSerializerMixin:
    """
    Миксин для выбора сериализатора, в зависимости от события
    """
    def get_serializer_class(self):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.serializer_class

        return serializer_class