import uuid
from datetime import datetime, timedelta

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal


def get_graph():
    g = traversal().withRemote(DriverRemoteConnection("ws://localhost:8182/gremlin"))
    return g


if __name__ == "__main__":
    g = get_graph()
    g.V().drop().iterate()

    id = str(uuid.uuid4())

    v1 = (
            g.addV("states")
            .property("type", "state")
            .property("state", "starting_paid")
            .property("received_date", (datetime.now() - timedelta(days=2)).timestamp())
            .property("id_payment", id)
            .next()
        )

    for i in range(10):

        id = str(uuid.uuid4())

        v1 = (
            g.addV("states")
            .property("type", "state")
            .property("state", "starting_paid")
            .property("received_date", (datetime.now() - timedelta(days=2)).timestamp())
            .property("id_payment", id)
            .next()
        )

        v2 = (
            g.addV("states")
            .property("type", "state")
            .property("state", "waiting_authorization")
            .property("received_date", (datetime.now() - timedelta(days=1)).timestamp())
            .property("id_payment", id)
            .next()
        )

        v3 = (
            g.addV("states")
            .property("type", "state")
            .property("state", "paid")
            .property("received_date", datetime.timestamp(datetime.now()))
            .property("id_payment", id)
            .next()
        )

        g.V(v1).addE("changed").to(v2).iterate()
        g.V(v2).addE("changed").to(v3).iterate()
