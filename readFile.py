class ReadFile:
    def __init__(self, filename):
        self.filename = filename
    #处理文件路径 运行路劲和开发路径不同
    def filePaths(self):
        return [self.filename]
    def ToFile(self, content):
        with open(self.filename, 'w') as f:
            f.write(content)
    def ToExcel(self, content):
        pass
    def read(self):
        with open(self.filename, 'r') as f:
            return f.read() 
# Usage:
rf = ReadFile('myfile.txt') 
rf.read()