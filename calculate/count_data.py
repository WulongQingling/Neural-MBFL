import os
import json
from collections import Counter
from tool.config_variables import tempSrcPath, tpydataPath, outputCleanPath, djSrcPath, mutantsFilePath, faliingTestOutputPath, faultlocalizationResultPath, SOMfaultlocalizationResultPath, sbflMethod, sourcePath, password, project, mbflMethods, FOMprocessedData
from tool.remote_transmission import ip, get_host_ip, sftp_upload, cp_from_remote
from tool.logger_config import logger_config
from tool.mbfl_formulas import dstar, ochiai, gp13, op2, jaccard, russell, turantula, naish1, binary, crosstab
from tool.other import clearDir, checkAndCreateDir, run
from execute.FOM import generateFom, executeFom
from execute.SOM import generateSom, executeSom
def countTonN(root_path, project, mode):
    """
    遍历指定目录下所有子目录是否存在指定文件,如果存在则使用json.load读取文件内容
    """
    projectStatistics = dict()
    for version in os.listdir(root_path + "/" + project):
        for root, dirs, files in os.walk(root_path + "/" + project + "/" + version + "/" +mode):
            # 遍历当前目录下的所有文件
            for filename in files:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                if filename == 'sbfl.json':
                    if filename not in projectStatistics:
                        projectStatistics[filename] = dict()
                    for key in data.keys():
                        for line in data[key].keys():
                            for item in data[key][line].keys():
                                if item not in projectStatistics[filename]:
                                    projectStatistics[filename][item] = Counter({'top1': 0, 'top2': 0, 'top3': 0, 'top4': 0, 'top5': 0, 'top10': 0})
                                if data[key][line][item] <= 10 and data[key][line][item] >= 0:
                                    projectStatistics[filename][item]['top10'] += 1
                                if data[key][line][item] <= 5 and data[key][line][item] >= 0:
                                    projectStatistics[filename][item]['top5'] += 1
                                if data[key][line][item] <= 4 and data[key][line][item] >= 0:
                                    projectStatistics[filename][item]['top4'] += 1
                                if data[key][line][item] <= 3 and data[key][line][item] >= 0:
                                    projectStatistics[filename][item]['top3'] += 1
                                if data[key][line][item] <= 2 and data[key][line][item] >= 0:
                                    projectStatistics[filename][item]['top2'] += 1
                                if data[key][line][item] <= 1 and data[key][line][item] >= 0:
                                    projectStatistics[filename][item]['top1'] += 1
                else:
                    if projectStatistics.get(filename) == None:
                        projectStatistics[filename] = dict()
                    for j in range(1, 5):
                        if projectStatistics[filename].get(f'type{j}') == None:
                            projectStatistics[filename][f'type{j}'] = dict()
                        for key in data[f'type{j}'].keys():
                            for line in data[f'type{j}'][key].keys():
                                for item in data[f'type{j}'][key][line].keys():
                                    if item not in projectStatistics[filename][f'type{j}']:
                                        projectStatistics[filename][f'type{j}'][item] = Counter({'top1': 0, 'top2': 0, 'top3': 0, 'top4': 0, 'top5': 0, 'top10': 0})
                                    if data[f'type{j}'][key][line][item] <= 10 and data[f'type{j}'][key][line][item] >= 0:
                                        projectStatistics[filename][f'type{j}'][item]['top10'] += 1
                                    if data[f'type{j}'][key][line][item] <= 5 and data[f'type{j}'][key][line][item] >= 0:
                                        projectStatistics[filename][f'type{j}'][item]['top5'] += 1
                                    if data[f'type{j}'][key][line][item] <= 4 and data[f'type{j}'][key][line][item] >= 0:
                                        projectStatistics[filename][f'type{j}'][item]['top4'] += 1
                                    if data[f'type{j}'][key][line][item] <= 3 and data[f'type{j}'][key][line][item] >= 0:
                                        projectStatistics[filename][f'type{j}'][item]['top3'] += 1
                                    if data[f'type{j}'][key][line][item] <= 2 and data[f'type{j}'][key][line][item] >= 0:
                                        projectStatistics[filename][f'type{j}'][item]['top2'] += 1
                                    if data[f'type{j}'][key][line][item] <= 1 and data[f'type{j}'][key][line][item] >= 0:
                                        projectStatistics[filename][f'type{j}'][item]['top1'] += 1
    checkAndCreateDir(FOMprocessedData)
    checkAndCreateDir(FOMprocessedData + "/" + mode)
    with open(FOMprocessedData + "/" + mode +"/" + project, 'w') as f:
        f.write(json.dumps(projectStatistics, indent=2))