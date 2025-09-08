# clientes/routers.py
class ClienteRouter:
    """
    Roteador para direcionar operações da model Cliente para o PostgreSQL
    e todas as outras para o SQLite (default)
    """

    def db_for_read(self, model, **hints):
        # Se for a model Cliente, usa o PostgreSQL
        if model._meta.model_name == 'cliente':
            return 'postgres'
        # Todas as outras models usam o SQLite (default)
        return 'default'

    def db_for_write(self, model, **hints):
        # Todas as escritas vão para o SQLite (default)
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Permite relações entre objetos dos dois bancos
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Só permite migrações no banco default (SQLite)
        if db == 'postgres':
            return False  # Não cria/migra tabelas no PostgreSQL
        return True  # Migra tudo no SQLite