from .dataset_iterator import DatasetIterator

class DatasetBackwardIterator(DatasetIterator):
    def __init__(self, dataset, batch_size=None):
        super().__init__(dataset=dataset, position=0, batch_size=batch_size)

    """----------------------------------------------------------------
    """
    def next(self, batch_size=None):
        if(batch_size is None):
            batch_size = self.batch_size
        if (self.position > (len(self.dataset) - 1)):
            raise StopIteration()
        start = self.count()-(self.position+1)
        stop = self.count()-(self.position+1)-batch_size if ((self.count()-(self.position+1)-batch_size) >= 0) else None
        step = -1
        data = self.dataset[start:stop:step]
        self.position += batch_size
        return data

