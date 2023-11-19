import json
from google.cloud import firestore


class Travel(object):
    def __init__(self):
        self.db = firestore.Client()

    def add_travel(self, name, date, departure, arrive):
        travel_ref = self.db.collection('travel')
        h = {'name': name,
             'date': date,
             'departure': departure,
             'arrive': arrive
             }
        travel_ref.document(name+date).set(h)

    def get_travel(self, name, date):
        travel = []
        name = name.lower()
        travel_doc = self.db.collection('travel').document(name + date).get()

        if travel_doc.exists:
            travel.append(travel_doc.get("departure"))
            travel.append(travel_doc.get("arrive"))
            return travel
        else:
            return None

    def get_list(self, name):
        travelmates = []

        # Get all documents in the 'travel' collection
        travel_documents = self.db.collection('travel').stream()

        for doc in travel_documents:
            # Check if the provided name is in the document's name field
            if name.lower() in doc.to_dict()['name'].lower():
                t = doc.to_dict()

                # Find other travelmates with the same date, departure, and arrive
                for x in travel_documents:
                    x_data = x.to_dict()
                    if (
                            x_data['date'] == t['date']
                            and x_data['departure'] == t['departure']
                            and x_data['arrive'] == t['arrive']
                    ):
                        travelmates.append(x_data['name'])

        return travelmates
