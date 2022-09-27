from datetime import datetime
import uuid
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

def get_graph():
  g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin'))
  return g

if __name__ == "__main__":
  g = get_graph()
  g.V().drop().iterate()

  id = str(uuid.uuid4())
  
  v1 = g.addV('states').property("type", "state").property("state","starting_paid").property("receive_date",datetime.now().isoformat()).property("id_payment", id).next()
  v2 = g.addV("states").property("type", "state").property("state", "waiting_authorization").property("receive_date",datetime.now().isoformat()).property("id_payment", id).next()
  v3 = g.addV("states").property("type", "state").property("state", "paid").property("receive_date",datetime.now().isoformat()).property("id_payment", id).next()

  g.V(v1).addE("changed").to(v2).iterate()
  g.V(v2).addE("changed").to(v3).iterate()
  
  