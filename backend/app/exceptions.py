class ApplicationError(Exception):
    """Базовое исключение приложения."""

    def __init__(self, detail: str = "Внутренняя ошибка") -> None:
        self.detail = detail
        super().__init__(detail)


class NotFoundError(ApplicationError):
    """Запрашиваемый ресурс не найден."""

    def __init__(self, detail: str = "Ресурс не найден") -> None:
        super().__init__(detail)


class ForbiddenError(ApplicationError):
    """Недостаточно прав для выполнения операции."""

    def __init__(
        self, detail: str = "Нет прав на выполнение операции"
    ) -> None:
        super().__init__(detail)
