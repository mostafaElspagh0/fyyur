from enums import Genre


def genre_validator():
    message = 'Invalid genre value.'
    values = [g.value for g in Genre]

    def _validate(form, field):
        for value in field.data:
            if value not in values:
                raise ValidationError(message)

    return _validate
