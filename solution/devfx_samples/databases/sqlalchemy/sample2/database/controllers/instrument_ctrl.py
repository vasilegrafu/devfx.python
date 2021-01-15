import devfx.databases.sqlalchemy as sa
from ..models import Instrument

"""------------------------------------------------------------------------------------------------
"""
class InstrumentCtrl(object):  
    def __init__(self, dbsession):
        self.__dbsession = dbsession

    """----------------------------------------------------------------
    """
    def save(self, instance):
        existing_instance = self.getByCode(instance.code)
        if(existing_instance is not None):
            existing_instance.copy_from(instance)
        else:
            self.__dbsession.add(instance)

    def saveAll(self, instances):
        for instance in instances:
            self.save(instance)

    """----------------------------------------------------------------
    """
    def deleteById(self, id):
        self.__dbsession.delete(self.getById(id))

    def deleteByCode(self, code):
        self.__dbsession.delete(self.getByCode(code))

    """----------------------------------------------------------------
    """
    def getById(self, id, projection=(Instrument, )):
        return self.__dbsession.query(*projection) \
                    .filter(Instrument.id == id) \
                    .one_or_none()

    """----------------------------------------------------------------
    """
    def getByCode(self, code, projection=(Instrument, )):
        return self.__dbsession.query(*projection) \
                    .filter(Instrument.code == code) \
                    .one_or_none()

    """----------------------------------------------------------------
    """
    def getAll(self, projection=(Instrument, )):
        return self.__dbsession.query(*projection) \
                    .to_list()


    """------------------------------------------------------------------------------------------------
    """
    class __querier(object):  
        def __init__(self, dbsession):
            self.__dbsession = dbsession

        """----------------------------------------------------------------
        """
        def getAll(self, projection=(Instrument, ), index_col=None):
            return self.__dbsession.query(*projection) \
                        .to_dataframe(index_col=index_col)

    """----------------------------------------------------------------
    """
    @property
    def querier(self):
        return InstrumentCtrl.__querier(self.__dbsession)
