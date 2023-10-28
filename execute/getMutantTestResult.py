
from collections import OrderedDict
import pandas as pd
import csv
import subprocess

#逐行读取原始txt
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

#逐行读取变异体执行结果txt
def get_lines_starting_with(filename, start_with):
  with open(filename, "r", encoding='utf-8') as f:
      lines = f.readlines()
  results = [line for line in lines if "Has it failed?" in line]
  return results

# results = get_lines_starting_with("file.txt", "org.jfree")
# print(results)


#找到测试用用例txt及其结果txt
def find_test_txt_files(file_path, txt_name):
  result = subprocess.run(["find", file_path, "-name", txt_name + ".txt"], stdout=subprocess.PIPE)
  txt_files = result.stdout.decode("utf-8").strip().split("\n")
  return txt_files
 
#得到原版本测试用例执行结果
def get_init_test_result(cover_path):
  tests_txt = find_test_txt_files(cover_path, "all_tests")
  tests_result_txt = find_test_txt_files(cover_path, "inVector")
  # print(tests_txt, tests_result_txt)
  test_result = {}
  test_result['name'] = 'init'
  for item in range(len(tests_txt)):
    test_list = read_txt_file(tests_txt[item])
    result_list = read_txt_file(tests_result_txt[item])
    # print(len(test_list), len(result_list), test_list[2], 1 if test_list[2] == 'org.jfree.chart.annotations.junit.CategoryLineAnnotationTests#testCloning' else 0)
    for test_item in range(len(test_list)):
      # print(test_list[test_item], result_list[test_item])
      test_result[str(test_list[test_item])] = result_list[test_item]
      # if test_item <= 10:
      #   print(test_list[test_item], result_list[test_item])
  return test_result

#得到变异体的测试用例执行结果txt
def get_mutant_test_result_txt(mutant_path):
  tests_result_txt = find_test_txt_files(mutant_path, "*")
  print(len(tests_result_txt), tests_result_txt)
  result = []
  for item in tests_result_txt:
    mutant_result = get_lines_starting_with(item, "org")
    result.append([mutant_result, item])
  return result
  # print(mutant_result)

#根据txt的每行数据获取测试用例及结果
def split_string(string):
    parts = string.strip().split(' ')
    # print(string)
    first = parts[0]
    last = parts[-1]
    return first, 1 if last == "true" else 0

#整理每个txt的测试用例及结果
def get_mutant_test_result(mutant_result_list, mutant_result_path):
  test_result = {}
  test_result['name'] = mutant_result_path
  num = 0
  for item in mutant_result_list:
    result = split_string(item)
    test_result[result[0]] = result[1]
    if result[1] == 1:
      num += 1
  return test_result, num

#计算杀死矩阵   
def kill_matrix(mutant_result_path, init_path, filename):
  kill_matrix_data = []
  initInfo = get_init_test_result(init_path)
  # print(len(initInfo))
  # print(initInfo['org.jfree.chart.annotations.junit.CategoryLineAnnotationTests#testCloning'])
  kill_matrix_data.append(initInfo)
  # # print(initInfo)
  mutant_result = get_mutant_test_result_txt(mutant_result_path)
  # print(len(mutant_result[0][0]))
  # print(mutant_result[0][0])
  with open(filename + 'output.txt', 'w') as f:
    for item in mutant_result:
      test_result = get_mutant_test_result(item[0], item[1])
      # print(len(test_result[0]), initInfo['org.jfree.chart.needle.junit.LongNeedleTests#testSerialization'], test_result[0]['org.jfree.chart.needle.junit.LongNeedleTests#testSerialization'])
      # a = set(initInfo)
      # b = set(test_result[0])
      # print(len(a.symmetric_difference(b)))
      # print(test_result[1])
      print("{}已生成，长度为{}，1的个数为{}".format(item[1], len(test_result[0]), test_result[1]), file = f)
      kill_matrix_data.append(test_result[0])
    #生成csv
    df = pd.DataFrame(kill_matrix_data)
    df.to_csv(filename +  'result.csv', index=False)
  f.close()
    

if __name__ == '__main__':
  kill_matrix("/home/changzexing/mutant_result/Time/1b", '/home/changzexing/d4jbasecover/Time/1b', 'Time-1b')