class DataSize:

    def __init__(self, data_size_mb):
        self.data_size_mb = 0 if data_size_mb is None else float(data_size_mb)

    def to_kb(self):
        data_size_kb = self.data_size_mb * 1024
        return f"{data_size_kb:.2f} KB"

    def to_mb(self):
        return f"{self.data_size_mb:.2f} MB"

    def to_gb(self):
        data_size_gb = self.data_size_mb / 1024
        return f"{data_size_gb:.2f} GB"

    def to_tb(self):
        data_size_tb = self.data_size_mb / 1024 / 1024
        return f"{data_size_tb:.2f} TB"

    def auto_format(self):
        bigger_then_onegb = (self.data_size_mb / 1024) > 1
        bigger_then_onetb = (self.data_size_mb / 1024 / 1024) > 1
        formatted_data_size = "Error"
        if self.data_size_mb < 1:
            formatted_data_size = self.to_kb()
        elif bigger_then_onegb:
            if bigger_then_onetb:
                formatted_data_size = self.to_tb()
            else:
                formatted_data_size = self.to_gb()
        else:
            formatted_data_size = self.to_mb()

        return formatted_data_size
