import csv
import json
import os
from re import T
import pandas as pd


class DataHandler:
    def __init__(self, sheet_names):
        # Initialize a DataFrame for each sheet
        self.dfs = {name: pd.DataFrame(columns=['Project', 'Version', 'faulty_entity', 'Rank_ave','Rank_best','Filename']) for name in sheet_names}

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
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return {}
#csv转字典
def csv_to_dict(file_path):
    json_content = read_json_file(file_path)
    ranknum = {}
    trueranknum = {}
    faulty = []
    sum = 0
    for item in json_content:
      tmp_rank = json_content[item]["rank"]
      tmp_rank = str(tmp_rank)
      if json_content[item]["faulty"] == False:
        if tmp_rank in trueranknum:
            trueranknum[tmp_rank].append(item)
        else:
            trueranknum[tmp_rank] = [item]
      if tmp_rank in ranknum:
          ranknum[tmp_rank].append(item)
      else:
          ranknum[tmp_rank] = [item]
      if json_content[item]["faulty"] == True:
          faulty.append(item)
    # print(ranknum)
    return json_content, ranknum, faulty, trueranknum, sum

def init(handler, pro, svid, evid):
  formula = ["Dstar", "Ochiai", "Jaccard", "Op2", "Tarantula", "Gp13"]
  # formula = ["Dstar_function", "Ochiai_function", "Jaccard_function", "Op2_function", "Tarantula_function", "Gp13_function"]

  # filename = ["mbertrank", "majorrank", "mergerank"]
  # filename = ["MaxSubAvgMbertrank"]
  # filename = ["susMaxSubAvgMbertType1Rank", "susMaxSubAvgMbertType3Rank"]
  # SusMajorMergeMaxType3Rank/ SusMbertMergeMaxType3Rank/ SusMergeMaxType3/
  # filename = ["SusMbertMergeMaxType3Rank","SusMajorMergeMaxType3Rank","SusMergeMaxType3Rank"
  #             "susMaxMbertType1Rank", "susMaxMbertType3Rank", "susMaxMbertType4Rank", "susMaxSubAvgMbertType4Rank", "susMaxSubAvgMbertType1Rank", "susMaxSubAvgMbertType3Rank", "susMaxSubAvgMajorType1Rank", "susMaxSubAvgMajorType3Rank", "susMaxSubAvgMajorType4Rank", "susMaxMajorType1Rank", "susMaxMajorType3Rank", "susMaxMajorType4Rank"]
  # filename = ["susMaxMbertType1Rank_func", "susMaxMbertType3Rank_func", "susMaxMbertType4Rank_func", "susMaxSubAvgMbertType4Rank_func", "susMaxSubAvgMbertType1Rank_func", "susMaxSubAvgMbertType3Rank_func", "susMaxSubAvgMajorType1Rank_func", "susMaxSubAvgMajorType3Rank_func", "susMaxSubAvgMajorType4Rank_func", "susMaxMajorType1Rank_func", "susMaxMajorType3Rank_func", "susMaxMajorType4Rank_func"]
  # filename = ["SusMbertMergeMaxType3Rank","SusMajorMergeMaxType3Rank","SusMergeMaxType3Rank","susMaxMbertType3Rank","susMaxMajorType3Rank"]
  filename = ["susMaxMbertType3Rank","susMaxMajorType3Rank"]
  ans_ave = {}
  ans_best = {}
  for _item_ in filename:
    for formula_item in formula:
      for item in range(svid, evid + 1):
        print(item)
        # list_ignore = [] 
        # if pro == 'Math':
        #    list_ignore = [5, 6, 13, 14, 15, 16, 17, 19, 36, 44, 54, 59, 71, 73, 74, 99]
        # elif pro == 'Chart':
        #    list_ignore = [8,10]
        # elif pro == 'Lang':
        #    list_ignore = [56,30,22,39,20,40,29,59,18,45,43,8,14,38,26,31]
        # if item in list_ignore:
        #     print(f"跳过{item}版本")
        #     continue
        mbert_sus_path = f"/home/{_item_}/{pro}/{item}b/{formula_item}.json"
        if not os.path.exists(mbert_sus_path):
          print(f"跳过{item}版本")
          continue
        sus, ranknum, faulty, trueranknum, sum = csv_to_dict(mbert_sus_path)
        fautly_result_best = {}
        fautly_result_ave = {}
        # print(faulty) #['src-main-java-org-apache-commons-math3-geometry-euclidean-threed-Line-2139']
        # faulty文件全为空？
        for _item in faulty:
          i = 0
          sus[_item]["rank"]  = str(sus[_item]["rank"])
          if int(sus[_item]["rank"]) > 1:
            for rank in range(1, int(sus[_item]["rank"])):
              i += len(trueranknum[str(rank)]) if str(rank) in trueranknum else 0
          # print(sus[_item]["rank"], type(sus[_item]["rank"]))
          j = len(ranknum[sus[_item]["rank"]]) if sus[_item]["rank"] in ranknum else 0
          data_dict= {
             'Project':pro, 
             'Version':item, 
             'faulty_entity':_item, 
             'Rank_ave': ((i + 1) + (i + j)) / 2,
             'Rank_best': i + 1,
             'Filename': _item_
          }
          # if _item_ == 'susMaxMajorType3Rank' and pro == 'Chart' and item == 18 and _item == 'source-org-jfree-data-DefaultKeyedValues2D-130':
          #    print(f"i:{i},j:{j},((i + 1) + (i + j)) / 2:{((i + 1) + (i + j)) / 2},")
          #    breakpoint()
          handler.add_data(formula_item, data_dict)
          print(_item_)
          # # 平均排名
          # fautly_result_ave[_item] = ((i + 1) + (i + j)) / 2
          # # best
          # fautly_result_best[_item] = i + 1
        # ans_ave[f"{item}b"] = fautly_result_ave
        # ans_best[f"{item}b"] = fautly_result_best
      #   break
      # break
      # mbert_averank_json_path = f"/home/{ave[_item_]}/{pro}"
      # if not os.path.exists(mbert_averank_json_path):
      #   os.makedirs(mbert_averank_json_path)
      # with open(f"{mbert_averank_json_path}/{formula_item}.json", 'w') as f:
      #   json.dump(ans_ave, f)
      # mbert_bestrank_json_path = f"/home/{best[_item_]}/{pro}"
      # if not os.path.exists(mbert_bestrank_json_path):
      #   os.makedirs(mbert_bestrank_json_path)
      # with open(f"{mbert_bestrank_json_path}/{formula_item}.json", 'w') as f:
      #   json.dump(ans_best, f)


if __name__ == '__main__':
  # sheet_names = ["Dstar", "Ochiai", "Jaccard", "Op2", "Tarantula", "Gp13"]  # Specify your sheet names
  # # 'Math': (1, 106),
  # # 'Time': (1, 27),
  # # 'Chart': (1, 26),
  # # 'Lang': (1, 65),
  # # 'Mockito': (1, 38),
  # # 'Closure': (1, 133)
  # handler = DataHandler(sheet_names)
  # init(handler,'Chart', 1, 26)
  # init(handler,'Time', 1, 27)
  # init(handler,'Lang', 1, 65)
  # init(handler,'Math', 1, 106)
  # init(handler,'Mockito',1,38)
  # init(handler,'Closure',1,133)
  # handler.save_data("output_rank_v2.xlsx")


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
      init(project_handler,pid,svid,evid)
      project_handler.save_data(f"{output_directory}{pid}Type3Rank.xlsx")  # 以项目名命名的Excel文件
      overall_handler.merge_data(project_handler)  # 将项目数据合并到总体数据处理器
  # 保存总体汇总的数据
  overall_handler.save_data(f"{output_directory}Type3Rankoverall_summary.xlsx")
