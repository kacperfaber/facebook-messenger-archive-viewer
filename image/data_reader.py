import base64


# noinspection PyMethodMayBeStatic
class DataReader:
    def read_data_as_base64(self, file: str) -> str:
        with open(file, 'rb') as f:
            return base64.b64encode(f.read()).decode("utf-8")
