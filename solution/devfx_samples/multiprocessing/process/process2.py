import time
import devfx.multiprocessing as mproc
import devfx.diagnostics as dgn
import devfx.reflection as refl

class TargetArgs(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p1

class TargetResult(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p1

class Targets(object):
    @classmethod
    def target1(cls, args):
        time.sleep(2)
        print(args.p1, args.p2)
        return TargetResult('target1', 'target1')

    @classmethod
    def target2(cls, args):
        time.sleep(2)
        print(args.p1, args.p2)
        return TargetResult('target2', 'target2')

def main():
    sw = dgn.stopwatch().start()

    process1 = mproc.Process(target=Targets.target1, args=(TargetArgs(1, 1), ))
    process1.start()

    process2 = mproc.Process(target=Targets.target2, args=(TargetArgs(2, 3), ))
    process2.start()

    process1.join()
    process2.join()

    if(process1.result.is_exception()):
        print(process1.result.value)
    else:
        print(process1.result.value.p1, process1.result.value.p2)

    if(process2.result.is_exception()):
        print(process2.result.value)
    else:
        print(process2.result.value.p1, process2.result.value.p2)

    print("time elapsed: ", sw.stop().elapsed)

if(__name__ == '__main__'):
    main()
