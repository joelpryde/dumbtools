import c4d
from c4d import gui
from c4d import utils

def SetGlobalRotation(obj, rot):
    """
    Sets the global rotation of obj to rot
    Please remember, CINEMA 4D handles rotation in radians.
  
    Example for H=10, P=20, B=30:
  
    import c4d
    from c4d import utils
    #...
    hpb = c4d.Vector(utils.Rad(10), utils.Rad(20), utils.Rad(30))
    SetGlobalRotation(obj, hpb) #object's rotation is 10, 20, 30
    """
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector( m.v1.GetLength(),
                        m.v2.GetLength(),
                        m.v3.GetLength())
  
    m = utils.HPBToMatrix(rot)
  
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
  
    obj.SetMg(m)

# go through selected items and rotate them as if they are on a sphere at origin
def main():
    
    # get selected object (to duplicate)
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    
    #If there are less than 2 objects, quit with a useful message
    if len(selection) < 1:
        print "Please select at least 1 object"
        return
    
    # start undo
    doc.StartUndo()
    
    for obj in selection:
        objPos = obj.GetMg().off
        objPos.Normalize()
        rot = utils.VectorToHPB(objPos)
        SetGlobalRotation(obj, rot)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    
    # end undo and update ui
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
