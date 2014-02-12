import c4d

zero = c4d.Vector(0,0,0)
normScale = c4d.Vector(1,1,1)

def main():
  objList=doc.GetActiveObjects(True)# get the selected objects
  for obj in objList:
    oldm = obj.GetMg()
    points = obj.GetAllPoints()
    pcount = obj.GetPointCount() 
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    obj.SetAbsPos(zero)
    obj.SetAbsRot(zero)
    obj.SetAbsScale(normScale)
    newm = obj.GetMg()
    for p in xrange(pcount):
      obj.SetPoint(p,~newm*oldm*points[p])

  obj.Message(c4d.MSG_UPDATE) #Update the changes made to the object
  c4d.EventAdd()
  doc.EndUndo()

if __name__=='__main__':
  main()