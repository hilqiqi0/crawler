# -*- coding: utf-8 -*-

# Model of sqlalchemy , can be removed if mysql not needed

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlalchemyHelper:
    def __init__(self, SqlalchemyDatabaseUrl, DeclarativeBase, NewTable):
        self.engine = create_engine(SqlalchemyDatabaseUrl)
        self.declarative_base = DeclarativeBase
        self.Session = sessionmaker(bind=self.engine)
        self.create_table()
        self.NewTable = NewTable

    def create_table(self):
        self.declarative_base.metadata.create_all(self.engine)

    # 插入数据
    def insert_item(self, Dataitem):
        session = self.Session()
        try:
            session.merge(Dataitem)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # 更新数据
    def updata_item(self, name, value, **kwargs):
        session = self.Session()
        if name == 'blbl':
            result = session.query(self.NewTable).filter_by(aid=value).first()

        try:
            result.aid = kwargs["aid"]
            result.title = kwargs["title"]
            result.cid = kwargs["cid"]
            result.copyright = kwargs["copyright"]
            result.tname = kwargs["tname"]
            result.videos = kwargs["videos"]
            result.ctime = kwargs["ctime"]
            result.pubdate = kwargs["pubdate"]
            result.duration = kwargs["duration"]
            result.coin = kwargs["coin"]
            result.favorite = kwargs["favorite"]
            result.likes = kwargs["likes"]
            result.archive = kwargs["archive"]

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # 查找匹配数据
    def findMatch(self, field, value):
        session = self.Session()
        info = session.query(self.NewTable).filter(field == value).first()
        session.close()
        return info
    # 查找匹配数据
    def findMatch2(self, field1, value1, field2, value2):
        session = self.Session()
        info = session.query(self.NewTable).filter(field1 == value1, field2 == value2).first()
        session.close()
        return info

if __name__ == '__main__':
    # sqlalchemyhelper = SqlalchemyHelper(settings.SQLALCHEMY_DATABASE_URI_1, BasicInformation, basic_info_base)
    # print sqlalchemyhelper.findMatch(basic_info_base.comic_id, '536658')
    # print sqlalchemyhelper.findMatch2(basic_info_base.comic_id, '536658', basic_info_base.chapters_count, 323).chapters_count

    # sqlalchemyhelper = SqlalchemyHelper(settings.SQLALCHEMY_DATABASE_URI_1, KkBasicInformation, Kk_basic_info_base)
    # print sqlalchemyhelper.findMatch2(Kk_basic_info_base.comic_id, "906",
    #                             Kk_basic_info_base.chapters_count, 52
    #                             )
    # item = sqlalchemyhelper.findMatch("895639657")
    #
    # print sqlalchemyhelper.findMatch("8956396")

    # sqlalchemyhelper.updata_item("895639657")

    # d_info= {'books': '',
    #          'content_path': 'tieba/html/samanhua/tieba-baidu-com@p@5908319700.txt',
    #          'download_time': datetime.datetime(2018, 10, 11, 11, 51, 39, 314000),
    #          'image_paths': 'tieba/image/samanhua/5908319700/d6bcc3dc4a14f6b8bc93e11c82bce42b6a22f2ca-300x481.jpg;tieba/image/samanhua/5908319700/fa351384621831b8dfdf373ab0c6b9f85f581227-500x683.jpg;tieba/image/samanhua/5908319700/589b3bc9481532768b53426784a6174888519b1a-500x683.jpg;tieba/image/samanhua/5908319700/d3af97c53a307d3a76929dcf6f578bbb368e8d1b-300x779.jpg;tieba/image/samanhua/5908319700/e085ac8e3400b724480915efa7e3d542ccf1efcc-500x683.jpg;tieba/image/samanhua/5908319700/d0faccd2ba534df64ae0787f5e6ae5fc961e87aa-500x683.jpg;tieba/image/samanhua/5908319700/0ec35454faf12857f771d0642205ac3caeba320d-500x683.jpg;tieba/image/samanhua/5908319700/c984b025d2ed5baefc0de48f09a44096df013e1f-500x683.jpg;tieba/image/samanhua/5908319700/dc1a615b2ddc2099d404bd349f2e9869c191030d-500x683.jpg;tieba/image/samanhua/5908319700/d8795ba3cb65c8f09d413022a5ee3bf0ea913536-500x699.jpg;tieba/image/samanhua/5908319700/57ec66eb0d3c62b70ab76a686704d454ec1b6909-500x683.jpg',
    #          'image_urls': u'https://imgsa.baidu.com/forum/w%3D580/sign=aba1db53f0faaf5184e381b7bc5594ed/8dd0af096b63f6240eda4a768a44ebf81b4ca30b.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=320f006604f79052ef1f47363cf2d738/dbc05afbfbedab6411e43eb5fa36afc378311e7b.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=35638f52723e6709be0045f70bc69fb8/733b20adcbef7609d9d3eaea23dda3cc7dd99e3e.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=76c607719a0a304e5222a0f2e1c9a7c3/eeec86dda144ad34d25bf4f2dda20cf430ad852a.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=a581adbd174c510faec4e21250582528/61d89b82b9014a90d4c635c8a4773912b21bee1e.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=73ad937a8a94a4c20a23e7233ef41bac/300dc4628535e5dd4234d7aa7bc6a7efcf1b62fe.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=69ba97567ef082022d9291377bfafb8a/29818358d109b3de5873971dc1bf6c81820a4cc2.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=44a376e8c6ef76093c0b99971edca301/6e10b8ec8a1363272a87b0469c8fa0ec09fac7a8.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=769a8eaf18ce36d3a20483380af33a24/49b5cbb44aed2e73a6fbf4598a01a18b86d6fa80.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=c863b49bb98f8c54e3d3c5270a292dee/89eb7a600c3387448cca5d095c0fd9f9d62aa083.jpg;https://imgsa.baidu.com/forum/w%3D580/sign=ad6df49b9182d158bb8259b9b00b19d5/453c2b87e950352aba38577d5e43fbf2b3118bbd.jpg',
    #          'src_url': 'https://tieba.baidu.com/p/5909289892',
    #          'title': u'\u98d2\u6f2b\u753b\u7b2c299\u671f\u9898\u56fe'
    #          }
    # d_info['src_url_crc32'] = zlib.crc32(to_bytes(d_info["src_url"]))
    # d_info['download_time'] = datetime.datetime.now()
    # print type(d_info)
    # print sqlalchemyhelper.findMatch(d_info['src_url_crc32'])
    # if not sqlalchemyhelper.findMatch(d_info['src_url_crc32']):
    #     print("数据库中未查询到url：{}，需要添加。。。".format(d_info["src_url"]))
    # else:
    #     print("数据库中已有该url：{}，更新该记录。。。".format(d_info["src_url"]))
    #     sqlalchemyhelper.updata_item(d_info['src_url_crc32'],
    #                                  books=d_info["books"],
    #                                  image_urls=d_info["image_urls"],
    #                                  image_paths=d_info["image_paths"],
    #                                  download_time=d_info["download_time"]
    #                                  )

    # url = "https://tieba.baidu.com/p/5883917202"
    # result_info = sqlalchemyhelper.findMatch(zlib.crc32(to_bytes(url)))
    # image = ["https://imgsa.baidu.com/forum/w%3D580/sign=be7afe6675f0f736d8fe4c093a55b382/ffc508d8bc3eb13526e47fa2ab1ea8d3fc1f44d3.jpg",
    #         "https://gsp0.baidu.com/5aAHeD3nKhI2p27j8IqW0jdnxx1xbK/tb/editor/images/client/image_emoticon25.png",
    #         "https://gsp0.baidu.com/5aAHeD3nKhI2p27j8IqW0jdnxx1xbK/tb/editor/images/client/image_emoticon25.png"
    #          ]
    # if result_info:
    #     print("数据库中已有该url：{}，进行图片下载去重。。。".format(url))
    #     print(result_info.image_urls)
    #     print(type(result_info.image_urls))
    #     old = result_info.image_urls.split(";")
    #     print len(old)
    #     for i in image:
    #         if i in old:
    #             old.remove(i)
    #     print len(old)
    pass
