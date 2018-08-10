class http_state:
    Success="Success"
    Faile="Faile"

class img_file_path:
    File_Train="D:\\Data\\ai\\lenet\\train"
    File_Test="D:\\Data\\ai\\lenet\\test"

class httpResultWhiteMsg:
    @staticmethod
    def send(value):
        return '<div style="color:#fff;font-size:36px;">'+value+'</div>'
