class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class FindStatusException(Exception):
    """Вызывается, когда не может найти статус в карточке PEP"""
    pass
