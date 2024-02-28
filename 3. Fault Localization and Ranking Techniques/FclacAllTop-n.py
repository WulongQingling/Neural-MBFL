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
      # "8": "MaxMbertType3TopnAve",
      # "9": "MaxMajorType3TopnAve",
      # "10": "MaxMbertType4TopnAve",
      # "11": "MaxMajorType4TopnAve",
      # "12" : "MaxMajorMergeType3TopnAve",
      # "13":  "MaxMbertMergeType3TopnAve",
      # "14":  "MaxMergeType3TopnAve",
      # "15" : "MaxMbertHebingSingleType1TopnAve",
      # "16": "MaxMajorMberthebingTopnAve",
      # "17": "MaxSFCluSingleTopnAve",
      # "18": 'MaxSFCluShanjianFOMTopnAve',
      # "19":  "MaxMajorLast2FirstFOMTopnAve",
      # "20": "MaxMajorRandomMixFOMTopnAve",
      # "21": "MaxMajorSFCluFOMTopnAveNew",
      #  "22": "MaxMajorMbertLast2FirstFOMTopnAve",
      #  "23": "MaxMajorMbertRandomMixFOMTopnAve",
      #  "24": "MaxMajorMbertSFCluFOMTopnAveNew",
      #  "25": "MaxMajorMbertSFCluFOMType3TopnAveNew",
      #  "26": "Delta4MsMajorMbertSFCluType3TopnAve",
      "27" : "MuseMaxMbertType3TopnAve",
      "28" : "MuseMaxMajorType3TopnAve",

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
    #   json_path = "/home/top-n-new/" + pid + "/" + item + ".json"
    #   json_path = "/home/top-n-merge/" + pid + "/" + item + ".json"
    #   json_path = "/home/top-n-major/" + pid + "/" + item + ".json"
    #   json_path = "/home/AveTopnmBert/" + pid + "/" + item + ".json"
    # print(item, f'{pid}-Ave')
    for _item in avetopn:
      json_path = f"/home/{avetopn[_item]}/" + pid + "/" + item + ".json"
      if not os.path.exists(json_path):
          continue
      content = read_json_file(json_path)
      # print(avetopn[_item], content)
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
    #   json_path = "/home/top-n-new/" + pid + "/" + item + ".json"
    #   json_path = "/home/top-n-merge/" + pid + "/" + item + ".json"
    #   json_path = "/home/top-n-major/" + pid + "/" + item + ".json"
    #   json_path = f"/home/{besttopn[_item]}/" + pid + "/" + item + ".json"
    # #   json_path = "/home/BestTopnmBert/" + pid + "/" + item + ".json"
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
    
    # 假设init函数按照打印输出所示填充DataFrame
    # 下面是修订方法可能的轮廓：保存为一个excel文件，每个project为一个sheet，累加和再作一个新的sheet

    # 初始化一个空列表以保存DataFrames
    project_dataframes = []

    # 项目名称列表，用于迭代和工作表名称
    project_names = ["Chart", "Time", "Lang", "Math", "Mockito", "Closure"]

    # 模拟每个项目的init函数（您将用实际调用init替换此处）
    for project in project_names:
        df = pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10'])  # 用实际的init调用替换：df = init(project, pd.DataFrame(columns=['Item', 'Type', 'Top-1', 'Top-3', 'Top-5', 'Top-10']))
        df = init(project, df)
        print(project,df)
        project_dataframes.append(df)

    # 合并所有项目的DataFrame
    merged_df = pd.concat(project_dataframes)

    # 确保算术操作的数据类型正确
    for col in ['Top-1', 'Top-3', 'Top-5', 'Top-10']:
        merged_df[col] = pd.to_numeric(merged_df[col])

    # 按'Item'和'Type'分组并求和，重置索引使'Item'和'Type'再次成为列
    summary_result = merged_df.groupby(['Item', 'Type']).sum().reset_index()

    # 将每个项目的DataFrame及汇总DataFrame保存到包含多个工作表的单个Excel文件中
    with pd.ExcelWriter('//home/d4jscript/hblscript/TopN/result_Muse.xlsx') as writer:  # 使用正确的路径
        for project_name, df in zip(project_names, project_dataframes):
            df.to_excel(writer, sheet_name=project_name, index=False)
        summary_result.to_excel(writer, sheet_name='Summary', index=False)