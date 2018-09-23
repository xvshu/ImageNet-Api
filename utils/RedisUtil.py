import redis
from  utils import CfgUtil

class RedisUtil(object):
    __pool = None
    imagenet_key=None

    def __init__(self):
        # Redis地址
        host = CfgUtil.get_cfg("redis_host")
        # Redis端口
        port = int(CfgUtil.get_cfg("redis_port"))
        db = int(CfgUtil.get_cfg("redis_db"))
        self.__pool = redis.ConnectionPool(host=host, port=port,db=db)
        # self.imagenet_key="EAI_JGZ_ImageNet_fic_xs_"

    # 保存数据
    # expire：过期时间，单位秒
    def r_set(self, key, value, expire=None):
        redi = redis.Redis(connection_pool=self.__pool)
        redi.set(key, value, ex=expire)

    # 获取数据
    def r_get(self, key):
        redi = redis.Redis(connection_pool=self.__pool)
        value = redi.get(key)
        if value is None:
            return None
        value = value.decode("UTF-8")
        return value

    # 删除数据
    def r_del(self, key):
        redi = redis.Redis(connection_pool=self.__pool)
        redi.delete(key)

    def h_set(self,name,val_key,val_value):
        redi = redis.Redis(connection_pool=self.__pool)
        redi.hset(name=name,key=val_key,value=val_value)

    def h_get(self,name,val_key):
        redi = redis.Redis(connection_pool=self.__pool)
        value = redi.hget(name=name,key=val_key)
        if value is None:
            return None
        value = value.decode("UTF-8")
        return value

    def h_exists(self,name,val_key):
        redi = redis.Redis(connection_pool=self.__pool)
        return redi.hexists(name=name,key=val_key)

    def h_getall(self,name):
        redi = redis.Redis(connection_pool=self.__pool)
        map_all=redi.hgetall(name=name)
        map_out={}
        for one_key in map_all:
            map_out[str(one_key, encoding = "utf8")]=str(map_all[one_key], encoding = "utf8")
        return map_out

    def h_del(self,name,val_key):
        redi = redis.Redis(connection_pool=self.__pool)
        redi.hdel(name=name,keys=val_key)

    def h_delall(self):
        redi = redis.Redis(connection_pool=self.__pool)
        redi.hdel("*","*")

    def l_push(self,name,value):
        redi = redis.Redis(connection_pool=self.__pool)
        redi.lpush(name,value)

    def l_exists(self,name,value):
        redi = redis.Redis(connection_pool=self.__pool)
        allclass  = redi.lrange(name=name,start=0,end=-1)
        for oneC in allclass:
            s_oneC=str(oneC, encoding = "utf8")
            if(value == s_oneC):
                return True
        return False

    def l_getall(self,name):
        redi = redis.Redis(connection_pool=self.__pool)
        allclass  = redi.lrange(name=name,start=0,end=-1)
        all_out=[]
        for one_vl in allclass:
            all_out.append(str(one_vl, encoding = "utf8"))
        return all_out

    def l_len(self,name):
        redi = redis.Redis(connection_pool=self.__pool)
        len  = redi.llen(name=name)
        return len

    def delete(self,name):
        redi = redis.Redis(connection_pool=self.__pool)
        len  = redi.delete(name)
        return len






