import csv
import glob
import json
import os
import subprocess
import pandas as pd

class DataHandler:
    def __init__(self, sheet_names):
        # Initialize a DataFrame for each sheet
        self.dfs = {name: pd.DataFrame(columns=['approach','project','version','code_entity','linenum', 'mutant_id', 'akf', 'akp', 'anf', 'anp', 'Sus']) for name in sheet_names}

    def add_data(self, sheet_name, data_dict):
        # Append new data to the specified DataFrame
        self.dfs[sheet_name] = self.dfs[sheet_name].append(data_dict, ignore_index=True)

    def save_data(self, filename):
        # Save all DataFrames to an Excel file, each DataFrame to a different sheet
        with pd.ExcelWriter(filename) as writer:
            for name, df in self.dfs.items():
                df.to_excel(writer, sheet_name=name, index=False)
    def merge_data(self, other_handler):
        # Merge DataFrames from another DataHandler instance
        for sheet_name, df in other_handler.dfs.items():
            if sheet_name in self.dfs:
                # Concatenate dataframes if the sheet name already exists
                self.dfs[sheet_name] = pd.concat([self.dfs[sheet_name], df]).reset_index(drop=True)
            else:
                # Otherwise, just add the new dataframe
                self.dfs[sheet_name] = df
#获取变异体结果json文件
def get_non_txt_files(folder_path):
  files = glob.glob(os.path.join(folder_path, "*"))
  non_txt_files = [os.path.basename(f) for f in files if not f.endswith('.txt') and os.path.isfile(f)]
  return non_txt_files

#找到测试用用例txt及其结果txt
def find_test_txt_files(file_path, txt_name):
  result = subprocess.run(["find", file_path, "-name", txt_name + ".txt"], stdout=subprocess.PIPE)
  txt_files = result.stdout.decode("utf-8").strip().split("\n")
  return txt_files

#逐行读取原始txt
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

#得到原版本测试用例执行结果：【测试用例：执行结果】
def get_init_test_result(cover_path):
  tests_txt = find_test_txt_files(cover_path, "all_tests")
  tests_result_txt = find_test_txt_files(cover_path, "inVector")
  # print(tests_txt, tests_result_txt)
  test_result = {}
  num = 0
  for item in range(len(tests_txt)):
    test_list = read_txt_file(tests_txt[item]) 
    result_list = read_txt_file(tests_result_txt[item])
    # print(len(test_list), len(result_list), test_list[2], 1 if test_list[2] == 'org.jfree.chart.annotations.junit.CategoryLineAnnotationTests#testCloning' else 0)
    for test_item in range(len(test_list)):
      # print(test_list[test_item], result_list[test_item])
      test_result[str(test_list[test_item])] = result_list[test_item]
      if str(result_list[test_item]) =='1':
         num += 1
      # if test_item <= 10:
      #   print(test_list[test_item], result_list[test_item])
  # print("1的数量为{}".format(num))
  return test_result

#得到变异体测试用例
def mutant_test(filename):
    with open(filename) as f:
        lines = f.readlines()

    processed_lines = []
    for line in lines:
        line = line.strip()
        left_idx = line.find("(")
        right_idx = line.find(")")
        if left_idx != -1 and right_idx != -1:
            class_name = line[:left_idx].split(".")[-1]
            method_name = line[left_idx+1:right_idx].replace(",", "#")
            processed_line = f"{method_name}#{class_name}"
            processed_lines.append(processed_line)

    return processed_lines

def Ochiai(kf, failed, killed):
    if failed == 0 or killed == 0:
      return 0
    # if kf == 0:
    #    kf = 1
    return kf / ((failed * killed) ** 0.5)

def Dstar(kf, kp, nf):
  if kp + nf == 0:
    return 0
  return (kf * kf) / (kp + nf)

def gp13(Akf, Anf, Akp, Anp):
    if (2 * Akp + Akf) == 0:
        return 0
    return Akf + (Akf / (2 * Akp + Akf))

def Jaccard(kf, kp, nf):
   if (kf + nf + kp == 0):
      return 0
   return kf / (kf + nf + kp)

def Tarantula(kf, kp, nf, np):
   if kf + kp == 0 or kf + nf == 0:
      return 0
   if kf + nf != 0 and kp + np == 0:
      return 1
   return (kf / (kf + nf)) / (kf / (kf + nf) + kp / (kp + np))

def Op2(kf, kp, np):
   return kf - kp / (kp + np + 1)

def init(handler, init_path, mutant_path, mutant_result_path, vid, pid, approach):
  print(init_path, os.path.exists(init_path))
  print(mutant_path, os.path.exists(mutant_path))
  print(mutant_path + '/all_tests', os.path.exists(mutant_path + '/all_tests'))
  if not os.path.exists(init_path) or not os.path.exists(mutant_path) or not os.path.exists(mutant_path + '/all_tests'):
    print("路径缺失")
    return 
  print(pid, vid)
  initresult = get_init_test_result(init_path) #Gzotar工具获取的所有测试用例
  mutant_result = mutant_test(mutant_path + '/all_tests') #执行源程序test后获得的测试用例
  # print(result)
  # print(mutant_result)
  # 
  mixtest = []  #给 initresult 和 mutant_result求一个交集
  # susdic_Oc = {}
  # susdic_Ds = {}
  # susdic_Ja = {}
  # susdic_Op = {}
  # susdic_Ta = {}
  # susdic_Gp = {}
  # avg_susdic_Oc = {}
  # avg_susdic_Ds = {}
  # avg_susdic_Ja = {}
  # avg_susdic_Op = {}
  # avg_susdic_Ta = {}
  # avg_susdic_Gp = {}
  # num_susdic_Oc = {}
  # num_susdic_Ds = {}
  # num_susdic_Ja = {}
  # num_susdic_Op = {}
  # num_susdic_Ta = {}
  # num_susdic_Gp = {}
  for key in initresult.keys():
     if key in mutant_result:
        mixtest.append(key)
  for item in mutant_result:
     if item in initresult and item not in mixtest:
        mixtest.append(key)
  # print(len(result), len(mutant_result), len(mixtest))
  mutant_result_json = get_non_txt_files(mutant_result_path) # 变异体执行结果 ['src-main-java-org-apache-commons-math3-fraction-Fraction-209-5.json', 'src-main-java-org-apache-commons-math3-fraction-BigFraction-172-19.json']
  # print(mutant_result_json)
  # input()
  # for item in mutant_result_json:
  #   line_name = "-".join(item.split("-")[:-1])
  #   susdic_Oc[line_name] = 0
  #   susdic_Ds[line_name] = 0
  #   susdic_Ja[line_name] = 0
  #   susdic_Op[line_name] = 0
  #   susdic_Ta[line_name] = 0
  #   susdic_Gp[line_name] = 0
  #   avg_susdic_Oc[line_name] = 0
  #   avg_susdic_Ds[line_name] = 0
  #   avg_susdic_Ja[line_name] = 0
  #   avg_susdic_Op[line_name] = 0
  #   avg_susdic_Ta[line_name] = 0
  #   avg_susdic_Gp[line_name] = 0
  #   num_susdic_Oc[line_name] = 0
  #   num_susdic_Ds[line_name] = 0
  #   num_susdic_Ja[line_name] = 0
  #   num_susdic_Op[line_name] = 0
  #   num_susdic_Ta[line_name] = 0
  #   num_susdic_Gp[line_name] = 0

  # 遍历变异体执行结果的每个测试类,获取每个变异体的怀疑度
  for item in mutant_result_json:
    # itme=>src-main-java-org-apache-commons-math3-fraction-Fraction-188-17.json
    line_name = "-".join(item.split("-")[:-1]) # src-main-java-org-apache-commons-math3-fraction-Fraction-188  188是这个文件对应的行号
    print(item)
    with open(mutant_result_path + '/' + item) as f:
      data = json.load(f)
      kf = nf = kp = np = 0
      for test_item in mixtest:
        # pass
        if str(initresult[test_item]) == '0':
          # if test_item.split('#')[0] in data:
          #    kp +=1
          # elif test_item in data:
          if test_item in data:
             kp += 1
          else:
             np += 1
        # fail
        elif str(initresult[test_item]) == '1':
          # print(vid + 'b', item, test_item, initresult[test_item])
          with open('/home/failingTestOutput/' + pid + '/'+ vid + 'b/failing_tests.json') as f:
            faildata = json.load(f) # 数据说明，faildata是原始文件的type1、2、3、4错误信息，会有若干个错误的测试类，组成一个大的json对象，test_item是每个测试类的名称
            # print(data)
            # input()
            # 这里如果测试的项目不在原始程序的错误测试类中,直接跳过
            if test_item not in faildata:
               continue
            if test_item in data:
              #  nf += 1
              # 下面全注释表示type1
              # if data[test_item].split('at')[0] == faildata[test_item].split('at')[0]: 
              # if data[test_item] == faildata[test_item]:pytho
              # if data[test_item]['type3'] == faildata[test_item]['type3']:
              if data[test_item]['type3'] == faildata[test_item]['type3']:
                nf += 1
              else:
                kf += 1
            else:
              kf += 1
      # 得到akf，apf，akp np的值：

      # myfile = '/home/susMaxMajorType1/' + pid + '/' + vid + 'b'
      # if not os.path.exists(myfile):
      #   os.makedirs(myfile) 
      # with open(myfile + '/b.txt', mode='a', newline='') as file:
      #   print(item, kf, kp, nf, np, file=file)
      Oc = Ochiai(kf, kf + nf, kf + kp)
      Ds = Dstar(kf, kp, nf)
      Ja = Jaccard(kf, kp, nf)
      Op = Op2(kf, kp, np)
      Ta = Tarantula(kf, kp, nf, np)
      Gp = gp13(kf, nf, kp, np)
      data_dict_Oc = {
        'approach': approach,
        'project': pid,
        'version': int(vid),
        'linenum': int(item.split('-')[-2]),
        'code_entity': "-".join(line_name.split("-")[:-1]),
        'mutant_id': item[:-5],
        'akf': kf,
        'akp': kp,
        'anf': nf,
        'anp': np,
        'Sus': Oc
      }
      data_dict_Ds = {
        'approach': approach,
        'project': pid,
        'version':int(vid),
        'linenum': int(item.split('-')[-2]),
        'code_entity': "-".join(line_name.split("-")[:-1]),
        'mutant_id': item[:-5],
        'akf': kf,
        'akp': kp,
        'anf': nf,
        'anp': np,
        'Sus': Ds
      }
      data_dict_Ja = {
        'approach': approach,
        'project': pid,
        'version':int(vid),
        'linenum': int(item.split('-')[-2]),
        'code_entity': "-".join(line_name.split("-")[:-1]),
        'mutant_id': item[:-5],
        'akf': kf,
        'akp': kp,
        'anf': nf,
        'anp': np,
        'Sus': Ja
      }
      data_dict_Op = {
        'approach': approach,
        'project': pid,
        'version': int(vid),
        'linenum': int(item.split('-')[-2]),
        'code_entity': "-".join(line_name.split("-")[:-1]),
        'mutant_id': item[:-5],
        'akf': kf,
        'akp': kp,
        'anf': nf,
        'anp': np,
        'Sus': Op
      }
      data_dict_Ta = {
        'approach': approach,
        'project': pid,
        'version': int(vid),
        'linenum': int(item.split('-')[-2]),
        'code_entity': "-".join(line_name.split("-")[:-1]),
        'mutant_id': item[:-5],
        'akf': kf,
        'akp': kp,
        'anf': nf,
        'anp': np,
        'Sus': Ta
      }
      data_dict_Gp = {
        'approach': approach,
        'project': pid,
        'version': int(vid),
        'linenum': int(item.split('-')[-2]),
        'code_entity': "-".join(line_name.split("-")[:-1]),
        'mutant_id': item[:-5],
        'akf': kf,
        'akp': kp,
        'anf': nf,
        'anp': np,
        'Sus': Gp
      }
      # 写入数据
      handler.add_data('Op2', data_dict_Op)
      handler.add_data('Ochiai', data_dict_Oc)
      handler.add_data('Dstar', data_dict_Ds)
      handler.add_data('Jaccard', data_dict_Ja)
      handler.add_data('Tarantula', data_dict_Ta)
      handler.add_data('Gp13', data_dict_Gp)

   
def process_project_versions(pid, svid, evid, handler):
    """处理特定软件项目的所有版本"""
    for i in range(svid, evid + 1):
        # 跳过忽略的版本
        # if i in list_ignore:
        #     continue
        # 处理每个版本
        process_version(pid, i, handler)

def process_version(pid, version, handler):
    """处理特定版本的数据"""
    base_path = f'/home/d4jbasecover/{pid}/{version}b'
    clean_path = f'/home/d4jclean/{pid}/{version}b'
    json_path = f'/home/mutant_result_faulty_file_json/{pid}/{version}b'
    major_json_path = f'/home/mutant_result_faulty_file_major_json/{pid}/{version}b'

    init(handler, base_path, clean_path, json_path, str(version), pid, 'mbert')
    init(handler, base_path, clean_path, major_json_path, str(version), pid, 'major')

if __name__ == '__main__':
    output_directory = "/home/d4jscript/hblscript/"
    sheet_names = ['Op2', 'Ochiai', 'Dstar', 'Jaccard', 'Tarantula', 'Gp13']
    overall_handler = DataHandler(sheet_names)  # 总体数据处理器

    # 定义项目及其版本范围
    projects = {
        'Math': (1, 106),
        'Time': (1, 27),
        'Chart': (1, 26),
        'Lang': (1, 65),
        'Mockito': (1, 38),
        'Closure': (1, 133)
    }
    for pid, (svid, evid) in projects.items():
        project_handler = DataHandler(sheet_names)  # 创建新的数据处理器
        process_project_versions(pid, svid, evid, project_handler)
        project_handler.save_data(f"{output_directory}{pid}.xlsx")  # 以项目名命名的Excel文件
        overall_handler.merge_data(project_handler)  # 将项目数据合并到总体数据处理器
    # 保存总体汇总的数据
    overall_handler.save_data(f"{output_directory}overall_summary.xlsx")
