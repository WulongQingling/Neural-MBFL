import os
import subprocess
import signal

#执行测试
def run_d4j_test(run_path, process_name):
    # 构造命令行参数
    cmd = ["defects4j", "test", "-w", run_path, "$1>/dev/null", "2>&1"]
    # 设置超时时间
    timeout_seconds = 600
    # 调用subprocess.Popen()函数创建子进程执行命令
    try:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid) as proc:
            try:
                stdout, stderr = proc.communicate(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                print("{} 执行测试超时 {}".format(run_path, process_name))
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM) # 强制杀死子进程
                return False
            if proc.returncode == 0:
                print("{} 执行测试成功 {}".format(run_path, process_name))
                return True
            else:
                print("{} 执行测试失败 {}".format(run_path, process_name))
                return False
    except subprocess.CalledProcessError as e:
        print("{} 执行测试失败".format(run_path))
        return False
    
def init(pid, svid, evid):
    for vid in range(svid, evid + 1):
      runPath = "/home/rs/Work/Projects/D4JClean/d4jclean/{}/{}b".format(pid, vid)
      if not os.path.exists(runPath):
          continue
      run_d4j_test(runPath, '')

if __name__ == '__main__':
    init('Chart', 1, 26)
    # init('Time', 1, 27)
    # init('Lang', 1, 65)
    # init('Math', 1, 106)
