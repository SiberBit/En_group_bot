import uuid


def generate_unique_token(Model, token_field="token", token_function=lambda: uuid.uuid4().hex):
    """
    Generates random tokens until a unique one is found
    :param Model: a Model class that should be searched
    :param token_field: a string with the name of the token field to search in the model_class
    :param token_function: a callable that returns a candidate value
    :return: the unique candidate token
    """

    unique_token_found = False
    while not unique_token_found:
        token = token_function()
        # This weird looking construction is a way to pass a value to a field with a dynamic name
        if Model.objects.filter(**{token_field: token}).count() == 0:
            unique_token_found = True
    return token
