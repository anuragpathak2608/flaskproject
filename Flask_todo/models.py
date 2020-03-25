from sqlalchemy import Column, Integer, String, ForeignKey\
    , Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "tasks"
    tid = Column(Integer, nullable= False, primary_key= True)
    ttitle = Column(String(50), nullable=False)
    tdesc = Column(String(500), nullable=False)
    tcreatedbyuser = Column(String(30), nullable=False)
    tcreatedondate = Column(Date, nullable=False)
    tisdeleted = Column(Boolean,nullable=False)
    tisdone = Column(Boolean, nullable=True)

    def __init__(self, tid, ttitle, tdesc, tcreatedbyuser, tcreatedondate, tisdeleted, tisdone):
        self.tid = tid
        self.ttitle = ttitle
        self.tdesc = tdesc
        self.tcreatedbyuser = tcreatedbyuser
        self.tcreatedondate = tcreatedondate
        self.tisdeleted = tisdeleted
        self.tisdone = tisdone

    def serialize(self):
        return {
            "id": self.tid,
            "title": self.ttitle,
            "describtiom": self.tdesc,
            "user": self.tcreatedbyuser,
            "createdon": self.tcreatedondate,
            "deleted": self.tisdeleted,
            "done": self.tisdone
        }


class Users(Base):
    __tablename__ = "users"
    uid = Column(Integer, nullable=False, primary_key=True)
    uname = Column(String(30), nullable=False)
    uemail = Column(String(50))

    def __init__(self, uid, uname, uemail):
        self.uid = uid
        self.uname = uname
        self.uemail = uemail



