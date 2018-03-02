#
# Created by pcapon on 27/02/18
#

import argparse

import time

import APIblablacarCall
import json


class tripclass:
    '''Class for keeping track of an item in inventory.'''
    Sstart: str
    Sdest: str

    def __str__(self):
        return "{} -> {}".format(self.Sstart.decode('utf8'), self.Sdest.decode('utf8'))

    def __repr__(self):
        return str(self)


class blablApi:

    def __init__(self, filetripname, apikey):
        self.triplist = self.getTripList(filetripname)
        self.apikey = apikey
        print(self.triplist)

    def searchTrajet(self):
        for trip in self.triplist:
            jsonsearch = APIblablacarCall.search(trip.Sstart, trip.Sdest, 1, self.apikey)
            if jsonsearch['pager']['pages'] > 1:
                self.pageToPage(trip, jsonsearch)
            else:
                self.getTripId(jsonsearch)

    def getTripId(self, json):
        trips = json['trips']
        #APIblablacarCall.jsonPrint(trip)
        for trip in trips:
            #APIblablacarCall.jsonPrint(trip)
            #TODO: WRITE HERE INFO TRIP
            print(trip['permanent_id'])
            id = trip['permanent_id']
            APIblablacarCall.getInfo(id, self.apikey)
            print('============================================================================================')

    def pageToPage(self, trip, jsonsearch):
            while int(jsonsearch['pager']['page']) < int(jsonsearch['pager']['pages']):
                print("{}/{}".format(jsonsearch['pager']['page'], jsonsearch['pager']['pages']))
                self.getTripId(jsonsearch)
                page = jsonsearch['pager']['page']
                page += 1
                jsonsearch = APIblablacarCall.search(trip.Sstart, trip.Sdest, page, self.apikey)


    def getTripInfo(self, jsontrip):
        """TODO"""

    def getTripList(self, filetripname):
        triplist = []
        filetrip = open(filetripname, "r")
        trips = filetrip.read().splitlines()
        for trip in trips:
            trip_class = tripclass()
            startdest = trip.split('|')
            trip_class.Sstart = startdest[0].encode('utf8')
            trip_class.Sdest = startdest[1].encode('utf8')
            triplist.append(trip_class)

        return (triplist)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filetrip', metavar='f',
                        help='File with trip')
    parser.add_argument('apikey', metavar='a',
                        help='API key')

    args = parser.parse_args()
    blabla = blablApi(args.filetrip, args.apikey)
    blabla.searchTrajet()


if __name__ == "__main__":
    main()
