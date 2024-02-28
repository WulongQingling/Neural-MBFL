import json
import os

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return {}

def init(pro):
  # filename = ["major", "mBert", "merge"]
  # filename = ["mBert"]
  formula = ["Dstar", "Ochiai", "Jaccard", "Op2", "Tarantula", "Gp13"]
  # formula = ["Dstar_function", "Ochiai_function", "Jaccard_function", "Op2_function", "Tarantula_function", "Gp13_function"]
  # averank = "MaxSubAvgAveRang"
  # avetopn = "MaxSubAvgAveTopn"
  # bestrank = "MaxSubAvgBestRang"
  # besttopn = "MaxSubAvgBestTopn"
  
  #语句级的怀疑度：
  averank = {
    # "0": "MaxSubAvgMbertType4RankAve",
    # "1": "MaxSubAvgMbertType1RankAve",
    # "2": "MaxSubAvgMbertType3RankAve",
    # "3" : "MaxMbertType1RankAve",
    # "4" : "MaxMbertType3RankAve",
    # "5" : "MaxMbertType4RankAve",
    # "6" : "MaxSubAvgMajorType1RankAve",
    # "7" : "MaxSubAvgMajorType3RankAve",
    # "8" : "MaxSubAvgMajorType4RankAve",
    # "9" : "MaxMajorType1RankAve",
    # "10" : "MaxMajorType3RankAve",
    # "11" : "MaxMajorType4RankAve",
    # "12" : "MaxMajorMergeType3RankAve",
    # "13":  "MaxMbertMergeType3RankAve",
    # "14":  "MaxMergeType3RankAve",
    # "15": "MaxMbertHebingSingleType1RankAve",
    # "16": "MaxMajorMberthebingRankAve",
    # "17": "MaxSFCluSingleRankAve",
    # "18": 'MaxSFCluShanjianFOMRankAve',
    # "19":  "MaxMajorLast2FirstFOMRankAve",
    # "20": "MaxMajorRandomMixFOMRankAve",
    # "21": "MaxMajorSFCluFOMRankAveNew",
    # "22": "MaxMajorMbertLast2FirstFOMRankAve",
    # "23": "MaxMajorMbertRandomMixFOMRankAve",
    # "24": "MaxMajorMbertSFCluFOMRankAveNew",
    #  "25": "MaxMajorMbertSFCluFOMType3RankAveNew",
    #  "26": "Delta4MsMajorMbertSFCluType3RankAve",
    "27" : "MuseMaxMbertType3RankAve",
    "28" : "MuseMaxMajorType3RankAve",

  }
  avetopn = {
    "0": "MaxSubAvgMbertType4TopnAve",
    "1": "MaxSubAvgMbertType1TopnAve",
    "2": "MaxSubAvgMbertType3TopnAve",
    "3" : "MaxMbertType1TopnAve",
    "4" : "MaxMbertType3TopnAve",
    "5" : "MaxMbertType4TopnAve",
    "6" : "MaxSubAvgMajorType1TopnAve",
    "7" : "MaxSubAvgMajorType3TopnAve",
    "8" : "MaxSubAvgMajorType4TopnAve",
    "9" : "MaxMajorType1TopnAve",
    "10" : "MaxMajorType3TopnAve",
    "11" : "MaxMajorType4TopnAve",
    "12" : "MaxMajorMergeType3TopnAve",
    "13":  "MaxMbertMergeType3TopnAve",
    "14":  "MaxMergeType3TopnAve",
    "15": "MaxMbertHebingSingleType1TopnAve",
    "16": "MaxMajorMberthebingTopnAve",
    "17": "MaxSFCluSingleTopnAve",
    "18": 'MaxSFCluShanjianFOMTopnAve',
    "19":  "MaxMajorLast2FirstFOMTopnAve",
    "20": "MaxMajorRandomMixFOMTopnAve",
    "21": "MaxMajorSFCluFOMTopnAveNew",
    "22": "MaxMajorMbertLast2FirstFOMTopnAve",
    "23": "MaxMajorMbertRandomMixFOMTopnAve",
    "24": "MaxMajorMbertSFCluFOMTopnAveNew",
    "25": "MaxMajorMbertSFCluFOMType3TopnAveNew",
    "26": "Delta4MsMajorMbertSFCluType3TopnAve",
    "27" : "MuseMaxMbertType3TopnAve",
    "28" : "MuseMaxMajorType3TopnAve",

  }
  bestrank = {
    # "0": "MaxSubAvgMbertType4RankBest",
    # "1": "MaxSubAvgMbertType1RankBest",
    # "2": "MaxSubAvgMbertType3RankBest",
    # "3" : "MaxMbertType1RankBest",
    # "4" : "MaxMbertType3RankBest",
    # "5" : "MaxMbertType4RankBest",
    # "6" : "MaxSubAvgMajorType1RankBest",
    # "7" : "MaxSubAvgMajorType3RankBest",
    # "8" : "MaxSubAvgMajorType4RankBest",
    # "9" : "MaxMajorType1RankBest",
    # "10" : "MaxMajorType3RankBest",
    # "11" : "MaxMajorType4RankBest",
    # "12" : "MaxMajorMergeType3RankBest",
    # "13":  "MaxMbertMergeType3RankBest",
    # "14":  "MaxMergeType3RankBest",
    # "15": "MaxMbertHebingSingleType1RankBest",
    # "16": "MaxMajorMberthebingRankBest",
    # "17": "MaxSFCluSingleRankBest",
    # "18": 'MaxSFCluShanjianFOMRankBest',
    "19":  "MaxMajorLast2FirstFOMRankAve",
    "20": "MaxMajorRandomMixFOMRankAve"
  }
  besttopn = {
    "0": "MaxSubAvgMbertType4TopnBest",
    "1": "MaxSubAvgMbertType1TopnBest",
    "2": "MaxSubAvgMbertType3TopnBest",
    "3" : "MaxMbertType1TopnBest",
    "4" : "MaxMbertType3TopnBest",
    "5" : "MaxMbertType4TopnBest",
    "6" : "MaxSubAvgMajorType1TopnBest",
    "7" : "MaxSubAvgMajorType3TopnBest",
    "8" : "MaxSubAvgMajorType4TopnBest",
    "9" : "MaxMajorType1TopnBest",
    "10" : "MaxMajorType3TopnBest",
    "11" : "MaxMajorType4TopnBest",
    "12" : "MaxMajorMergeType3TopnBest",
    "13":  "MaxMbertMergeType3TopnBest",
    "14":  "MaxMergeType3TopnBest",
    "15": "MaxMbertHebingSingleType1TopnBest",
    "16": "MaxMajorMberthebingTopnBest",
    "17": "MaxSFCluSingleTopnBest",
    "18": 'MaxSFCluShanjianFOMTopnBest'
  }

  #方法级的怀疑度
  # averank = {
  #   "0": "MaxSubAvgMbertType4RankAve_func",
  #   "1": "MaxSubAvgMbertType1RankAve_func",
  #   "2": "MaxSubAvgMbertType3RankAve_func",
  #   "3" : "MaxMbertType1RankAve_func",
  #   "4" : "MaxMbertType3RankAve_func",
  #   "5" : "MaxMbertType4RankAve_func",
  #   "6" : "MaxSubAvgMajorType1RankAve_func",
  #   "7" : "MaxSubAvgMajorType3RankAve_func",
  #   "8" : "MaxSubAvgMajorType4RankAve_func",
  #   "9" : "MaxMajorType1RankAve_func",
  #   "10" : "MaxMajorType3RankAve_func",
  #   "11" : "MaxMajorType4RankAve_func"
  # }
  # avetopn = {
  #   "0": "MaxSubAvgMbertType4TopnAve_func",
  #   "1": "MaxSubAvgMbertType1TopnAve_func",
  #   "2": "MaxSubAvgMbertType3TopnAve_func",
  #   "3" : "MaxMbertType1TopnAve_func",
  #   "4" : "MaxMbertType3TopnAve_func",
  #   "5" : "MaxMbertType4TopnAve_func",
  #   "6" : "MaxSubAvgMajorType1TopnAve_func",
  #   "7" : "MaxSubAvgMajorType3TopnAve_func",
  #   "8" : "MaxSubAvgMajorType4TopnAve_func",
  #   "9" : "MaxMajorType1TopnAve_func",
  #   "10" : "MaxMajorType3TopnAve_func",
  #   "11" : "MaxMajorType4TopnAve_func"
  # }
  # bestrank = {
  #   "0": "MaxSubAvgMbertType4RankBest_func",
  #   "1": "MaxSubAvgMbertType1RankBest_func",
  #   "2": "MaxSubAvgMbertType3RankBest_func",
  #   "3" : "MaxMbertType1RankBest_func",
  #   "4" : "MaxMbertType3RankBest_func",
  #   "5" : "MaxMbertType4RankBest_func",
  #   "6" : "MaxSubAvgMajorType1RankBest_func",
  #   "7" : "MaxSubAvgMajorType3RankBest_func",
  #   "8" : "MaxSubAvgMajorType4RankBest_func",
  #   "9" : "MaxMajorType1RankBest_func",
  #   "10" : "MaxMajorType3RankBest_func",
  #   "11" : "MaxMajorType4RankBest_func"
  # }
  # besttopn = {
  #   "0": "MaxSubAvgMbertType4TopnBest_func",
  #   "1": "MaxSubAvgMbertType1TopnBest_func",
  #   "2": "MaxSubAvgMbertType3TopnBest_func",
  #   "3" : "MaxMbertType1TopnBest_func",
  #   "4" : "MaxMbertType3TopnBest_func",
  #   "5" : "MaxMbertType4TopnBest_func",
  #   "6" : "MaxSubAvgMajorType1TopnBest_func",
  #   "7" : "MaxSubAvgMajorType3TopnBest_func",
  #   "8" : "MaxSubAvgMajorType4TopnBest_func",
  #   "9" : "MaxMajorType1TopnBest_func",
  #   "10" : "MaxMajorType3TopnBest_func",
  #   "11" : "MaxMajorType4TopnBest_func"
  # }
  # 计算averank
  for item in averank:
    for formula_item in formula:
      ans = {
        "Top-1": 0,
        "Top-3": 0,
        "Top-5": 0,
        "Top-10": 0,
      }
      ave_json_path = f"/home/{averank[item]}/{pro}/{formula_item}.json"
      result = read_json_file(ave_json_path)
      for vid in result:
        vid = result[vid]
        for faultyline in vid:
          if vid[faultyline] <= 1:
            ans["Top-1"] += 1
          if vid[faultyline] <= 3:
            ans["Top-3"] += 1
          if vid[faultyline] <= 5:
            ans["Top-5"] += 1
          if vid[faultyline] <= 10:
            ans["Top-10"] += 1
      topn_json_path = f"/home/{avetopn[item]}/{pro}"
      if not os.path.exists(topn_json_path):
        os.makedirs(topn_json_path)
      with open(f"{topn_json_path}/{formula_item}.json", 'w') as f:
        json.dump(ans, f)
  # 计算bestrank
  # for item in bestrank:
  #   for formula_item in formula:
  #     ans = {
  #       "Top-1": 0,
  #       "Top-3": 0,
  #       "Top-5": 0,
  #       "Top-10": 0,
  #     }
  #     ave_json_path = f"/home/{bestrank[item]}/{pro}/{formula_item}.json"
  #     result = read_json_file(ave_json_path)
  #     for vid in result:
  #       vid = result[vid]
  #       for faultyline in vid:
  #         if vid[faultyline] <= 1:
  #           ans["Top-1"] += 1
  #         if vid[faultyline] <= 3:
  #           ans["Top-3"] += 1
  #         if vid[faultyline] <= 5:
  #           ans["Top-5"] += 1
  #         if vid[faultyline] <= 10:
  #           ans["Top-10"] += 1
  #     topn_json_path = f"/home/{besttopn[item]}/{pro}"
  #     if not os.path.exists(topn_json_path):
  #       os.makedirs(topn_json_path)
  #     with open(f"{topn_json_path}/{formula_item}.json", 'w') as f:
  #       json.dump(ans, f)
            

if __name__ == "__main__":
  init("Chart")
  init("Time")
  init("Lang")
  init('Math')
  init('Mockito')
  init('Closure')
