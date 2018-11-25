import datetime
from sqlalchemy import Column, String, create_engine, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from setting import db_host, db_user, db_pawd, db_name, db_port

# 创建对象的基类:
Base = declarative_base()


# job51
class Job51(Base):
    # 表的名字:
    __tablename__ = 'JOB51_data'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    update_time = Column(String(255), index=True, comment="简历更新时间")
    seek_name = Column(String(255), index=True, comment="简历人名")
    tag = Column(String(255), index=True, comment="标签")
    telephone = Column(String(255), index=True, comment="电话")
    mail = Column(String(255), index=True, comment="邮箱")
    gender = Column(String(255), index=True, comment="性别")
    age_birthday = Column(String(255), index=True, comment="年龄")
    now_address = Column(String(255), index=True, comment="现住地址")
    work_experience = Column(String(255), index=True, comment="工作年限")
    recent_work_time = Column(String(255), index=True, comment="最近工作时间")
    position = Column(String(255), index=True, comment="在职岗位")
    professional = Column(String(255), index=True, comment="专业")
    company = Column(String(255), index=True, comment="所在公司")
    school = Column(String(255), index=True, comment="学校")
    industry = Column(String(255), index=True, comment="行业")
    edu_background = Column(String(255), index=True, comment="教育背景")
    add_time = Column(DateTime, default=datetime.datetime.now, comment="数据入库时间")


if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                           .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    Base.metadata.create_all(engine)
