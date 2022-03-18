class Memory:
    def __init__(self, size):
        self.size = size
        self.holes = []
        self.processes = []
        self.oldP = []
        self.free_space = 0

    def mergeholes(self):
        flag = 1

        while (flag):
            holesnum = len(self.holes)
            flag = 0
            for i in range(holesnum - 1):
                print(i, holesnum, self.holes[i])
                if (self.holes[i].start_add +
                        self.holes[i].size == self.holes[i + 1].start_add):
                    print("inside IF ", i)
                    self.holes[i].size += self.holes[i + 1].size
                    self.holes.pop(i + 1)
                    flag = 1
                    break

    def add_hole(self, start_add, size):

        flag = 0

        for oldhole in self.holes:
            oldendadd = oldhole.start_add + oldhole.size
            newendadd = start_add + size

            if (start_add == oldendadd):
                flag = 1
                oldhole.size += size
                break
            elif (newendadd == oldhole.start_add):
                flag = 1
                oldhole.start_add = start_add
                oldhole.size += size
                break
        if (not flag):
            self.holes.append(Hole(start_add, size))
            self.holes.sort(key=lambda hole: hole.start_add)
        self.free_space += size
        self.mergeholes()
        # holesnum = len(self.holes)
        # for i in range(holesnum - 1):
        #     print(i, holesnum)
        #     if (self.holes[i].start_add +
        #             self.holes[i].size == self.holes[i + 1].start_add):
        #         self.holes[i].size += self.holes[i + 1].size
        #         self.holes.pop(i + 1)

    def detect_old_p(self):
        holes = self.holes
        size = len(holes)
        if (size > 0):
            if (holes[0].start_add > 0):
                old_p = Process(True)
                old_p_start = 0
                old_p_size = holes[0].start_add
                old_p.add_seg("old_process", old_p_size, old_p_start)
                self.oldP.append(old_p)
            if (holes[-1].start_add + holes[-1].size - 1) < self.size - 1:
                old_p = Process(True)
                old_p_start = holes[-1].start_add + holes[-1].size
                old_p_size = self.size - old_p_start
                old_p.add_seg("old_process", old_p_size, old_p_start)
                self.oldP.append(old_p)
        if (size > 1):
            for i in range(size - 1):
                old_p = Process(True)
                old_p_start = holes[i].start_add + holes[i].size
                old_p_size = holes[i + 1].start_add - old_p_start
                old_p.add_seg("old_process", old_p_size, old_p_start)
                self.oldP.append(old_p)

    def allocate(segments, holes, bf=False):
        size = 0
        while (size != len(segments)):

            size = len(segments)
            flag = 0
            for segment in segments:
                for hole in holes:
                    diff = hole.size - segment.size
                    if (diff > 0):
                        segment.start_add = hole.start_add
                        hole.size = diff
                        hole.start_add += segment.size
                        holes.sort(
                            key=lambda hole: hole.size) if bf == True else None
                        segments.remove(segment)
                        flag = 1
                        break
                    elif (diff == 0):
                        segment.start_add = hole.start_add
                        holes.remove(hole)
                        segments.remove(segment)
                        flag = 1
                        break
                if (flag):
                    break
        return holes, False if size > 0 else True

    # ------>  ff(first fit),bf(best fit), wf(worst fit)

    def Add_process(self, process, method="ff"):
        if (process.size <= self.free_space):
            segments = list(process.segments)
            holes = []
            is_fit = False
            if (method == "ff"):
                holes = list(self.holes)
                holes, is_fit = Memory.allocate(segments, holes)
            elif (method == "bf"):
                holes = sorted(self.holes, key=lambda hole: hole.size)
                holes, is_fit = Memory.allocate(segments, holes)
            if (is_fit):
                self.holes = sorted(holes, key=lambda hole: hole.start_add)
                process.is_alloc = True
                self.processes.append(process)
                self.free_space -= process.size
            else:
                return f"Process doesn't fit"
            del segments
            del holes

        else:
            return f"Process doesn't fit"

    def de_alloc(self, process):
        if process in self.processes or process in self.oldP:
            for segment in process.segments:
                self.add_hole(segment.start_add, segment.size)
            if process in self.processes:
                self.processes.remove(process)
            if process in self.oldP:
                self.oldP.remove(process)
            process.is_alloc = False


class Process:
    pNum = 1
    oldnum = 1

    def __init__(self, old=False):
        self.name = f"P{Process.pNum}" if old == False else f"Old_P{Process.oldnum}"
        self.segments = []
        self.segNum = 0
        self.size = 0
        self.is_alloc = False if old == False else True
        Process.pNum = Process.pNum + 1 if old == False else Process.pNum
        Process.oldnum = Process.oldnum + 1 if old == True else Process.oldnum

    def add_seg(self, name, size, start_add=-1):

        self.segments.append(Segment(name, size, start_add))
        self.size += size
        self.segNum += 1

    def __del__(self):
        for seg in self.segments:
            del seg


class Hole:
    def __init__(self, start_add, size):
        self.start_add = start_add
        self.size = size


class Segment:
    def __init__(self, name, size, start_add=-1):
        self.name = name
        self.size = size
        self.start_add = start_add
