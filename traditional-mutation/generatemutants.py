import os
import subprocess

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

def init(pid, svid, evid):
    for vid in range(svid, evid + 1):
        # 设置环境变量
        export_directory = f"/home/changzexing/d4jclean/{pid}/{vid}b/mutantsjava"
        export_variable = f'-J-Dmajor.export.directory={export_directory}'
        os.environ['MAJOR_OPT'] = f'-J-Dmajor.export.mutants=true {export_variable}'
        # 获取失败的测试变量
        failing_tests = f"/home/changzexing/d4jclean/{pid}/{vid}b/failing_tests"
        if not os.path.exists(failing_tests):
            continue
        # 执行命令
        command = f'defects4j mutation -w /home/changzexing/d4jclean/{pid}/{vid}b -t {failing_tests}'
        output, error = execute_command(command)
        # 检查命令执行结果
        # if error:
        #     print(f'{pid}-{vid}b 失败 {error}')
        # else:
        #     print(f'{pid}-{vid}b 成功')
        # break
        print(f'{pid}-{vid}b 完成')

if __name__ == '__main__':
    init('Chart', 3, 26)
    # init('Cli', 1, 40)
    # init('Csv', 1, 16)
    init('Time', 1, 27)
    init('Lang', 1, 65)
    init('Math', 1, 106)