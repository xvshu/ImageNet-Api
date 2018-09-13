class http_state:
    Success="Success"
    Faile="Faile"

class img_file_path:
    File_Train="/Data/servers/python/AI/train"
    File_Test="/Data/servers/python/AI/test"

class httpResultWhiteMsg:
    @staticmethod
    def send(value):
        return '<div style="color:red;font-size:36px;">'+value+'</div>'

class Parameters:
    host='192.168.2.170'
    port=8899
    model_path="/Data/servers/python/AI/model/eloancn_sign.model"
    user="admin"
    pwd="admin"
    object_map={"000":"driverCard","001":"hkb","002":"idcard","003":"jhz",
                "004":"relativesPhoto","005":"vehicleCard"}
    logdir="/Data/servers/python/AI/TensorBoard_log"
    min_num_img=10
    max_num_img=500
    redis_key_img_AllClass="AI_EL_Img_all_class"
    redis_key_img_labletonum="AI_EL_Img_label_to_num"
