import os

class dbpgspedRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_dbpgsped_labels = {'sped'}
    route_dbpg_labels = {'requisicoes'}
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to default.
        """
        if model._meta.app_label  in self.route_dbpgsped_labels:
            return 'dbpgsped'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to dbpg.
        """
        if model._meta.app_label  in self.route_dbpgsped_labels:
            return 'dbpgsped'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_dbpgsped_labels or
            obj2._meta.app_label in self.route_dbpgsped_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'dbpg' database.
        """
        if app_label in self.route_dbpgsped_labels:
            #return True#os dois tem tudo...
            return db == 'dbpgsped'
            # apenas dbpgsped recebe as tabelas de sped
        if app_label in self.route_dbpg_labels:
            return db == 'default'
            # apenas default recebe as tabelas de requisicoes
        # Qd os dois bancos tem auth e contenttypes a aplicação parece funcionar normalmente
        return None
    
    """
    def allow_syncdb(self, db, model):
        if model._meta.app_label in self.route_app_labels:
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True
    """