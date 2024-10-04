def toDict(perspective_object):
    """Formats a perspective object as Dict

    Adapted from https://forum.inductiveautomation.com/t/ideal-way-to-display-objects-on-a-screen/41575

    Args:
        perspective_object: A perspective property object
    """
    from com.inductiveautomation.ignition.common import TypeUtilities

    # Convert the Perspective property object to Gson and back to a Py Object
    return TypeUtilities.gsonToPy(TypeUtilities.pyToGson(perspective_object))