#!/usr/bin/python
import apt_pkg
import sys
import apt
import pydot as pd

class debname:
	def __init__(self,name,size):
		self.name = name
		self.size = size
		self.deplist = []


def dependencies(cache, pkg, deps, key="Depends"):
    candver = cache._depcache.GetCandidateVer(pkg._pkg)
    tempobj = debname(pkg.name,candver.size)
    if candver == None:
        return deps
    if(pkg.name not in tobeinstalled[currentpkg]):
	tobeinstalled[currentpkg].append(pkg.name)
    dependslist = candver.DependsList
    if dependslist.has_key(key):
        for depVerList in dependslist[key]:
            for dep in depVerList:
                if cache.has_key(dep.TargetPkg.Name):
                    if pkg.name != dep.TargetPkg.Name and not dep.TargetPkg.Name in deps:
                        deps.add(dep.TargetPkg.Name)
			candver1 = cache._depcache.GetCandidateVer(dep.TargetPkg)
			temobj = debname(dep.TargetPkg.Name,candver1.size)
			tempobj.deplist.append(temobj)
			if tempobj not in pkglist:
				pkglist.append(tempobj)
				if(pkg.name not in tobeinstalled[currentpkg]):
	                        	tobeinstalled[currentpkg].append(dep.TargetPkg.Name)
			dependencies(cache, cache[dep.TargetPkg.Name], deps, key)
	return deps


c = apt.Cache()
pkgname = []
for i in range(2,len(sys.argv)):
	pkgname.append(sys.argv[i])
pkglist = []
rootlist = []
given_size = int(sys.argv[1])
given_size = given_size * 1024 * 1024
given_size = given_size - 733.4
current_size = 0
final = []
tobeinstalled = {}
deps = set()
currentpkg = ""
downloadl = []
for i in range(0,len(pkgname)):
	pkg = c[pkgname[i]]
	currentpkg = pkgname[i]
	tobeinstalled[pkgname[i]] = []
	rootlist.append(len(pkglist))
	deps = dependencies(c,pkg,deps,"Depends")

for i in range(0,len(pkglist)):
	current_size += pkglist[i].size


#print "TOTAL SIZE = "
#print current_size

#print tobeinstalled
#print "\n\n\n\n\n"
#print pkglist
#print current_size

for i in tobeinstalled.keys():
	while(given_size < current_size):
			#print given_size
			temp = tobeinstalled[i]
			if(len(temp) == 0):
				continue
			for j in range(0,len(pkglist)):
				if(pkglist[j].name == temp[0]):
					current_size = current_size - pkglist[j].size
					
			#current_size = current_size - temp[0].size	
			#print "\nPopped\n"			
			downloadl.append(tobeinstalled[i].pop(0))

#print "\n\n\n\n\n"
#print tobeinstalled
for i in tobeinstalled.keys():
	temp = tobeinstalled[i]
	for k in range(0,len(temp)):
		final.append(temp[k])

print "Given Size - "
print given_size
print "\nCurrent Size - "
print current_size

		
fp = open("download",'w')
for i in range(0,len(final)):
	fp.write(final[i])
	fp.write("\n")
fp.close()
fp = open("downloadl","w")
for i in range(0,len(downloadl)):
	fp.write(downloadl[i])
	fp.write("\n")
fp.close()

	
		
