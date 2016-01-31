from google.appengine.ext import ndb

class Importer(ndb.Model):
    @classmethod
    def delete_all(self, Model):
        """Deletes all records for a given model"""
        ndb.delete_multi(
            Model.query().fetch(keys_only=True)
        )