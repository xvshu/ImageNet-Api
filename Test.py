from utils import RedisUtil
from Parameter import Parameters

def test_redis_1():
    redi = RedisUtil.RedisUtil()
    # redi.delete(Parameters.redis_key_img_labletonum)
    # redi.delete(Parameters.redis_key_img_AllClass)
    #
    #
    #
    # # print("begin init redis Object")
    # for oneMapkey in Parameters.object_map:
    #     print(oneMapkey)
    #     print(Parameters.object_map[oneMapkey])
    #     redi.l_push(name=Parameters.redis_key_img_AllClass,value=str(Parameters.object_map[oneMapkey]))
    #     redi.h_set(name=Parameters.redis_key_img_labletonum,val_key=str(oneMapkey),val_value=str(Parameters.object_map[oneMapkey]))

    mapall = redi.h_getall(name=Parameters.redis_key_img_labletonum)
    redi.h_del(name=Parameters.redis_key_img_labletonum)

    # print(mapall)
    # print(redi.h_get(name=Parameters.redis_key_img_labletonum,val_key="000"))
    # print(redi.h_exists(name=Parameters.redis_key_img_labletonum,val_key="000"))
    #
    # print(redi.l_exists(name=Parameters.redis_key_img_AllClass,value="hkb"))
    # print(redi.l_getall(name=Parameters.redis_key_img_AllClass))
    # print(redi.l_len(name=Parameters.redis_key_img_AllClass))

def dele_ai():
    redi = RedisUtil.RedisUtil()
    redi.h_delall()
    mapall = redi.h_getall(name=Parameters.redis_key_img_labletonum)
    print(mapall)






if __name__ == '__main__':
    dele_ai()