import json
import os
import glob

#获取变异体失败测试用例执行信息
def get_non_txt_files(folder_path):
  files = glob.glob(os.path.join(folder_path, "*"))
  non_txt_files = [os.path.basename(f) for f in files if not f.endswith('.txt') and os.path.isfile(f)]
  return non_txt_files

#读取文件内容获取失败测试用例及其报错信息
def parse_file(filename):
    with open(filename) as f:
        lines = f.readlines()

    result = {}
    key = None
    value = ""

    for line in lines:
        if line.startswith('---'):
            if key is not None:
                # key = line.replace(' ', '').replace('\n', '').replace('---', '').replace('::', '#')
                # result[key] = value.replace(' ', '').replace('\n', '').replace('\t', '')
                result[key] = {
                    # "type2" : value.split('\n')[0].split(':')[0],
                    "type3" : value.split('\n')[0].replace(' ', ''),
                    # "type4" : value.replace(' ', '').replace('\n', '').replace('\t', '')
                }
            key = line.replace(' ', '').replace('\n', '').replace('---', '').replace('::', '#')
            value = ""
        else:
            value += line

    # result[key] = value.replace(' ', '').replace('\n', '').replace('\t', '')
    result[key] = {
        # "type2" : value.split('\n')[0].split(':')[0],
        "type3" : value.split('\n')[0].replace(' ', ''),
        # "type4" : value.replace(' ', '').replace('\n', '').replace('\t', '')
    }
    return result

#写入json文件
def get_json_file(json_path, data, file_name):
  if not os.path.exists(json_path):
    os.makedirs(json_path)
  with open(json_path + '/' + file_name + '.json', 'w') as f:
     json.dump(data, f) 

#程序入口
def init(result_path, name):
  result = get_non_txt_files(result_path) #得到所有不是txt的文件
  # print(result)
  for item in result: # 对于每个文件执行下面的file to json操作
    test_result = parse_file(result_path + '/' + item)
    # print(test_result)
    # break
    # get_json_file(result_path.replace('mutant_result_faulty_file', 'mutant_result_faulty_file_json'), test_result, item)
    # get_json_file(result_path.replace('mutant_result_faulty_file_major', 'mutant_result_faulty_file_major_json'), test_result, item)
    get_json_file(result_path.replace(name, f'{name}_json'), test_result, item)
    # get_json_file(result_path, test_result, item)
    # get_json_file(result_path.replace('mutant_result', 'mutant_result_json'), test_result, item)
    # get_json_file(result_path, test_result, item)
  print("{} 已完成".format(result_path))


def start(pid, svid, evid, name):
   for i in range(svid, evid + 1):
      # path = '/home/mutant_result_faulty_file/' + pid  + '/' + str(i) + 'b'
      # path = '/home/mutant_result_faulty_file_SFClu/' + pid  + '/' + str(i) + 'b'
      path = f'/home/{name}/{pid}/{i}b'
      # path = '/home/failingTestOutput/' + pid  + '/' + str(i) + 'b'
      # path = '/home/mutant_result/' + pid  + '/' + str(i) + 'b'
      if not os.path.exists(path):
         print(f'{pid}-{i} 不存在')
         continue
      # init('/home/mutant_result/Time/' + str(i) + 'b')
      init(path, name)

def chushihua(name):
    # start('Chart', 1, 26, name)
    # start('Time', 1, 27, name)
    # start('Lang', 1, 65, name)
    # start('Math', 1, 106, name)
    # start('Mockito', 1, 38, name)
    # start('Closure', 1, 133, name)
    start('Gson', 1, 18, name)
    start('JacksonXml', 1, 6, name)

if __name__ == '__main__':
    # chushihua('mutant_result_faulty_file_SFClu_shanjian')
  #  chushihua('mutant_result_faulty_file_SFClu')
  #  chushihua('mutant_result_faulty_file')
  #  chushihua('mutant_result_faulty_file_Major_Mbert_SFClu')
   chushihua('failingTestOutput')
  #  chushihua('mutant_result_faulty_file_Major_Mbert_SFClu_shanjian')
    # chushihua('mutant_result_faulty_file_Major_SFClu_FaultyLine')
    # start('Chart', 1, 26, 'mutant_result_faulty_file_SFClu_shanjian')
    # start('Time', 1, 27, 'mutant_result_faulty_file_SFClu_shanjian)
    # start('Lang', 1, 65, 'mutant_result_faulty_file_SFClu_shanjian)
    # start('Math', 1, 106, 'mutant_result_faulty_file_SFClu_shanjian)
    # pid = 'Csv'
    # svid = 1
    # evid = 16
    # pid = 'Time'
    # svid = 1
    # evid = 27
    # pid = 'Chart'
    # svid = 1
    # evid = 26
    # pid = 'Lang'
    # svid = 1
    # evid = 65
    # pid = 'Math'
    # svid = 1
    # evid = 106

    # pid = 'Time'
    # svid = 1
    # evid = 27
    # for i in range(svid, evid + 1):
    #   # path = '/home/mutant_result_faulty_file/' + pid  + '/' + str(i) + 'b'
    #   path = '/home/failingTestOutput/' + pid  + '/' + str(i) + 'b'
    #   # path = '/home/mutant_result/' + pid  + '/' + str(i) + 'b'
    #   if not os.path.exists(path):
    #      continue
    #   # init('/home/mutant_result/Time/' + str(i) + 'b')
    #   init(path)