# This import statement brings the application instance into the top-level of the application package. 
#  This import statement simplifies the location process. Without it the export statement a few steps below would need to be "export FLASK_APP=flaskr.flaskr".
from .flaskr import app
