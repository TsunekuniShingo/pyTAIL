import re

class NCparser:
    def __init__(self,nc,identifier=['X','Y','Z','B','C']):
        self.nc = nc
        self.identifier = identifier

        self.active_value = {key:0.0 for key in identifier}
        self.CL = {key:[] for key in identifier}

        self.pat = re.compile('[a-zA-Z][^a-zA-Z]+')

    
    def toCL(self):
        ncs  = self.nc.split('\n')
        for t in ncs:
            if t=='': continue
            if '(' in t: continue
            if self.pat.search(t):
                j = self.__div(t)
                if j:
                    [self.CL[key].append(value) for key,value in self.active_value.items()]


    def __div(self,string):
        segments = self.pat.findall(string)
        j = [s[0] in self.identifier for s in segments]
        if not any(j): return False

        for s in segments:
            if s[0] in self.identifier:
                self.active_value[s[0]] = float(s[1:])
        return True
        