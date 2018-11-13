# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, TEXT, VARCHAR, DATETIME, BigInteger
from sqlalchemy.ext.declarative import declarative_base

bilibiliInformation = declarative_base()

class bilibili_info_base(bilibiliInformation):
    __tablename__ = "bili_info"
    id = Column('id', Integer(), autoincrement=True, primary_key=True)
    title = Column("title", TEXT())                                         # 标题
    aid = Column('aid', Integer(), unique=True)                             # aid
    cid = Column("cid", TEXT())                                             # cid
    copyright = Column("copyright", TEXT())                                 # 版权：1、可以正常转载；2、无法转载
    tname = Column("tname", TEXT())                                         # 类别
    videos = Column("videos", Integer())                                    # page数量
    ctime = Column("ctime", DATETIME())                                     # 创建时间
    pubdate = Column("pubdate", DATETIME())                                 # 更新时间
    duration = Column("duration", Integer())                                # 视频时长
    coin = Column("coin", Integer())                                        # 硬币
    favorite = Column("favorite", BigInteger())                             # 好评
    likes = Column("likes", BigInteger())                                   # 收藏
    archive = Column("archive", TEXT())                                     # 全部信息
    update_time = Column("update_time", DATETIME())



