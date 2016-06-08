# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure_db(app):
    db.init_app(app)


class TimestampMixin(object):

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now,
                         onupdate=datetime.now)


class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'

    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, unique=True)
    bkp_type = db.Column(db.Integer, nullable=False)
    type_code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Record({}, {} {})>".format(self.user_code,
            self.datetime.isoformat(' '), "OUT" if self.type_code else "IN")


class Employee(db.Model, TimestampMixin):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.UnicodeText, nullable=False)
    last_name = db.Column(db.UnicodeText, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    cuil = db.Column(db.String(11), nullable=False)
    user_code = db.Column(db.Integer)
    file_no = db.Column(db.Integer)

    records = db.relationship(
        AttendanceRecord,
        primaryjoin=user_code == db.foreign(AttendanceRecord.user_code),
        backref='employee', lazy='dynamic'
    )

    @property
    def name(self):
        return ", ".join([self.last_name, self.first_name])

    @property
    def age(self):
        today = date.today()
        return relativedelta(today, self.birth_date)

    @property
    def seniority(self):
        today = date.today()
        return relativedelta(today, self.hire_date)

    def month_records(self, year, month):
        return self.records\
                .filter(db.extract('year', AttendanceRecord.datetime)==year)\
                .filter(db.extract('month', AttendanceRecord.datetime)==month)

    def __repr__(self):
        return "<Employee '{}', age {}>".format(self.name, self.age.years)
