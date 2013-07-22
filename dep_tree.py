#!/usr/bin/env python
import sys
import apt
import pydot as pd


def dependencies(cache, pkg, deps, key="Depends"):
    #print "pkg: %s (%s)" % (pkg.name, deps)
    candver = cache._depcache.GetCandidateVer(pkg._pkg)
    name1 = pkg.name + " " + str(candver.size)
    print name1
    adj_list_row[name1] = []
    internal[name1] = 0
    #print pkg.name
    #candver = cache._depcache.GetCandidateVer(pkg._pkg)

    #adj_list_col[pkg.name] = []
    if candver == None:
        return deps
    dependslist = candver.DependsList
    if dependslist.has_key(key):
        for depVerList in dependslist[key]:
            for dep in depVerList:
                if cache.has_key(dep.TargetPkg.Name):
                    if pkg.name != dep.TargetPkg.Name and not dep.TargetPkg.Name in deps:
                        deps.add(dep.TargetPkg.Name)
			candver1 = cache._depcache.GetCandidateVer(dep.TargetPkg)
			#print candver.Size #Package size
			size = candver1.size
			#print size
			name2 = dep.TargetPkg.Name + " " + str(size)
			print name2
			adj_list_row[name1].append(name2)
			dependencies(cache, cache[dep.TargetPkg.Name], deps, key)
    return deps

internal = {}
adj_list_row = {}
#adj_list_col = {}
c = apt.Cache()

if (len(sys.argv) == 1):
	print "\nUsage: python dep_tree.py <package_name> <output_image_name>\n"
	exit(0)
pkgname = sys.argv[1]
imagename = sys.argv[2]
c = apt.Cache()
print type(c)
pkg = c[pkgname]
#print pkg.name
deps = set()

deps = dependencies(c,pkg, deps, "Depends")
#print " ".join(deps)
#print adj_list_row
final = {}
graph = pd.Dot(graph_type='digraph')
for pkname in adj_list_row.keys():
	for pkname1 in internal.keys():
		if pkname1 in adj_list_row[pkname]:
			internal[pkname1] = 1	
			edge = pd.Edge(pkname, pkname1)
			graph.add_edge(edge)
				
		else:
			internal[pkname1] = 0
	final[pkname] = internal

graph.write_png(imagename)
#print final

#preDeps = set()
#preDeps = dependencies(c,pkg, preDeps, "PreDepends")
#print " ".join(preDeps)
