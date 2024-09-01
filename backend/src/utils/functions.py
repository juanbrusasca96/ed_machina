from pydantic import BaseModel


def filter_fields(data: BaseModel, model_cls):
    """
    Filtra los campos de un Pydantic BaseModel para incluir solo aquellos que existen en el modelo SQLAlchemy.

    :param data: La instancia del modelo Pydantic.
    :param model_cls: La clase del modelo SQLAlchemy.
    :return: Un diccionario con los campos filtrados.
    """
    model_fields = set(model_cls.__table__.columns.keys())
    data_dict = data.model_dump()
    return {key: value for key, value in data_dict.items() if key in model_fields}


def extract_id(obj, id_name):
    """
    Extrae el valor de un identificador de un objeto.

    Args:
        obj: El objeto del cual se va a extraer el identificador.
             Puede ser un diccionario, una tupla, una lista o cualquier objeto con atributos.
        id_name: El nombre o índice del identificador a extraer.
                 Si el objeto es un diccionario, `id_name` es la clave.
                 Si el objeto es una tupla o lista, `id_name` es el índice.
                 Si el objeto es de otro tipo, `id_name` es el nombre del atributo.

    Returns:
        El valor del identificador si existe; de lo contrario, retorna None.
    """
    if isinstance(obj, dict):
        id = obj.get(id_name)
    elif isinstance(obj, tuple) or isinstance(obj, list):
        try:
            id = obj[id_name]
        except IndexError:
            id = None
    else:
        id = getattr(obj, id_name, None)

    return id


def get_dict_from_list(array: list, id_name_or_index):
    """
    Agrupa objetos de una lista en un diccionario basado en un identificador especificado.

    Args:
        array (list): La lista de objetos que se van a agrupar.
        id_name_or_index: El nombre o índice usado para extraer el identificador de cada objeto.
                 Puede ser una clave de diccionario, un índice de lista/tupla o un nombre de atributo de objeto.

    Returns:
        Un diccionario donde cada clave es un identificador y cada valor es una lista de objetos
        que tienen ese identificador.
    """
    grouped_dict = {}

    for obj in array:
        if obj is not None:
            key = extract_id(obj, id_name_or_index)

            if key is not None:
                if key in grouped_dict:
                    grouped_dict[key].append(obj)
                else:
                    grouped_dict[key] = [obj]

    return grouped_dict
