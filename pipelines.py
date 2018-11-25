import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setting import db_host, db_user, db_pawd, db_name, db_port
from models import Job51
from job51_main import job51


class Job51Pipeline(object):
    def __init__(self, vip_name, user_name, user_password, dama_user_name, dama_password, dama_id):
        self.session = self.connect_sql()
        self.vip_name = vip_name
        self.user_name = user_name
        self.user_password = user_password
        self.dama_user_name = dama_user_name
        self.dama_password = dama_password
        self.dama_id = dama_id

    def process_item(self):
        data_dict_list = job51(vip_name=self.vip_name, user_name=self.user_name, user_password=self.user_password,
                               dama_user_name=self.dama_user_name, dama_password=self.dama_password,
                               dama_id=self.dama_id)
        if data_dict_list:
            for data_dict in data_dict_list:
                info = Job51(
                    update_time=data_dict.get("update_time", "-1"),
                    seek_name=data_dict.get("seek_name", "-1"),
                    tag=data_dict.get("tag", "-1"),
                    telephone=data_dict.get("telephone", "-1"),
                    mail=data_dict.get("mail", "-1"),
                    gender=data_dict.get("gender", "-1"),
                    age_birthday=data_dict.get("age_birthday", "-1"),
                    now_address=data_dict.get("now_address", "-1"),
                    work_experience=data_dict.get("work_experience", "-1"),
                    recent_work_time=data_dict.get("recent_work_time", "-1"),
                    position=data_dict.get("position", "-1"),
                    professional=data_dict.get("professional", "-1"),
                    company=data_dict.get("company", "-1"),
                    school=data_dict.get("school", "-1"),
                    industry=data_dict.get("industry", "-1"),
                    edu_background=data_dict.get("edu_background", "-1"),
                )
                try:
                    self.session.add(info)
                    self.session.commit()
                    print("数据库插入成功!!!!!!!!!!!!!!!!")
                except Exception as e:
                    print("数据库插入异常{}".format(e))
                    self.session.rollback()

    @staticmethod
    def connect_sql():
        while True:
            try:
                engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
                                       .format(db_user, db_pawd, db_host, db_port, db_name),
                                       max_overflow=500, pool_timeout=120, pool_recycle=3600, echo=False)
                db_session = sessionmaker(bind=engine)
                return db_session()
            except Exception as conn_err:
                print("数据库连接异常：{} {}秒后重新尝试连接".format(conn_err, 2))
                time.sleep(2)


if __name__ == '__main__':
    # dama_id去超级鹰用户中心>>软件ID 生成一个替换 96001
    call = Job51Pipeline(vip_name="锐力信息西安", user_name="锐力", user_password="sxruilixx01",
                         dama_user_name="jianjian1", dama_password="ljgcvbcss@*", dama_id="897833")

    call.process_item()
