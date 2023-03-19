import importlib


def find_model_class_by_path(model_class_path: str):
    # model_class_path's format:module_path.class_name
    model_name = model_class_path.split('.')[-1]
    model_import = model_class_path.replace('.' + model_name, '')

    module = importlib.import_module(model_import)
    class_db_manager = getattr(module, model_name)

    return class_db_manager
