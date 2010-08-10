from facilities.models import Facility

def encode_myway(obj):
  if isinstance(obj, Facility):
    return [obj.name,
            obj.point.x,
            obj.point.y]
    # and/or whatever else
#  elif isinstance(obj, OtherModel):
#    return [] # whatever
  else:
    raise TypeError(repr(obj) + " is not JSON serializable")