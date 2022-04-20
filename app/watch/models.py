from email.policy import default
import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config

settings = config.get_settings()


class WatchEvent(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    event_id = columns.TimeUUID(
        clustering_order="DESC", primary_key=True, default=uuid.uuid1)
    user_id = columns.UUID(primary_key=True)
    path = columns.Text()
    start_time = columns.Double()
    end_time = columns.Double()
    duration = columns.Double()
    complete = columns.Boolean(default=False)

    @property
    def completed(self):
        return (self.duration * 0.97) < self.end_time

    @staticmethod
    def get_resume_time(host_id, user_id):
        resume_time = 0
        watchObj = WatchEvent.objects.allow_filtering().filter(
            host_id=host_id, user_id=user_id).first()
        if watchObj is not None:
            if not watchObj.complete or not watchObj.completed:
                resume_time = watchObj.end_time
        return resume_time