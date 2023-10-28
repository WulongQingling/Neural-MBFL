import json
import os
import pandas as pd

#逐行读取json
def read_json_file_line_by_line(file_path):
    result = []
    with open(file_path, 'r') as f:
        line = f.readline()
        # print(type(line), type(eval(line)))
        while line:
            # line = "'" + line + "'"
            # result.append(json.loads(line.strip()))
            # print(line.strip())
            result.append(line.strip())
            line = f.readline()
    return result

def read_json_file(file_path):
    """
    读取JSON文件并返回解析后的JSON数据
    :param file_path: JSON文件路径
    :return: 解析后的JSON数据.
    """
    with open(file_path) as file:
        data = json.load(file)
    return data

def init(pid,results):
  formula = ["Dstar", "Ochiai", "Jaccard", "Op2", "Tarantula", "Gp13"]
  # formula = ["Dstar_function", "Ochiai_function", "Jaccard_function", "Op2_function", "Tarantula_function", "Gp13_function"]
    # print(pid, "Ave")
    # ave = "MaxSubAvgAveTopnmBert"
    # best = "MaxSubAvgBestTopnmBert"
    # ave = "MaxSubAvgAveTopnType1mBert"
    # best = "MaxSubAvgBestTopnType1mBert"
  avetopn = {
      # "0": "MaxSubAvgMbertType4TopnAve",
      # "1": "MaxSubAvgMajorType4TopnAve",
      # "2": "MaxSubAvgMbertType1TopnAve",
      # "3": "MaxSubAvgMajorType1TopnAve",
      # "4": "MaxSubAvgMbertType3TopnAve",
      # "5": "MaxSubAvgMajorType3TopnAve",
      # "6": "MaxMbertType1TopnAve",
      # "7": "MaxMajorType1TopnAve",
      "8": "MaxMbertType3TopnAve",
      "9": "MaxMajorType3TopnAve",
      # "10": "MaxMbertType4TopnAve",
      # "11": "MaxMajorType4TopnAve",
      "12" : "MaxMajorMergeType3TopnAve",
      "13":  "MaxMbertMergeType3TopnAve",
      "14":  "MaxMergeType3TopnAve",

      # "0": "MaxSubAvgMbertType4TopnAve_func",
      # "1": "MaxSubAvgMajorType4TopnAve_func",
      # "2": "MaxSubAvgMbertType1TopnAve_func",
      # "3": "MaxSubAvgMajorType1TopnAve_func",
      # "4": "MaxSubAvgMbertType3TopnAve_func",
      # "5": "MaxSubAvgMajorType3TopnAve_func",
      # "6": "MaxMbertType1TopnAve_func",
      # "7": "MaxMajorType1TopnAve_func",
      # "8": "MaxMbertType3TopnAve_func",
      # "9": "MaxMajorType3TopnAve_func",
      # "10": "MaxMbertType4TopnAve_func",
      # "11": "MaxMajorType4TopnAve_func"
    }
  
  besttopn = {
      # "0" : "MaxSubAvgMbertType4TopnBest_func",
      # "1" : "MaxSubAvgMajorType4TopnBest_func",
      # "2" : "MaxSubAvgMbertType1TopnBest_func",
      # "3" : "MaxSubAvgMajorType1TopnBest_func",
      # "4" : "MaxSubAvgMbertType3TopnBest_func",
      # "5" : "MaxSubAvgMajorType3TopnBest_func",
      # "6" : "MaxMbertType1TopnBest_func",
      # "7" : "MaxMajorType1TopnBest_func",
      # "8" : "MaxMbertType3TopnBest_func",
      # "9" : "MaxMajorType3TopnBest_func",
      # "10" : "MaxMbertType4TopnBest_func",
      # "11" : "MaxMajorType4TopnBest_func"
      "0" : "MaxSubAvgMbertType4TopnBest",
      "1" : "MaxSubAvgMajorType4TopnBest",
      "2" : "MaxSubAvgMbertType1TopnBest",
      "3" : "MaxSubAvgMajorType1TopnBest",
      "4" : "MaxSubAvgMbertType3TopnBest",
      "5" : "MaxSubAvgMajorType3TopnBest",
      "6" : "MaxMbertType1TopnBest",
      "7" : "MaxMajorType1TopnBest",
      "8" : "MaxMbertType3TopnBest",
      "9" : "MaxMajorType3TopnBest",
      "10" : "MaxMbertType4TopnBest",
      "11" : "MaxMajorType4TopnBest",
      "12" : "MaxMajorMergeType3TopnBest",
      "13":  "MaxMbertMergeType3TopnBest",
      "14":  "MaxMergeType3TopnBest",
    }
  
  for item in formula:
    #   json_path = "/home/changzexing/top-n-new/" + pid + "/" + item + ".json"
    #   json_path = "/home/changzexing/top-n-merge/" + pid + "/" + item + ".json"
    #   json_path = "/home/changzexing/top-n-major/" + pid + "/" + item + ".json"
    #   json_path = "/home/changzexing/AveTopnmBert/" + pid + "/" + item + ".json"
    print(item, f'{pid}-Ave')
    for _item in avetopn:
      json_path = f"/home/changzexing/{avetopn[_item]}/" + pid + "/" + item + ".json"
      if not os.path.exists(json_path):
          continue
      content = read_json_file(json_path)
      print(avetopn[_item], content)
      # content_dict = json.loads(content)  # 将字符串转换为字典
      # 一行
      results = results.append({'Item': item, 'Type': avetopn[_item],
                                'Top-1': content['Top-1'],
                                'Top-3': content['Top-3'],
                                'Top-5': content['Top-5'],
                                'Top-10':content['Top-10']}, ignore_index=True)
  return results
    # print(item, f'{pid}-Best')
    # for _item in besttopn:
    #   json_path = "/home/changzexing/top-n-new/" + pid + "/" + item + ".json"
    #   json_path = "/home/changzexing/top-n-merge/" + pid + "/" + item + ".json"
    #   json_path = "/home/changzexing/top-n-major/" + pid + "/" + item + ".json"
    #   json_path = f"/home/changzexing/{besttopn[_item]}/" + pid + "/" + item + ".json"
    # #   json_path = "/home/changzexing/BestTopnmBert/" + pid + "/" + item + ".json"
    #   if not os.path.exists(json_path):
    #       continue
    #   content = read_json_file(json_path)
    #   print(besttopn[_item], content)
    #   # content_dict = json.loads(content)  # 将字符串转换为字典
    #   results = results.append({'Item': item, 'Type': besttopn[_item],
    #                             'Top-1': content['Top-1'],
    #                             'Top-3': content['Top-3'],
    #                             'Top-5': content['Top-5'],
    #                             'Top-10': content['Top-10']}, ignore_index=True)
  

if __name__ == '__main__':
    results_chart = pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10'])
    results_chart = init("Chart",results_chart)

    results_lang = pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10'])
    results_lang = init("Lang",results_lang)
    # init("Cli")
    # init("Csv")

    results_time = pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10'])
    results_time = init("Time",results_time)

    results_math = pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10'])
    results_math = init("Math",results_math)

    # 创建一个与results_chart相同的DataFrame
    results = pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10'], index=results_chart.index)
    for i in range(len(results_chart)):
        # 判断results_chart的Item和Type是否与其他三个DataFrame相同
        Item_list = [results_chart.loc[i, 'Item'], results_lang.loc[i, 'Item'], results_time.loc[i, 'Item'], results_math.loc[i, 'Item']]
        Type_list = [results_chart.loc[i, 'Type'], results_lang.loc[i, 'Type'], results_time.loc[i, 'Type'], results_math.loc[i, 'Type']]
        if len(list(set(Item_list))) != 1 or len(list(set(Type_list))) != 1:
            print('Error: Item or Type is not equal!')
            exit(1)
        results.loc[i, ['Item', 'Type']] = results_chart.loc[i, ['Item', 'Type']]
        results.loc[i, ['Top-1', 'Top-3', 'Top-5', 'Top-10']] = results_chart.loc[i, ['Top-1', 'Top-3', 'Top-5', 'Top-10']] + results_lang.loc[i, ['Top-1', 'Top-3', 'Top-5', 'Top-10']] + results_time.loc[i, ['Top-1', 'Top-3', 'Top-5', 'Top-10']] + results_math.loc[i, ['Top-1', 'Top-3', 'Top-5', 'Top-10']]
    results.to_excel(f'/home/changzexing/hbl/topn/result_Merge_all.xlsx', index=False)