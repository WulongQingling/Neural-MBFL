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
  filenameList = ["major", "mBert", "merge"]
  formula = ["Dstar", "Ochiai", "Jaccard", "Op2", "Tarantula", "Gp13"]
  # formula = ["Dstar_function", "Ochiai_function", "Jaccard_function", "Op2_function", "Tarantula_function", "Gp13_function"]
  ans = {}
  for filename in filenameList:
    ans[filename] = {}
    for item in formula:
      faulty_line_rank_path = f"/home/changzexing/AveRang{filename}/{pro}/{item}.json"
      faulty_line_rank = read_json_file(faulty_line_rank_path)
      sum = 0
      num = 0
      for vid in faulty_line_rank:
        tmp = faulty_line_rank[vid]
        num += len(tmp)
        for line in tmp:
          sum += 1 / tmp[line]
      ans[filename][item] = sum / num
    map_json_path = f"/home/changzexing/Map{pro}"
    if not os.path.exists(map_json_path):
      os.makedirs(map_json_path)
    # json_str = json.dumps(ans)
    with open(f"{map_json_path}/{pro}.json", 'w') as f:
      json.dump(ans, f)
      


if __name__ == "__main__":
    init('Chart')
    init('Time')
    init('Lang')
    init('Math')