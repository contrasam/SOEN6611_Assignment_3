import understand
import sys


class CBO:

    def calculate_cbo(self, ent_class, ents_class):

        using = self.get_ents_using(ent_class,ents_class)
        uses = self.get_ents_uses(ent_class,ents_class)

        set_keys_using = set(using.keys())
        set_keys_uses = set(uses.keys())
        set_keys_classes = set(ents_class.keys())

        set_coupled = (set_keys_using.union(set_keys_uses)).intersection(set_keys_classes)
        cbo_val = len(set_coupled)

        return cbo_val;
        
    def get_ents_using(self,ent_class,ents_class):
        using = dict()
        for d in ent_class.dependsby():
            using[d.longname()] = d
        return using

    def get_ents_uses(self,ent_class,ents_class):
        uses = dict()
        for d in ent_class.depends():
            uses[d.longname()] = d
        return uses    

