import devfx.multiprocessing as mproc
import devfx.diagnostics as dgn
import time

class TargetArgs(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p1

class TargetResult(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p1

class Targets(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def target1(self, args):
        time.sleep(2)
        print(self.p1, self.p2)
        print(args.p1, args.p2)
        return TargetResult('target1', 'target1')

    def target2(self, args):
        time.sleep(2)
        print(self.p1, self.p2)
        print(args.p1, args.p2)
        return TargetResult('target2', 'target2')

def main():
    sw = dgn.stopwatch().start()

    targets = Targets(4, 4)

    process1 = mproc.Process(targets.target1, args=TargetArgs(1, 1))
    process1.start()

    process2 = mproc.Process(targets.target2, args=TargetArgs(2, 2))
    process2.start()

    process1.join()
    process2.join()

    if(process1.result_is_exception()):
        print(process1.result)
    else:
        print(process1.result.p1, process1.result.p2)

    if(process2.result_is_exception()):
        print(process2.result)
    else:
        print(process2.result.p1, process2.result.p2)

    print("time elapsed: ", sw.stop().elapsed)

if(__name__ == '__main__'):
    main()

