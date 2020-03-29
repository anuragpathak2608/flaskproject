from sqlalchemy import Column, Integer, String, ForeignKey\
    , DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()


#Each class in model.py is table.
#Each data member in class is a column
class Tasks(Base):
    __tablename__ = "tasks"
    tid = Column("tid", Integer, nullable=False, primary_key=True, autoincrement=True)
    ttitle = Column("ttitle", String(50), nullable=False)
    tdesc = Column("tdesc", String(500), nullable=False)
    tcreatedbyuser = Column("tcreatedbyuser", String(30), nullable=False)
    tcreatedondate = Column("tcreatedondate", String, nullable=True)
    tisdeleted = Column("tisdeleted", Boolean,nullable=False, default=False)
    tisdone = Column("tisdone", Boolean, nullable=True, default=False)


    #Tasks class constructor used for taking the input from JSOn
    def __init__(self, data):
       #self.tid = data["tid"]
        self.ttitle = data[1]
        self.tdesc = data[2]
        self.tcreatedbyuser = data[0]
       #self.tcreatedondate = data["tcreatedondate"]
        self.tisdeleted = data[3]
        self.tisdone = data[4]


    #Task Class serializer to convert the Pythton object back to the the json format
    def serialize(self):
        return {
            "id": self.tid,
            "title": self.ttitle,
            "description": self.tdesc,
            "user": self.tcreatedbyuser,
            "created_on": self.tcreatedondate,
            "is_deleted": self.tisdeleted,
            "is_done": self.tisdone
         }


#user table with columns details.
class Users(Base):
    __tablename__ = "users"
    uid = Column("uid", Integer, nullable=False, primary_key=True, autoincrement=True)
    uname = Column("uname", String(30), nullable=False)
    uemail = Column("uemail", String(50))


    #Users call constructor to read the input from the json.
    def __init__(self, user_data):
        # self.uid = user_data["uid"]
        self.uname = user_data[0]
        self.uemail = user_data[1]


    #user clalss serializer to convert python object back to the json format
    def serialize(self):
        return {
            "id": self.uid,
            "name": self.uname,
            "email": self.uemail
        }


#database connection
if __name__ == "__main__":
    engine = create_engine("sqlite:///todo.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()

