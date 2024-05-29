"""Метакласс для создания Singleton-классов."""


class SingletonMeta(type):
    """Метакласс для создания Singleton-классов."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Возвращает единственный экземпляр класса."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
