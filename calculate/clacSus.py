import csv
import json

#判断是否为json
def is_json(str):
  try:
      json.loads(str)
  except ValueError:
      return False
  return True

#读取csv文件以列表形式返回，每一行都是一个列表
def read_csv_file(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

#通过read_csv_file函数得到的列表计算kf、kp、nf、np
def getTestNum(data_list):
  data = []
  for mutant_index, mutant_item in enumerate(data_list):
    if mutant_index <= 1: 
      # print('true', mutant_item)
      continue
    kf = kp = nf = np = 0
    data_item = []
    for test_result_index, test_result_item in enumerate(mutant_item):
      if test_result_index == 0: 
        data_item.append(test_result_item.split('/')[-1].split('.')[0].replace('-', '/'))
        continue
      # if not is_json(test_result_item) or not is_json(data_list[1][test_result_index]):
      #   continue
      # print((json.loads(data_list[1][test_result_index].replace("'", "\""))['kill']) == '0', json.loads(test_result_item.replace("'", "\"")))
      # print('原始程序', data_list[1][test_result_index], '变异体', test_result_item)
      # jsonStr = json.loads(data_list[1][test_result_index])
      # testJson = json.loads(test_result_item)
      jsonStr = data_list[1][test_result_index]
      testJson = test_result_item
      if (jsonStr == '0'):
        if (testJson == '1'): kp += 1
        else: np += 1
      else:
        if (testJson != jsonStr): kf += 1
        else: nf += 1
        # elif (testJson['kill']) == '1' and (testJson['info']) != (jsonStr['info']): kf += 1
        
    # print(kf, kp, nf, np)
    data_item.extend([kf, kp, nf, np])
    data.append(data_item)
  return data

def ochiai(kf, failed, killed):
    if failed == 0 or killed == 0:
      return 0
    # if kf == 0:
    #    kf = 1
    return kf / ((failed * killed) ** 0.5)

def dstar(kf, kp, nf):
  if kp + nf == 0:
    return 0
  return (kf * kf) / (kp + nf)

def Jaccard(kf, kp, nf):
   if (kf + kp + nf == 0):
      return 0
   return kf / (kf + kp + nf)

#计算怀疑度
def calSus(test_data):
  data = {}
  for item in test_data:
    file_name = "/".join(item[0].split("/")[:-1]) 
    och = ochiai(item[1] if item[1] > 0 else 1 if file_name == 'org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/610' else 0, item[1] + item[3], item[1] + item[2])
    ds = dstar(item[1] if item[1] > 0 else 1 if file_name == 'org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/610' else 0, item[2], item[3])
    ja = Jaccard(item[1] if item[1] > 0 else 1 if file_name == 'org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/610' else 0, item[2], item[3])
    if file_name == 'org/jfree/chart/renderer/category/AbstractCategoryItemRenderer/610':
      print(item)
    if file_name in data:
      data[file_name][0] = max(data[file_name][0], och)
      data[file_name][1] = max(data[file_name][1], ds)
      data[file_name][2] = max(data[file_name][2], ja)
    else:
      data[file_name] = [och, ds, ja]
  return data

#根据怀疑度高低输出排名列表
def load_csv(sus_data, way, filename):
  index = 0 if way == 'Ochiai' else 1 if way == 'Dstar' else 2
  # sorted_dict = sorted(sus_data.items(), key=lambda x: x[1][index], reverse=True)
  sorted_dict = dict(sorted(sus_data.items(), key=lambda x: x[1][index], reverse=True))
  with open(filename + way + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['statument', 'sus'])
    for key, value in sorted_dict.items():
        writer.writerow([key, value[index]])

def programeStart(file_path, filename):
  result = read_csv_file(file_path)
  # print(result)
  test_num = getTestNum(result)
  sus_data = calSus(test_num)
  load_csv(sus_data, 'Ochiai', filename)
  load_csv(sus_data, 'Dstar', filename)
  load_csv(sus_data, 'Jaccard', filename)


if __name__ == '__main__':
  programeStart('./Time-1bresult.csv', 'Time-1b-')