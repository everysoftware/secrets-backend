from secrets_app.skeleton import SkeletonBase

PrimaryKey = int


class Base(SkeletonBase):
    __abstract__ = True