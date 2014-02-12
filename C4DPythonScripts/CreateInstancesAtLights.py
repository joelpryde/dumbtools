import c4d
from c4d import gui

def nearest_point(op, point):
    """ @param op: The polygon-object to operate on
        @param point: A c4d.Vector in global space.
        @returns: ``[point, distance, index]`` *point* is given in local space.
                  None on failure.
        """
    points = op.GetAllPoints()
    if not points: return None

    matrix = op.GetMg()
    points = iter(points)

    mesh_point = points.next()
    result = [mesh_point, (mesh_point * matrix - point).GetLength(), 0]
    index  = 1
    while True:
        try:
            mesh_point = points.next()
        except StopIteration:
            break

        distance = (mesh_point * matrix - point).GetLength()
        if distance < result[1]:
            result = [mesh_point, distance, index]

        index += 1

    return result


# duplicate first selected object at all other object's positions

def main():
    
    # get selected object (to duplicate)
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    
    #If there are less than 2 objects, quit with a useful message
    if len(selection) < 2:
        print "Please select at least 2 objects"
        return
    
    # start undo
    doc.StartUndo()
    
    # get first object
    copyObject = selection[0]
    
    for i in xrange(1, len(selection)):
        copyMatrix = selection[i].GetMg()
        objectcopy = copyObject.GetClone()
        objectcopy.SetName( selection[i].GetName().replace("Light_", "Flat_") )
        doc.InsertObject(objectcopy)
        objectcopy.SetMg(copyMatrix)
        doc.AddUndo(c4d.UNDOTYPE_NEW, objectcopy)
    
    # end undo and update ui
    doc.EndUndo()
    c4d.EventAdd()
    

if __name__=='__main__':
    main()
