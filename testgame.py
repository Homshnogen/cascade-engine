import et

vn = et.BranchingDialogue.from_list(["a", "c", "b", "e", "<3"])
vn2 = vn
print(vn)
print(vn.text)
vn = vn.choose(0)
print(vn.text)
print(vn2.text)
print(et.BranchingDialogue.from_file("test.txt"))