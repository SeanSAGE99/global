## shared.dev.tag
def writeConfigFromTable():
    """
    Description:
        Reads a list of tag paths and their config copied into clipboard from Excel, then writes the new config to the tags.
        Excel table should use columns:
        Tag Path | tagProp1 | tagProp2 | etc...
        
        E.g.
        Tag Path | historyEnabled | historicalProvider
        tag 1/pv | true           | sql_history

    Dependencies:
        shared.util.clipboard library
    """

    rows = shared.util.clipboard.readText()
    rows = rows.splitlines()

    # get the tag prop names from the top row starting at the 2nd column
    props = rows[0].split('\t')[1:]
    tagsAffected = []

    # loop through all tag paths and their values and write the prop values to the tags
    for row in rows[1:]:
        # get the tagPaths (string) and the propsVals (list)
        tagPath, propVals = row.split('\t')[0], row.split('\t')[1:]
        
        # if there are any props with values, then proceed, if not, ignore this tag
        if len(''.join(propVals)) != 0:
            parentPath = '/'.join(tagPath.split('/')[:-1])
            # get the current configuration so we don't munt the tag config
            cfg = system.tag.getConfiguration(basePath=tagPath)
            
            # add the props with values to the tag's config object
            for i, val in enumerate(propVals):
                if val != '':
                    cfg[0][props[i]] = val
            
            # write the updated tag config back to the tag
            ret = system.tag.configure(basePath=parentPath, tags=cfg, collisionPolicy='o')
            tagsAffected.append(tagPath)

    print 'Done. Tags affected:'
    for tag in tagsAffected: print tag