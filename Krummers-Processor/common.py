class CustomTrackDistributions(object):
    
    class Line(object):
        
        def __init__(self, name, version, ct_id, dis_id):
            self.name = name
            if version == None:
                self.version = None
            else:
                self.version = str(version)
            self.ct_id = ct_id
            self.dis_id = dis_id
            
            if name.startswith("A "):
                self.sort = name[2:].lower()
            elif name.startswith("The "):
                self.sort = name[4:].lower()
            elif name.startswith("s☆Ris"):
                self.sort = "s{}ris CT Pack".format(chr(ord("a") - 1)).lower()
            else:
                self.sort = name.lower()
        
        def __str__(self):
            if self.version == None:
                return "* {{{{Distrib-ref|{}|{}|{}}}}}".format(self.name, self.ct_id, self.dis_id)
            else:
                return "* [[{}]] ({})".format(self.name, self.version)
        
        def __repr__(self):
            r = self.name
            
            if self.version != None:
                r += " " + self.version
            
            if self.ct_id != None:
                r += " (" + str(self.ct_id) + ")"
            
            if self.dis_id != None:
                r += " (" + str(self.dis_id) + ")"
            
            return r
        
    def __init__(self, text):
        s = text.find("distribution]]s:\n")
        if s == -1:
            self.distributions == None
            return
        text = text[s + 17:]
        s = text.find("\n\n")
        if s != -1:
            text = text[:s]
                
        if text == "* (none)":
            self.distributions = None
            return
        
        l = text.split("\n")
        distributions = []
        
        for k in range(len(l)):
            if l[k][2] == "{":
                s = l[k].find("|") + 1
                l[k] = l[k][s:]
                s = l[k].find("|")
                name = l[k][:s]
                l[k] = l[k][s + 1:]
                s = l[k].find("|")
                ct_id = l[k][:s]
                l[k] = l[k][s + 1:]
                s = l[k].find("}")
                dis_id = l[k][:s]
                line = CustomTrackDistributions.Line(name, None, ct_id, dis_id)
            elif l[k][2] == "[":
                name = l[k][4:l[k].rfind("]") - 1]
                version = l[k][l[k].rfind("(") + 1:l[k].rfind(")")]
                line = CustomTrackDistributions.Line(name, version, None, None)
            distributions.append(line)
        
        self.distributions = distributions
    
    def __str__(self):
        l = [str(line) for line in self.distributions]
        return "\n".join(l)
    
    def __repr__(self):
        return self.distributions.__repr__()
    
    def sort_by_name(self):
        self.distributions = sorted(self.distributions, key = lambda l:l.sort)