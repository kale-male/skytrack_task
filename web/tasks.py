import operator
from datetime import datetime
from sqlalchemy import func

from app import app, make_celery, db
from models import ArithmLog

celery = make_celery(app)


@celery.task(name='mytasks.operator')
def operator_task(operator_name, a, b, ip_addr):
    res = getattr(operator, operator_name)(a, b)
    log = ArithmLog(
        param1=a,
        param2=b,
        result=res,
        operator=operator_name,
        created=datetime.utcnow(),
        ip=ip_addr
    )
    db.session.add(log)
    db.session.commit()
    return res



@celery.task(name='mytasks.stat')
def stat():
    app.logger.info(f"HELLO!!")
    res = db.session.query(
        ArithmLog.operator, func.count(ArithmLog.operator)
    ).group_by(ArithmLog.operator).all()
    # res = db.engine.execute("""
    #     SELECT count(*) AS count, operator FROM arithm_log
    #     GROUP BY operator
    # """)
    return list(res)

