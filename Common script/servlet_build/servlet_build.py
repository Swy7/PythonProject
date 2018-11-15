import os
import shutil

class ServletBuild(object):
  def __init__(self):
    self.build_path = ""
    self.project_name = ""
    self.package_name = ""
    self.dir_path = ["build/classes",
              "src/{0}/dao/daoImp",
              "src/{0}/domain",
              "src/{0}/service/serviceImp",
              "src/{0}/test",
              "src/{0}/utils",
              "src/{0}/web/filter",
              "src/{0}/web/servlet",
              "web/admin",
              "web/js",
              "web/css",
              "web/fonts",
              "web/img",
              "web/upload",
              "web/jsp",
              "web/WEB_INF/lib",
            ]
    self.file_path=[("InitStaticFile/index.jsp","web/index.jsp"),
              ("InitStaticFile/web.xml","web/WEB_INF/web.xml"),
            ]

  @staticmethod
  def check_path(path):
    if not os.path.exists(path):
      print(path+"路径不存在")
      return False
    elif not os.access(path,os.R_OK|os.W_OK):
      print(path + "路径无读写权限")
      return False
    else:
      return True

  def prepare_input(self):
    input_str = input("初始化(根目录绝对地址+项目名+src包名)\n"
                      "例:  /root/java + javaweb + com.java.myproject:\n")
    input_list = list(map(lambda x:x.strip(),input_str.split("+")))
    if len(input_list) == 3:
      self.build_path = os.path.abspath(input_list[0].replace("\\","/"))
      self.project_name = input_list[1]
      self.package_name = input_list[2].replace(".","/")
    else:
      print("输入根目录+项目名+src包名,用+号隔开")

  def build_servlet(self):
    current_path = os.getcwd()
    if self.check_path(self.build_path):
      project_path = os.path.join(self.build_path,self.project_name)
      if not os.path.isdir(project_path):
        os.mkdir(project_path)
      for i in self.dir_path:
        temp_path = os.path.join(project_path,i.format(self.package_name))
        if not os.path.isdir(temp_path):
          os.makedirs(temp_path)
      for i in self.file_path:
        from_path = os.path.join(current_path,i[0])
        to_path = os.path.join(project_path,i[1])
        if self.check_path(from_path) and os.path.isfile(from_path):
          shutil.copy(from_path,to_path)
      print("初始化完成")

if __name__ == "__main__":
  sb = ServletBuild()
  sb.prepare_input()
  sb.build_servlet()
