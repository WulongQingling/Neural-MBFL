import json
import logging
import math
import operator
import os
import pickle
import sys
from execute.FOM import executeFom, generateFom
from execute.SOM import executeSom, generateSom
from tool.config_variables import (SOMfaultlocalizationResultPath, djSrcPath,
                                   faliingTestOutputPath,
                                   faultlocalizationResultPath, mbflMethods,
                                   mutantsFilePath, outputCleanPath, password,
                                   project, sbflMethod, sourcePath,
                                   tempSrcPath, tpydataPath, method_names)
from tool.logger_config import logger_config
from tool.mbfl_formulas import (binary, crosstab, dstar, gp13, jaccard, naish1,
                                ochiai, op2, russell, turantula)
from tool.other import checkAndCreateDir, clearDir, run
from tool.remote_transmission import (cp_from_remote, get_host_ip, ip,
                                      sftp_upload)

def calSbfl(project, version):
    if os.path.exists(faultlocalizationResultPath + "/" + project + "/" + version + "/susStatement/sbfl.json"):
        with open(faultlocalizationResultPath + "/" + project + "/" + version + "/susStatement/sbfl.json", 'r') as f:
            susResult = json.load(f)
    else:
        sus1 = dict()
        susResult = dict()
        with open(faultlocalizationResultPath + "/" + project + "/" + version + "/suspiciousSbfl.json", 'r') as f:
            sus1 = json.load(f)

        for key in sus1.keys():
            for key1 in sus1[key].keys():
                if key1 in method_names:
                    if susResult.get(key[1:]) == None:
                        susResult[key[1:]] = dict()
                    susResult[key[1:]][key1] = sus1[key][key1]
        # print(os.path.dirname(resultPath))
        checkAndCreateDir(os.path.dirname(faultlocalizationResultPath + "/" + project + "/" + version + "/susStatement/"))
        with open(faultlocalizationResultPath + "/" + project + "/" + version + "/susStatement/sbfl.json", 'w') as f:
            f.write(json.dumps(susResult, indent=2))
    if os.path.exists(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction/sbfl.json"):
        with open(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction/sbfl.json", 'r') as f:
            functionSus = json.load(f)
    else:
        with open("../../d4j/hugeToFunction/" + project + "/" + version + "/HugetoFunction.in", 'rb') as f:
            hugeToFunction = pickle.load(f)
        with open(outputCleanPath + "/" + project + "/" + version + "/faultHuge_Function.in", 'rb') as f:
            faultHuge_Function = pickle.load(f)
        with open(outputCleanPath + "/" + project + "/" + version + "/FunctionList.txt", 'r') as f:
            FunctionList = f.readlines()
        with open(outputCleanPath + "/" + project + "/" + version + "/HugeToFile.txt", 'r') as f:
            hugeToFile = f.readlines()

        hugeToFiledict = dict()
        for i in range(0,len(hugeToFile)):
            if hugeToFiledict.get(hugeToFile[i].split("\t")[0]) == None:
                hugeToFiledict[hugeToFile[i].split("\t")[0]] = dict()
            functionLine = hugeToFunction[i] + 1
            count = sum(1 for element in FunctionList[0:functionLine] if FunctionList[functionLine-1].split(":")[0] in element)
            hugeToFiledict[hugeToFile[i].split("\t")[0]][hugeToFile[i].split("\t")[1].strip()] = count
        checkAndCreateDir(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction")

        functionSus = {}
        for key in susResult.keys():
            functionSus[key] = dict()
            for method in susResult[key].keys():
                functionSus[key][method] = dict()
                for line in susResult[key][method].keys():
                    for k in hugeToFiledict.keys():
                        if k in key:
                            break
                    if hugeToFiledict[k].get(str(int(line)-1)) == None:
                        continue
                    count = hugeToFiledict[k][str(int(line)-1)]
                    if functionSus[key][method].get(count)==None:
                        functionSus[key][method][count] = susResult[key][method][line]
        with open(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction/sbfl.json", 'w') as f:
            f.write(json.dumps(functionSus, indent=2))
    return susResult, functionSus

def calFomMbfl(project, version, muInfoList, resultList):
    """
    通过变异体的执行矩阵和杀死矩阵计算语句怀疑度
    :param Fom: 变异体的信息,主要用到行号
    :param FomResult: 变异体的执行结果和杀死信息,数组形式存储,第一个是执行结果,第二个是杀死信息.
                      执行结果: 1代表失败,0代表通过
                      杀死信息: 1代表杀死,0代表没杀死
    :return: 变异体信息列表
    """
    try:
        suspiciousFirstOrderPath = os.path.join(
            faultlocalizationResultPath, project, version, "susStatement", "complete.json")
        susResult = {}
        for j in range(1, 5):
            susResult[f'type{j}'] = dict()
            if resultList == None:
                resultList = []
            for i in range(0, len(resultList)):
                if resultList[i]["status"] == 0:
                    continue
                Anp = 0
                Anf = 0
                Akp = 0
                Akf = 0
                if susResult[f'type{j}'].get(muInfoList[i]['relativePath']) == None:
                    susResult[f'type{j}'][muInfoList[i]['relativePath']] = dict()
                for index in range(0, len(resultList[i]["passList"][f'type{j}'])):
                    if resultList[i]["passList"][f'type{j}'][index] == 1:
                        if resultList[i]["killList"][f'type{j}'][index] == 1:
                            Akf += 1
                        else:
                            Anf += 1
                    else:
                        if resultList[i]["killList"][f'type{j}'][index] == 1:
                            Akp += 1
                        else:
                            Anp += 1
                with open('./b.txt', mode='a', newline='') as file:
                    print(Akf, Akp, Anf, Anp, file=file)
                for method in mbflMethods:
                    if susResult[f'type{j}'][muInfoList[i]['relativePath']].get(str(method).split(" ")[1]) == None:
                        susResult[f'type{j}'][muInfoList[i]['relativePath']][str(method).split(" ")[1]] = dict()
                    if susResult[f'type{j}'][muInfoList[i]['relativePath']][str(method).split(" ")[1]].get(resultList[i]["linenum"]) == None:
                        susResult[f'type{j}'][muInfoList[i]['relativePath']][str(method).split(" ")[1]][resultList[i]["linenum"]] = method(Akf, Anf, Akp, Anp)
                    else:
                        susResult[f'type{j}'][muInfoList[i]['relativePath']][str(method).split(" ")[1]][resultList[i]["linenum"]] = max(
                            susResult[f'type{j}'][muInfoList[i]['relativePath']][str(method).split(" ")[1]][resultList[i]["linenum"]], method(Akf, Anf, Akp, Anp)
                        )
                for item in susResult[f'type{j}'].keys():
                    for method in mbflMethods:
                        susResult[f'type{j}'][item][str(method).split(" ")[1]] = dict(sorted(susResult[f'type{j}'][item][str(method).split(" ")[1]].items(),
                                                                                key=operator.itemgetter(1), reverse=True))

        checkAndCreateDir(os.path.join(faultlocalizationResultPath, project))
        checkAndCreateDir(os.path.join(faultlocalizationResultPath, project, version))
        checkAndCreateDir(os.path.join(faultlocalizationResultPath, project, version, 'susStatement'))
        with open(suspiciousFirstOrderPath, 'w') as f:
            f.write(json.dumps(susResult, indent=2))
        if ip != '202.4.130.30':
            sftp_upload('202.4.130.30', 'fanluxi', password,
                     suspiciousFirstOrderPath, suspiciousFirstOrderPath)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')

def countFunctionSus(project, version):
    try:
        with open("../../d4j/hugeToFunction/" + project + "/" + version + "/HugetoFunction.in", 'rb') as f:
            hugeToFunction = pickle.load(f)
        with open("../../d4j/outputClean/" + project + "/" + version + "/faultHuge_Function.in", 'rb') as f:
            faultHuge_Function = pickle.load(f)
        with open("../../d4j/outputClean/" + project + "/" + version + "/FunctionList.txt", 'r') as f:
            FunctionList = f.readlines()
        with open("../../d4j/outputClean/" + project + "/" + version + "/HugeToFile.txt", 'r') as f:
            hugeToFile = f.readlines()
        #region 生成 falutFunction.json
        falutFunction = dict()
        for key in faultHuge_Function.keys():
            falutFunction[key] = list()
            for line in faultHuge_Function[key]:
                # XSQ
                count = sum(1 for element in FunctionList[0:line] if FunctionList[line].split(":")[0] in element) + 1
                # fanluxi
                # count = sum(1 for element in FunctionList[0:line] if FunctionList[line-1].split(":")[0] in element) + 1
                if count not in falutFunction[key]:
                    falutFunction[key].append(count)
        with open(faultlocalizationResultPath + "/" + project + "/" + version + "/falutFunction.json", 'w') as f:
            f.write(json.dumps(falutFunction, indent=2))
        #endregion

        hugeToFiledict = dict()
        for i in range(0,len(hugeToFile)):
            if hugeToFiledict.get(hugeToFile[i].split("\t")[0]) == None:
                hugeToFiledict[hugeToFile[i].split("\t")[0]] = dict()
            functionLine = hugeToFunction[i] + 1
            count = sum(1 for element in FunctionList[0:functionLine] if FunctionList[functionLine-1].split(":")[0] in element)
            hugeToFiledict[hugeToFile[i].split("\t")[0]][hugeToFile[i].split("\t")[1].strip()] = count

        suspiciousPath = faultlocalizationResultPath + "/" + project + "/" + version + "/susStatement"
        for root, dirs, files in os.walk(suspiciousPath):
            for file in files:
                checkAndCreateDir(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction")
                functionSus = dict()
                file_path = os.path.join(root, file)
                # if os.path.exists(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction/" + file):
                #     continue
                if file == 'sbfl.json':
                    continue
                with open(file_path, 'r') as f:
                    sus = json.load(f)
                for j in range(1, 5):
                    functionSus[f'type{j}'] = dict()
                    for key in sus[f'type{j}'].keys():
                        functionSus[f'type{j}'][key] = dict()
                        for method in sus[f'type{j}'][key].keys():
                            functionSus[f'type{j}'][key][method] = dict()
                            for line in sus[f'type{j}'][key][method].keys():
                                for k in hugeToFiledict.keys():
                                    if k in key:
                                        break
                                if hugeToFiledict[k].get(str(int(line)-1)) == None:
                                    continue
                                count = hugeToFiledict[k][str(int(line)-1)]
                                if functionSus[f'type{j}'][key][method].get(count)==None:
                                    functionSus[f'type{j}'][key][method][count] = sus[f'type{j}'][key][method][line]
                with open(faultlocalizationResultPath + "/" + project + "/" + version + "/susFunction/" + file, 'w') as f:
                    f.write(json.dumps(functionSus, indent=2))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')

def calTopNMbflAverage(project, version, susResult, FileName, FaultFile, dir):
    try:
        topNResult = dict()
        with open(os.path.join(faultlocalizationResultPath, project, version, FaultFile), 'r')as f:
            faultLocalization = json.load(f)
        if FileName == 'sbfl.json':
            for key in faultLocalization.keys():
                topNResult[key] = dict()
                for line in faultLocalization[key]:
                    topNResult[key][line] = dict()
                    f = key[1:]
                    if susResult.get(f) is None:
                        for method in mbflMethods:
                            topNResult[key][line][str(method).split(" ")[1]] = -1
                        continue
                    for method in susResult[f].keys():
                        susOfFaultStatement={}
                        for i in range(len(faultLocalization[key])):
                            if susResult[f][method].get(str(faultLocalization[key][i])) == None:
                                susOfFaultStatement[faultLocalization[key][i]] = -math.inf
                            else:
                                susOfFaultStatement[faultLocalization[key][i]] = susResult[f][method][str(faultLocalization[key][i])]
                        startFlagIndex=-1
                        repeatFaultTime=0
                        endFlagIndex=-1
                        ind = 0
                        for item, value in susResult[f][method].items():
                            ind += 1
                            if math.isnan(value):
                                continue
                            if value > susOfFaultStatement[line]:
                                continue
                            if value == susOfFaultStatement[line]:
                                if startFlagIndex == -1:
                                    startFlagIndex = ind
                                else:
                                    if int(item) in faultLocalization[key]:
                                        repeatFaultTime += 1
                            else:
                                endFlagIndex = ind-1-repeatFaultTime
                                break
                        if endFlagIndex == -1:
                            endFlagIndex = ind
                        if startFlagIndex == -1 or endFlagIndex == -1:
                            topNResult[key][line][method] = -1
                        else:
                            topNResult[key][line][method] = (startFlagIndex+endFlagIndex)/2
            checkAndCreateDir(os.path.join(
                faultlocalizationResultPath, project, version, dir))
            with open(os.path.join(faultlocalizationResultPath, project, version, dir, FileName), 'w') as f:
                f.write(json.dumps(topNResult, indent=2))
            return topNResult
        for j in range(1, 5):
            topNResult[f'type{j}'] = dict()
            for key in faultLocalization.keys():
                topNResult[f'type{j}'][key] = dict()
                for line in faultLocalization[key]:
                    topNResult[f'type{j}'][key][line] = dict()
                    f = key[1:]
                    if susResult[f'type{j}'].get(f) is None:
                        for method in mbflMethods:
                            topNResult[f'type{j}'][key][line][str(method).split(" ")[1]] = -1
                        continue
                    for method in susResult[f'type{j}'][f].keys():
                        susOfFaultStatement={}
                        for i in range(len(faultLocalization[key])):
                            if susResult[f'type{j}'][f][method].get(str(faultLocalization[key][i])) == None:
                                susOfFaultStatement[faultLocalization[key][i]] = -math.inf
                            else:
                                susOfFaultStatement[faultLocalization[key][i]] = susResult[f'type{j}'][f][method][str(faultLocalization[key][i])]
                        startFlagIndex=-1
                        repeatFaultTime=0
                        endFlagIndex=-1
                        ind = 0
                        for item, value in susResult[f'type{j}'][f][method].items():
                            ind += 1
                            if math.isnan(value):
                                continue
                            if value > susOfFaultStatement[line]:
                                continue
                            if value == susOfFaultStatement[line]:
                                if startFlagIndex == -1:
                                    startFlagIndex = ind
                                else:
                                    if int(item) in faultLocalization[key]:
                                        repeatFaultTime += 1
                            else:
                                endFlagIndex = ind-1-repeatFaultTime
                                break
                        if endFlagIndex == -1:
                            endFlagIndex = ind
                        if startFlagIndex == -1 or endFlagIndex == -1:
                            topNResult[f'type{j}'][key][line][method] = -1
                        else:
                            topNResult[f'type{j}'][key][line][method] = (startFlagIndex+endFlagIndex)/2
        checkAndCreateDir(os.path.join(
            faultlocalizationResultPath, project, version, dir))
        with open(os.path.join(faultlocalizationResultPath, project, version, dir, FileName), 'w') as f:
            f.write(json.dumps(topNResult, indent=2))
        return topNResult
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')

def calTopNMbflBest(project, version, susResult, FileName, FaultFile, dir):
    try:
        topNResult = dict()
        with open(os.path.join(faultlocalizationResultPath, project, version, FaultFile), 'r')as f:
            faultLocalization = json.load(f)
        if FileName == "sbfl.json":
            for key in faultLocalization.keys():# 遍历所有错误文件
                topNResult[key] = dict()
                for line in faultLocalization[key]:# 遍历所有错误行
                    topNResult[key][line] = dict()
                    f = key[1:]
                    if susResult.get(f) is None:
                        for method in mbflMethods:
                            topNResult[key][line][str(method).split(" ")[1]] = -1
                        continue
                    for method in susResult[f].keys():
                        susOfFaultStatement={}
                        for i in range(len(faultLocalization[key])):# 拿到错误语句的怀疑度分数
                            if susResult[f][method].get(str(faultLocalization[key][i])) == None:
                                susOfFaultStatement[faultLocalization[key][i]] = -math.inf
                            else:
                                susOfFaultStatement[faultLocalization[key][i]] = susResult[f][method][str(faultLocalization[key][i])]
                        startFlagIndex=-1
                        repeatFaultTime=0
                        endFlagIndex=-1
                        ind = 0
                        for item, value in susResult[f][method].items():
                            ind += 1
                            if math.isnan(value):
                                continue
                            if value > susOfFaultStatement[line]:
                                continue
                            if value == susOfFaultStatement[line]:
                                if startFlagIndex == -1:
                                    startFlagIndex = ind
                                else:
                                    if int(item) in faultLocalization[key]:
                                        repeatFaultTime += 1
                            else:
                                endFlagIndex = ind-1-repeatFaultTime
                                break
                        topNResult[key][line][method] = startFlagIndex
            checkAndCreateDir(os.path.join(
                faultlocalizationResultPath, project, version, dir))
            with open(os.path.join(faultlocalizationResultPath, project, version, dir, FileName), 'w') as f:
                f.write(json.dumps(topNResult, indent=2))
            return topNResult
        for j in range(1, 5):# 为什么没有else
            topNResult[f'type{j}'] = dict()
            for key in faultLocalization.keys():
                topNResult[f'type{j}'][key] = dict()
                for line in faultLocalization[key]:
                    topNResult[f'type{j}'][key][line] = dict()
                    f = key[1:]
                    if susResult[f'type{j}'].get(f) is None:
                        for method in mbflMethods:
                            topNResult[f'type{j}'][key][line][str(method).split(" ")[1]] = -1
                        continue
                    for method in susResult[f'type{j}'][f].keys():
                        susOfFaultStatement={}
                        for i in range(len(faultLocalization[key])):
                            if susResult[f'type{j}'][f][method].get(str(faultLocalization[key][i])) == None:
                                susOfFaultStatement[faultLocalization[key][i]] = -math.inf
                            else:
                                susOfFaultStatement[faultLocalization[key][i]] = susResult[f'type{j}'][f][method][str(faultLocalization[key][i])]
                        startFlagIndex=-1
                        repeatFaultTime=0
                        endFlagIndex=-1
                        ind = 0
                        for item, value in susResult[f'type{j}'][f][method].items():
                            ind += 1
                            if math.isnan(value):
                                continue
                            if value > susOfFaultStatement[line]:
                                continue
                            if value == susOfFaultStatement[line]:
                                if startFlagIndex == -1:
                                    startFlagIndex = ind
                                else:
                                    if int(item) in faultLocalization[key]:
                                        repeatFaultTime += 1
                            else:
                                endFlagIndex = ind-1-repeatFaultTime
                                break

                        topNResult[f'type{j}'][key][line][method] = startFlagIndex

        checkAndCreateDir(os.path.join(
            faultlocalizationResultPath, project, version, dir))
        with open(os.path.join(faultlocalizationResultPath, project, version, dir, FileName), 'w') as f:
            f.write(json.dumps(topNResult, indent=2))
        return topNResult
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')

def calTopNMbflWorst(project, version, susResult, FileName, FaultFile, dir):
    try:
        topNResult = dict()
        with open(os.path.join(faultlocalizationResultPath, project, version, FaultFile), 'r')as f:
            faultLocalization = json.load(f)

        if FileName == "sbfl.json":
            for key in faultLocalization.keys():
                topNResult[key] = dict()
                for line in faultLocalization[key]:
                    topNResult[key][line] = dict()
                    f = key[1:]
                    if susResult.get(f) is None:
                        for method in mbflMethods:
                            topNResult[key][line][str(method).split(" ")[1]] = -1
                        continue
                    for method in susResult[f].keys():
                        susOfFaultStatement={}
                        for i in range(len(faultLocalization[key])):
                            if susResult[f][method].get(str(faultLocalization[key][i])) == None:
                                susOfFaultStatement[faultLocalization[key][i]] = -math.inf
                            else:
                                susOfFaultStatement[faultLocalization[key][i]] = susResult[f][method][str(faultLocalization[key][i])]
                        startFlagIndex=-1
                        repeatFaultTime=0
                        endFlagIndex=-1
                        ind = 0
                        for item, value in susResult[f][method].items():
                            ind += 1
                            if math.isnan(value):
                                continue
                            if value > susOfFaultStatement[line]:
                                continue
                            if value == susOfFaultStatement[line]:
                                if startFlagIndex == -1:
                                    startFlagIndex = ind
                                else:
                                    if int(item) in faultLocalization[key]:
                                        repeatFaultTime += 1
                            else:
                                endFlagIndex = ind-1-repeatFaultTime
                                break
                        topNResult[key][line][method] = endFlagIndex
            checkAndCreateDir(os.path.join(
                faultlocalizationResultPath, project, version, dir))
            with open(os.path.join(faultlocalizationResultPath, project, version, dir, FileName), 'w') as f:
                f.write(json.dumps(topNResult, indent=2))
            return topNResult
        for j in range(1, 5):
            topNResult[f'type{j}'] = dict()
            for key in faultLocalization.keys():
                topNResult[f'type{j}'][key] = dict()
                for line in faultLocalization[key]:
                    topNResult[f'type{j}'][key][line] = dict()
                    f = key[1:]
                    if susResult[f'type{j}'].get(f) is None:
                        for method in mbflMethods:
                            topNResult[f'type{j}'][key][line][str(method).split(" ")[1]] = -1
                        continue
                    for method in susResult[f'type{j}'][f].keys():
                        susOfFaultStatement={}
                        for i in range(len(faultLocalization[key])):
                            if susResult[f'type{j}'][f][method].get(str(faultLocalization[key][i])) == None:
                                susOfFaultStatement[faultLocalization[key][i]] = -math.inf
                            else:
                                susOfFaultStatement[faultLocalization[key][i]] = susResult[f'type{j}'][f][method][str(faultLocalization[key][i])]
                        startFlagIndex=-1
                        repeatFaultTime=0
                        endFlagIndex=-1
                        ind = 0
                        for item, value in susResult[f'type{j}'][f][method].items():
                            ind += 1
                            if math.isnan(value):
                                continue
                            if value > susOfFaultStatement[line]:
                                continue
                            if value == susOfFaultStatement[line]:
                                if startFlagIndex == -1:
                                    startFlagIndex = ind
                                else:
                                    if int(item) in faultLocalization[key]:
                                        repeatFaultTime += 1
                            else:
                                endFlagIndex = ind-1-repeatFaultTime
                                break

                        topNResult[f'type{j}'][key][line][method] = endFlagIndex

        checkAndCreateDir(os.path.join(
            faultlocalizationResultPath, project, version, dir))
        with open(os.path.join(faultlocalizationResultPath, project, version, dir, FileName), 'w') as f:
            f.write(json.dumps(topNResult, indent=2))
        return topNResult
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        print(f'\033[1;31mError in {file_name} at line {line_number}: {e}\033[0m')
        logging.error(f'Error in {file_name} at line {line_number}: {e}')