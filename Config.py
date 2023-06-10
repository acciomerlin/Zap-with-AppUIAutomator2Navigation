class Config(object):
    def __init__(self):
        self.CLICK_MAX_CNT = 4
        self.sleep_time_sec = 2

        # self.target_pkg_name = "com.example.myapplication"
        self.target_pkg_name = "com.alibaba.android.rimet"
        # self.target_pkg_name = "net.csdn.csdnplus"
        # self.target_pkg_name = "com.sina.weibo"
        # self.target_pkg_name = "com.youku.phone"
        # self.target_pkg_name = "cn.damai"
        # self.target_pkg_name = "com.ss.android.lark"
        # self.target_pkg_name = "com.cloudy.component"
        # self.target_pkg_name = "com.jingyao.easybike"
        # self.target_pkg_name = "com.cainiao.wireless"
        # self.target_pkg_name = "com.xingin.xhs"
        # self.target_pkg_name = "com.yipiao"
        # self.target_pkg_name = "app.podcast.cosmos"
        # self.target_pkg_name = "com.hunantv.imgo.activity"


    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            Config._instance = object.__new__(cls)
        return Config._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Config, '_instance'):
            Config._instance = Config(*args, **kwargs)
        return Config._instance

    def get_target_pkg_name(self):
        return self.target_pkg_name

    def get_CLICK_MAX_CNT(self):
        return self.CLICK_MAX_CNT

    def get_sleep_time_sec(self):
        return self.sleep_time_sec