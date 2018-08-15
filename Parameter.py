class http_state:
    Success="Success"
    Faile="Faile"

class img_file_path:
    File_Train="D:\\Data\\ai\\lenet\\train"
    File_Test="D:\\Data\\ai\\lenet\\test"

class httpResultWhiteMsg:
    @staticmethod
    def send(value):
        return '<div style="color:red;font-size:36px;">'+value+'</div>'

class Parameters:
    host='172.30.53.250'
    port=8899
    TensorBoard_port=6006
    model_path="D:\\Data\\ai\\model\\traffic_sign.model"
    user="admin"
    pwd="admin"
    object_map={"000":"driverCard","001":"hkb","002":"idcard","003":"jhz",
                "004":"relativesPhoto","005":"socialSecurity","006":"vehicleCard"}
    logdir="D:\\Data\\ai\\log"

