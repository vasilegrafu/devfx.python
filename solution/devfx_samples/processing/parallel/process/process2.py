import time
import devfx.core as core
import devfx.diagnostics as dgn
import devfx.processing as processing

class Targets(object):
    @classmethod
    def target1(cls, p1, p2):
        time.sleep(2)
        print(p1, p2)
        return (p1, p2)

    @classmethod
    def target2(cls, p1, p2):
        time.sleep(2)
        print(p1, p2)
        return (p1, p2)

def main():
    sw = dgn.stopwatch().start()

    process1 = processing.parallel.Process(fn=Targets.target1, args=(1, 1))
    process1.start()

    process2 = processing.parallel.Process(fn=Targets.target2, args=(2, 2))
    process1.start()

    process1.join()
    process2.join()

    print(process1.result)

    print(process2.result)

    print("time elapsed: ", sw.stop().elapsed)

if(__name__ == '__main__'):
    main()

