import understand
import sys


class LCOM:

    def calculate_lcom(self, ent_class):

        subcomponents = self.get_connected_components(ent_class)
        subcomponents = self.calculate(subcomponents)

        lcom = len(subcomponents)

        return lcom

    def get_connected_components(self,ent_class):

        connected_by_attribute = self.get_connected_by_attribute(ent_class)
        connected_by_method_call = self.get_connected_by_method_call(ent_class)

        subcomponents = connected_by_attribute + connected_by_method_call

        return subcomponents 

    def get_connected_by_attribute(self,ent_class):
        connected_subcomponents = []
        ref_instances = []

        for ref in ent_class.refs("Define", "Object"):
            ref_instances.append(ref.ent())

        for inst in ref_instances:
            used_by = inst.ents("Useby", "Function")
            used_set = set([])
            for u in used_by:
                used_set.add(str(u))
            connected_subcomponents.append(used_set)

        return connected_subcomponents

    def get_connected_by_method_call(self,ent_class):
        connected_subcomponents = []
        ref_methods = []

        for ref in ent_class.refs("Define", "Function"):
            ref_methods.append(ref.ent())

        for meth in ref_methods:
            calling = meth.ents("Call", "Function")
            used_set = set([])
            for u in calling:
                if u in ref_methods:
                    used_set.add(str(u))
            used_set.add(str(meth))
            if len(used_set) > 1:
                connected_subcomponents.append(used_set)

        return connected_subcomponents

    def union_subcomponents(self, subcomponent_x, subcomponent_y):
        if (subcomponent_x.isdisjoint(subcomponent_y)):
            return subcomponent_x
        else:
            return subcomponent_x.union(subcomponent_y)

    def is_disconnected(self, subcomponents):

        is_disjoint = True

        for x in subcomponents:
            for y in subcomponents:
                if (x != y):
                    is_disjoint = (is_disjoint and x.isdisjoint(y))

        return is_disjoint

    def calculate(self, subcomponents):
        if (self.is_disconnected(subcomponents)):
            return subcomponents
        else:
            k = []
            for x in subcomponents:
                z = x
               
                for i in k:
                    if (z.issubset(i)):
                        break
                else:
                    for y in subcomponents:
                        z = self.union_subcomponents(z, y)

                    k.append(z)
                
            return self.calculate(k)
