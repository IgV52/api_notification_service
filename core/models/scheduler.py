from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from core.shemas.dispath import Dispath, DispathUpdate

import settings

class Scheduler:
    __jobstores = {
            'default': SQLAlchemyJobStore(url=settings.URL_SCHEDULER)
        }
    __job_defaults = {
            'coalesce': False,
            'max_instances': 5
        }
    _scheduler = AsyncIOScheduler(jobstores=__jobstores, job_defaults=__job_defaults, replace_existing=True)
    _scheduler_test = AsyncIOScheduler()

    @classmethod
    def add_task(cls, func: 'function', dispath: Dispath):
        settings = {
                    'start_time': dispath.start_sending, 
                    'end_time': dispath.end_sending, 
                    'id': dispath.number,
                    'filter': dispath.filter, 
                    'text': dispath.text,
                }
        cls._scheduler.add_job(func,trigger='interval', kwargs=settings, seconds=2, 
        start_date=settings['start_time'], end_date=settings['end_time'], id=str(settings['id']))

    @classmethod
    def delete_task(cls, task_id: str):
        cls._scheduler.remove_job(job_id=task_id)
        
    @classmethod
    def init_scheduler(cls):
        cls._scheduler.start()
    
    @classmethod
    def init_scheduler_test(cls):
        cls._scheduler = cls._scheduler_test
        cls._scheduler_test.start()

    @classmethod
    def modify_task(cls, func: 'function', task_id: int, dispath: DispathUpdate):
        update_dispath = Dispath(
                    start_sending=dispath.start_sending, 
                    end_sending=dispath.end_sending,
                    number=task_id,
                    filter=dispath.filter, 
                    text=dispath.text,
                    )
        job_id = str(task_id)
    
        cls.delete_task(job_id)
        cls.add_task(func, update_dispath)

    @classmethod
    def reload_scheduler(cls):
        cls._scheduler.pause()
        cls._scheduler.resume()
