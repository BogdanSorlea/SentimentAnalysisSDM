import bayescl

#print bayesclassifier.getwords("asta asta o mare mare cineva cine unde cine")

cl = bayescl.classifier(bayescl.getwords)
cl.train("ceva", 1)
cl.train("unu altu si inca 2", 2)
cl.train("mata ma-ta e proasta", 3)
cl.train("mata ma-ta e proasta", 4)
cl.train("15 435 varza", 5)

print cl.fcount("mata", 1)
print cl.fcount("mata", 2)
print cl.fcount("mata", 3)
print cl.fcount("mata", 4)
print cl.fcount("mata", 5)
