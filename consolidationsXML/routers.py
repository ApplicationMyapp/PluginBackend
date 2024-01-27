class ConsolidationRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'consolidationsXML' and model.__name__ == 'Token':
            return 'consolidation'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'consolidationsXML' and model.__name__ == 'Token':
            return 'consolidation'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'consolidationsXML' and obj1.__class__.__name__ == 'Token' or
            obj2._meta.app_label == 'consolidationsXML' and obj1.__class__.__name__ == 'Token'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'consolidationsXML' and model_name == 'Token':
            return db == 'consolidation'
        return None
